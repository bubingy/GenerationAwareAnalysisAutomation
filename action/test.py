import os
import glob
import time
import shutil
from subprocess import PIPE

import config
from utils.terminal import run_command_async


def run_test(env: dict, output_dir: os.PathLike) -> None:
    core_run_path_pattern = os.path.join(
        config.runtime_root,
        'artifacts', 'tests', 'coreclr',
        '*', 'Tests', 'Core_Root', 'corerun*'
    )
    core_run_path_candidates = glob.glob(core_run_path_pattern)
    assert len(core_run_path_candidates) >= 1
    core_run_path = core_run_path_candidates[0]

    app_path_pattern = os.path.join(
        config.blog_samples_root,
        'GenAwareDemo', 'bin', 'Debug',
        '*', 'GenAwareDemo.dll'
    )
    app_path_candidates = glob.glob(app_path_pattern)
    assert len(app_path_candidates) >= 1
    app_path = app_path_candidates[0]

    command = f'{core_run_path} {app_path}'

    tmp_path = os.path.join(config.result_bed, 'tmp')
    tmp_write = open(tmp_path, 'w+')
    tmp_read = open(tmp_path, 'r')
    
    p = run_command_async(command, cwd=output_dir, stdin=PIPE, stdout=tmp_write, env=env)
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


def test_trace_only_scenario() -> None:
    result_root = os.path.join(config.result_bed, 'traceonly')
    if os.path.exists(result_root): shutil.rmtree(result_root)
    os.makedirs(result_root)

    env = os.environ.copy()
    env['COMPlus_GCGenAnalysisGen'] = '1'
    env['COMPlus_GCGenAnalysisBytes'] = '16E360'
    env['COMPlus_GCGenAnalysisDump'] = '0'
    env['COMPlus_GCGenAnalysisTrace'] = '1'

    run_test(env, result_root)


def test_trace_dump_scenario() -> None:
    result_root = os.path.join(config.result_bed, 'tracedump')
    if os.path.exists(result_root): shutil.rmtree(result_root)
    os.makedirs(result_root)

    env = os.environ.copy()
    env['COMPlus_GCGenAnalysisGen'] = '1'
    env['COMPlus_GCGenAnalysisBytes'] = '16E360'
    env['COMPlus_GCGenAnalysisDump'] = '1'
    env['COMPlus_GCGenAnalysisTrace'] = '1'

    run_test(env, result_root)


def test_dump_only_scenario() -> None:
    result_root = os.path.join(config.result_bed, 'dumponly')
    if os.path.exists(result_root): shutil.rmtree(result_root)
    os.makedirs(result_root)

    env = os.environ.copy()
    env['COMPlus_GCGenAnalysisGen'] = '1'
    env['COMPlus_GCGenAnalysisBytes'] = '16E360'
    env['COMPlus_GCGenAnalysisDump'] = '1'
    env['COMPlus_GCGenAnalysisTrace'] = '0'

    run_test(env, result_root)
