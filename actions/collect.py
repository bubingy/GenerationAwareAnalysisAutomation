import os
import glob
import shutil

import app
from configuration import GenerationAwareAnalyzeConfiguration
from actions import target_app
from tools.sysinfo import SysInfo
from tools import dotnet_app


@app.function_monitor(
    pre_run_msg='------ start to collect trace ------',
    post_run_msg='------ collect trace completed ------'
)
def collect_for_trace_only_scenario(test_conf: GenerationAwareAnalyzeConfiguration) -> str:
    result_root = os.path.join(test_conf.test_result_folder, 'traceonly')
    if os.path.exists(result_root):
        shutil.rmtree(result_root)
    os.makedirs(result_root)

    env = os.environ.copy()
    env['COMPlus_GCGenAnalysisGen'] = '1'
    env['COMPlus_GCGenAnalysisBytes'] = '16E360'
    env['COMPlus_GCGenAnalysisDump'] = '0'
    env['COMPlus_GCGenAnalysisTrace'] = '1'

    result_root = target_app.run_genawaredemo(test_conf, result_root, env)
    return result_root


@app.function_monitor(
    pre_run_msg='------ start to collect trace and dump ------',
    post_run_msg='------ collect trace and dump completed ------'
)
def collect_for_trace_dump_scenario(test_conf: GenerationAwareAnalyzeConfiguration) -> str:
    result_root = os.path.join(test_conf.test_result_folder, 'tracedump')
    if os.path.exists(result_root): 
        shutil.rmtree(result_root)
    os.makedirs(result_root)

    env = os.environ.copy()
    env['COMPlus_GCGenAnalysisGen'] = '1'
    env['COMPlus_GCGenAnalysisBytes'] = '16E360'
    env['COMPlus_GCGenAnalysisDump'] = '1'
    env['COMPlus_GCGenAnalysisTrace'] = '1'

    result_root = target_app.run_genawaredemo(test_conf, result_root, env)
    return result_root


@app.function_monitor(
    pre_run_msg='------ start to collect dump ------',
    post_run_msg='------ collect dump completed ------'
)
def collect_for_dump_only_scenario(test_conf: GenerationAwareAnalyzeConfiguration) -> str:
    result_root = os.path.join(test_conf.test_result_folder, 'dumponly')
    if os.path.exists(result_root):
        shutil.rmtree(result_root)
    os.makedirs(result_root)

    env = os.environ.copy()
    env['COMPlus_GCGenAnalysisGen'] = '1'
    env['COMPlus_GCGenAnalysisBytes'] = '16E360'
    env['COMPlus_GCGenAnalysisDump'] = '1'
    env['COMPlus_GCGenAnalysisTrace'] = '0'

    result_root = target_app.run_genawaredemo(test_conf, result_root, env)
    return result_root


@app.function_monitor(
    pre_run_msg='------ start to collect symbols ------',
    post_run_msg='------ collect symbols completed ------'
)
def collect_symbols(test_conf: GenerationAwareAnalyzeConfiguration) -> None:
    if 'win' not in SysInfo.rid:
        return
    
    symbols_dir = os.path.join(test_conf.test_bed, 'symbols')
    if not os.path.exists(symbols_dir):
        os.makedirs(symbols_dir)

    core_root_dlls = glob.glob(
        os.path.join(
            test_conf.runtime_root, 'artifacts', 'tests', 'coreclr',
            'windows.x64.Checked', 'Tests', 'Core_Root', '*.dll'
        )
    )
    for core_root_dll in core_root_dlls:
        shutil.copy(core_root_dll, symbols_dir)

    app_dlls = glob.glob(
        os.path.join(
            test_conf.blog_samples_root, 'GenAwareDemo',
            'bin', 'Debug', 'net*', '*.dll'
        )
    )
    for app_dll in app_dlls:
        shutil.copy(app_dll, symbols_dir)

    linux_symbols = glob.glob(
        os.path.join(
            test_conf.runtime_root, 'artifacts', 'bin', 'coreclr',
            'linux.x64.Checked', 'x64', '*.dll'
        )
    )
    for linux_symbol in linux_symbols:
        shutil.copy(linux_symbol, symbols_dir)

    perfview_open_script_path = os.path.join(test_conf.test_bed, 'open_perfview.bat')
    with open(perfview_open_script_path, 'w+') as fp:
        fp.write('@ECHO off\n')
        fp.write(f'set _NT_SYMBOL_PATH={symbols_dir}\n')
        fp.write(f'start {test_conf.perfview_bin}\n')


@app.function_monitor(
    pre_run_msg='------ start to set registry keys ------',
    post_run_msg='------ set registry keys completed ------'
)
def set_registry_keys(test_conf: GenerationAwareAnalyzeConfiguration):
    core_root = dotnet_app.get_core_root(test_conf.runtime_root)
    if isinstance(core_root, Exception):
        return core_root

    # set registry keys
    if 'win' not in SysInfo.rid:
        return
    
    import winreg
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