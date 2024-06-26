'''methods for dotnet app creation and building'''

import os
import glob
from typing import Union

import app
from tools.terminal import run_command_sync
from tools.sysinfo import SysInfo


def get_app_dll(app_name: str, app_root: str) -> Union[str, Exception]:
    '''Get path of dll file

    :param app_name: type of .NET app
    :param app_root: root of .NET app
    :return: path of dll file or exception if can't find
    '''
    project_dll_path_template = os.path.join(
        app_root,
        'bin',
        '*',
        '*',
        f'{app_name}.dll'
    )
    project_dll_path_candidates = glob.glob(project_dll_path_template)

    if len(project_dll_path_candidates) < 1:
        return Exception(f'no dll file availble for {app_root}')
    
    return project_dll_path_candidates[0]
    

def get_app_bin(app_name: str, app_root: str) -> Union[str, Exception]:
    '''Get path of executable file

    :param app_name: type of .NET app
    :param app_root: root of .NET app
    :return: path of executable file or exception if can't find
    '''
    project_bin_path_template = os.path.join(
        app_root,
        'bin',
        '*',
        '*',
        f'{app_name}{SysInfo.bin_ext}'
    )
    project_bin_path_candidates = glob.glob(project_bin_path_template)

    if len(project_bin_path_candidates) < 1:
        return Exception(f'no executable file availble for {app_root}')
    return project_bin_path_candidates[0]


def get_app_symbol_root(app_name: str, app_root: str) -> Union[str, Exception]:
    '''Get folder of executable file

    :param app_name: type of .NET app
    :param app_root: root of .NET app
    :return: path of executable file or exception if fail to create
    '''
    dll_path = get_app_dll(app_name, app_root)
    if isinstance(dll_path, Exception):
        return dll_path
    return os.path.dirname(dll_path)


@app.function_monitor()
def build_app(dotnet_bin_path: str, 
              app_root: str,
              env: dict) -> Union[str, Exception]:
    '''build app with dotnet command

    :param dotnet_bin_path: path to dotnet executable
    :param app_root: path to the project
    :param env: required environment variable
    :return: path to the project or exception if fail to create
    '''
    args = [
        dotnet_bin_path, 'build'
    ]
    command, stdout, stderr = run_command_sync(args, cwd=app_root, env=env)
    if stderr != '':
        return Exception(f'fail to install tool, see log for details')
    else:
        return app_root


def get_core_root(runtime_root: str) -> Union[str, Exception]:
    # search for core_root
    if 'win' in SysInfo.rid:
        platform_pattern = 'windows.*.Checked'
    else:
        platform_pattern = '*.Checked'
    core_root_pattern = os.path.join(
        runtime_root,
        'artifacts', 'tests', 'coreclr',
        platform_pattern, 'Tests', 'Core_Root'
    )
    core_root_candidates = glob.glob(core_root_pattern)
    if len(core_root_candidates) < 1:
        return Exception('Core_Root not found!')
    else:
        return core_root_candidates[0]


def get_corerun_path(runtime_root: str) -> Union[str, Exception]:
    core_root = get_core_root(runtime_root)
    if isinstance(core_root, Exception):
        return core_root
    
    core_run_path_pattern = os.path.join(
        core_root, 'corerun*'
    )
    core_run_path_candidates = glob.glob(core_run_path_pattern)
    if len(core_run_path_candidates) < 1:
        return Exception('corerun not found!')
    else:
        return core_run_path_candidates[0]