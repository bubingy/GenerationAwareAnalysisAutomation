import os
import glob
import time
import winreg
import shutil
import platform

import config
from utils.terminal import run_command_async, PIPE


def collect(env: dict, output_dir: os.PathLike) -> None:
    core_root_pattern = os.path.join(
        config.runtime_root,
        'artifacts', 'tests', 'coreclr',
        '*', 'Tests', 'Core_Root'
    )
    core_root_candidates = glob.glob(core_root_pattern)
    assert len(core_root_candidates) >= 1
    core_root = core_root_candidates[0]

    # search for core_run
    core_run_path_pattern = os.path.join(
        core_root, 'corerun*'
    )
    core_run_path_candidates = glob.glob(core_run_path_pattern)
    assert len(core_run_path_candidates) >= 1
    core_run_path = core_run_path_candidates[0]

    # search for GenAwareDemo.dll
    app_path_pattern = os.path.join(
        config.blog_samples_root,
        'GenAwareDemo', 'bin', 'Debug',
        '*', 'GenAwareDemo.dll'
    )
    app_path_candidates = glob.glob(app_path_pattern)
    assert len(app_path_candidates) >= 1
    app_path = app_path_candidates[0]

    # set registry keys
    system = platform.system().lower()
    if system == 'windows':
        with winreg.OpenKeyEx(
            winreg.HKEY_LOCAL_MACHINE, 
            r'SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\KnownManagedDebuggingDlls',
            0,
            winreg.KEY_SET_VALUE
        ) as debug_dll:
            winreg.SetValueEx(
                debug_dll,
                os.path.join(core_root, 'mscordaccore.dll'),
                0,
                winreg.REG_DWORD,
                0
            )

        with winreg.OpenKeyEx(
            winreg.HKEY_LOCAL_MACHINE, 
            r'SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\MiniDumpAuxiliaryDlls',
            0,
            winreg.KEY_SET_VALUE
        ) as auxiliary_dll:
            winreg.SetValueEx(
                auxiliary_dll,
                os.path.join(core_root, 'coreclr.dll'),
                0,
                winreg.REG_SZ,
                os.path.join(core_root, 'mscordaccore.dll')
            )    

    # generate command
    command = f'{core_run_path} {app_path}'.split(' ')

    tmp_path = os.path.join(config.result_bed, 'tmp')
    tmp_write = open(tmp_path, 'w+')
    tmp_read = open(tmp_path, 'r')
    
    p = run_command_async(command, cwd=output_dir, stdin=PIPE, stdout=tmp_write, env=env)
    # make sure the app is running before input
    while True:
        if 'My process id is' in tmp_read.read():
            print('app is running!')
            tmp_read.close()
            break
        else:
            time.sleep(2)
    p.stdin.write(b'run\n')
    p.communicate()
    tmp_write.close()


def collect_for_trace_only_scenario() -> str:
    result_root = os.path.join(config.result_bed, 'traceonly')
    if os.path.exists(result_root): shutil.rmtree(result_root)
    os.makedirs(result_root)

    env = os.environ.copy()
    env['COMPlus_GCGenAnalysisGen'] = '1'
    env['COMPlus_GCGenAnalysisBytes'] = '16E360'
    env['COMPlus_GCGenAnalysisDump'] = '0'
    env['COMPlus_GCGenAnalysisTrace'] = '1'

    print('collect trace only')
    collect(env, result_root)
    return result_root


def collect_for_trace_dump_scenario() -> str:
    result_root = os.path.join(config.result_bed, 'tracedump')
    if os.path.exists(result_root): shutil.rmtree(result_root)
    os.makedirs(result_root)

    env = os.environ.copy()
    env['COMPlus_GCGenAnalysisGen'] = '1'
    env['COMPlus_GCGenAnalysisBytes'] = '16E360'
    env['COMPlus_GCGenAnalysisDump'] = '1'
    env['COMPlus_GCGenAnalysisTrace'] = '1'

    print('collect trace and dump')
    collect(env, result_root)
    return result_root


def collect_for_dump_only_scenario() -> str:
    result_root = os.path.join(config.result_bed, 'dumponly')
    if os.path.exists(result_root): shutil.rmtree(result_root)
    os.makedirs(result_root)

    env = os.environ.copy()
    env['COMPlus_GCGenAnalysisGen'] = '1'
    env['COMPlus_GCGenAnalysisBytes'] = '16E360'
    env['COMPlus_GCGenAnalysisDump'] = '1'
    env['COMPlus_GCGenAnalysisTrace'] = '0'

    print('collect dump only')
    collect(env, result_root)
    return result_root


def collect_symbols() -> None:
    if 'win' not in config.rid: return
    
    print('collect symbol files')
    symbols_dir = os.path.join(config.test_bed, 'symbols')
    if not os.path.exists(symbols_dir): os.makedirs(symbols_dir)

    core_root_dlls = glob.glob(
        os.path.join(
            config.runtime_root, 'artifacts', 'tests', 'coreclr',
            'windows.x64.Checked', 'Tests', 'Core_Root', '*.dll'
        )
    )
    for core_root_dll in core_root_dlls:
        shutil.copy(core_root_dll, symbols_dir)

    app_dlls = glob.glob(
        os.path.join(
            config.blog_samples_root, 'GenAwareDemo',
            'bin', 'Debug', 'net*', '*.dll'
        )
    )
    for app_dll in app_dlls:
        shutil.copy(app_dll, symbols_dir)

    linux_symbols = glob.glob(
        os.path.join(
            config.runtime_root, 'artifacts', 'bin', 'coreclr',
            'linux.x64.Checked', 'x64', '*.dll'
        )
    )
    for linux_symbol in linux_symbols:
        shutil.copy(linux_symbol, symbols_dir)

    perfview_open_script_path = os.path.join(config.test_bed, 'open_perfview.bat')
    with open(perfview_open_script_path, 'w+') as fp:
        fp.write('@ECHO off\n')
        fp.write(f'set _NT_SYMBOL_PATH={symbols_dir}\n')
        fp.write(f'start {config.perfview_bin}\n')