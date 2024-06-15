import os
import glob
from typing import Union

import app
from configuration import GenerationAwareAnalyzeConfiguration
from tools import dotnet_tool
from tools.terminal import run_command_async, PIPE


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


@app.function_monitor(
    pre_run_msg='------ start to install dotnet-dump ------',
    post_run_msg='------ install dotnet-dump completed ------'
)
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
def analyze_dump(test_conf: GenerationAwareAnalyzeConfiguration, output_folder: str):
    '''Run sample apps and perform tests.

    '''
    tool_dll_path = dotnet_tool.get_tool_dll(
        test_conf.diag_tool_root
    )
    if isinstance(tool_dll_path, Exception):
        return tool_dll_path
    
    dump_path_list = glob.glob(os.path.join(output_folder, 'gcgenaware.*.dmp'))
    if len(dump_path_list) == 0:
        return Exception(f'no dump file in {output_folder}')
    
    for dump_path in dump_path_list:
        dump_name = os.path.basename(dump_path)
        analyze_output_path = os.path.join(
            test_conf.analyze_folder,
            dump_name.replace('dump', 'analyze')
        )

        analyze_commands = basic_analyze_commands.copy()
            
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


