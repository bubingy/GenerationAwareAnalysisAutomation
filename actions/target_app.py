
import os
import time
from typing import Union

import app
from configuration import GenerationAwareAnalyzeConfiguration
from tools import dotnet_app
from tools.sysinfo import SysInfo
from tools.terminal import run_command_sync, run_command_async, PIPE


@app.function_monitor(
    pre_run_msg='------ start to build runtime ------',
    post_run_msg='------ build runtime completed ------'
)
def build_runtime(test_conf: GenerationAwareAnalyzeConfiguration):
    if 'win' in SysInfo.rid: 
        script_engine = 'cmd.exe'
        command = [script_engine, '/k', test_conf.vcvars64_activation_path]
        _, p = run_command_async(
            command, 
            stdin=PIPE,
            cwd=test_conf.runtime_root
        )
        p.stdin.write(b'build.cmd -c checked -s clr\n')
        p.stdin.write(b'build.cmd -c release -s libs\n')
        p.stdin.write(b'src\\tests\\build.cmd generatelayoutonly checked\n')
        p.communicate()
    else:
        script_engine = '/bin/bash'

        command_list = [
            [script_engine, './build.sh', '-c', 'checked', '-s', 'clr'],
            [script_engine, './build.sh', '-c', 'release', '-s', 'libs'],
            [script_engine, './src/tests/build.sh', 'generatelayoutonly', 'checked']
        ]

        for command in command_list:
            command, out, err = run_command_sync(
                command,
                stdout=None, stderr=None,
                cwd=test_conf.runtime_root,
                env=test_conf.basic_env
            )


@app.function_monitor(
    pre_run_msg='------ start to build genawaredemo ------',
    post_run_msg='------ build genawaredemo completed ------'
)
def build_genawaredemo(test_conf: GenerationAwareAnalyzeConfiguration):
    app_name = 'GenAwareDemo'
    app_root = os.path.join(test_conf.blog_samples_root, app_name)

    app_root = dotnet_app.build_app(test_conf.dotnet_bin, app_root, test_conf.basic_env)
    return app_root


@app.function_monitor(
    pre_run_msg='------ start to run genawaredemo ------',
    post_run_msg='------ run genawaredemo completed ------'
)
def run_genawaredemo(test_conf: GenerationAwareAnalyzeConfiguration,
                     output_folder: str,
                     extra_env: os._Environ) -> Union[str, Exception]:
    corerun_path = dotnet_app.get_corerun_path(test_conf.runtime_root)
    if isinstance(corerun_path, Exception):
        return corerun_path

    app_name = 'GenAwareDemo'
    app_root = os.path.join(test_conf.blog_samples_root, app_name)
    app_dll_path = dotnet_app.get_app_dll(app_name, app_root)
    if isinstance(app_dll_path, Exception):
        return app_dll_path

    command = [corerun_path, app_dll_path]

    tmp_path = os.path.join(output_folder, 'tmp')
    tmp_write = open(tmp_path, 'w+')
    tmp_read = open(tmp_path, 'r')
    
    _, p = run_command_async(command, cwd=output_folder, stdin=PIPE, stdout=tmp_write, env=extra_env)
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

    return output_folder
