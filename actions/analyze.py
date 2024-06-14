import os
import glob
from typing import Union

import app
from configuration import GenerationAwareAnalyzeConfiguration
from tools import dotnet_app
from tools import dotnet_tool
from tools.sysinfo import SysInfo
from tools.terminal import run_command_sync, run_command_async, PIPE


basic_analyze_commands = [
    b'clrstack\n',
    b'clrstack -i\n',
    b'clrthreads\n',
    b'clrmodules\n',
    b'eeheap\n',
    b'dumpheap\n',
    b'printexception\n'
    b'dso\n',
    b'eeversion\n',
    b'exit\n'
]


def install_dotnet_dump(test_conf: GenerationAwareAnalyzeConfiguration) -> Union[str, Exception]:
    return dotnet_tool.install_dotnet_dump(
        test_conf.dotnet_bin,
        test_conf.diag_tool_root,
        test_conf.basic_env
    )


@app.function_monitor(
    pre_run_msg='------ start to analyze dump ------',
    post_run_msg='------ analyze dump completed ------'
)
def analyze_dump(test_conf: GenerationAwareAnalyzeConfiguration):
    '''Run sample apps and perform tests.

    '''
    tool_dll_path = dotnet_tool.get_tool_dll(
        test_conf.diag_tool_root
    )
    if isinstance(tool_dll_path, Exception):
        return tool_dll_path
    
    

    for dump_path in dump_path_list:
        dump_name = os.path.basename(dump_path)
        analyze_output_path = os.path.join(
            test_conf.analyze_folder,
            dump_name.replace('dump', 'analyze')
        )

        analyze_commands = basic_analyze_commands.copy()
        
        # analyze dump on windows
        if test_conf.arch is not None:
            analyze_output_path = f'{analyze_output_path}_win'

            app_name = dump_name.replace('dump_', '')
            app_root = os.path.join(test_conf.test_bed, app_name)
            project_symbol_root = dotnet_app.get_app_symbol_root(app_name, app_root)
            analyze_commands.insert(
                0,
                f'setsymbolserver -directory {project_symbol_root}\n'.encode()
            )
            
        async_args = [test_conf.dotnet_bin, tool_dll_path, 'analyze', dump_path]
        
        with open(analyze_output_path, 'wb+') as fp:
            _, proc = run_command_async(async_args, stdin=PIPE, stdout=fp, stderr=fp, env=test_conf.basic_env)

            for command in analyze_commands:
                try:
                    proc.stdin.write(command)
                except Exception as exception:
                    fp.write(f'{exception}\n'.encode('utf-8'))
                    continue
            proc.communicate()


