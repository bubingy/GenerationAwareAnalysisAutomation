'''methods for dotnet tool installation'''

import glob
from typing import Union

import app
from tools.terminal import run_command_sync


@app.function_monitor(
    pre_run_msg='start to install dotnet-dump',
    post_run_msg='install dotnet-dump completed'
)
def install_dotnet_dump(dotnet_bin_path: str, 
                        tool_root: str, 
                        env: dict) -> Union[str, Exception]:
    '''Install dotnet tool
    
    :param dotnet_bin_path: path to dotnet executable
    :param tool: name of tool
    :param tool_root: parent dir of the tool
    :param tool_version: version of tool
    :param tool_feed: feed of tool
    :param env: required environment variable
    :return: parent dir of the tool or exception if fail to install
    '''
    args = [
        dotnet_bin_path, 'tool', 'install', 'dotnet-dump',
        '--tool-path', tool_root,
    ]
    command, stdout, stderr = run_command_sync(args, env=env)
    if stderr != '':
        return Exception(f'fail to install dotnet-dump, see log for details')
    else:
        return tool_root


def get_tool_dll(tool_root: str) -> Union[str, Exception]:
    '''Get path of executable file

    :param tool_name: name of diag tool
    :param tool_root: root of diag tools
    :return: path of executable file or exception if fail to create
    '''
    tool_name = 'dotnet-dump'
    tool_dll_path_template = (
        f'{tool_root}/.store/{tool_name}'
        f'/*/{tool_name}'
        f'/*/tools/*/any/{tool_name}.dll'
    )
    tool_dll_path_candidates = glob.glob(tool_dll_path_template)
    
    if len(tool_dll_path_candidates) < 1:
        return Exception(f'no dll file availble for {tool_name}')
    return tool_dll_path_candidates[0]