import os
import glob

import config
from utils.terminal import run_command_sync, run_command_async, PIPE


def install_dotnet_dump() -> None:

    command = f'dotnet tool install dotnet-dump --tool-path {config.tool_root}'
    
    run_command_sync(command, env=config.basic_env_variables)


def analyze_dump(dump_root: str) -> None:
    dump_path_candidates = glob.glob(os.path.join(dump_root, 'gcgenaware.*.dmp'))
    if len(dump_path_candidates) == 0:
        return print(f'no dump file in {dump_root}')
    
    dump_path = dump_path_candidates[0]
    analyze_output_path = os.path.join(
        dump_root,
        'dump_analyze.log'
    )

    tool_path_pattern = \
        f'{config.tool_root}/.store/dotnet-dump/*/dotnet-dump/*/tools/*/any/dotnet-dump.dll'
    tool_path = glob.glob(tool_path_pattern)[0]

    analyze_commands = [
        b'dumpheap\n',
        b'exit\n'
    ]
    with open(analyze_output_path, 'w+') as f:
        command = f'dotnet {tool_path} analyze {dump_path}'
        print(f'run command: {command}')
        proc = run_command_async(
            command,
            cwd=dump_root,
            env=config.basic_env_variables,
            stdin=PIPE,
            stdout=f,
            stderr=f
        )

        for command in analyze_commands:
            try:
                proc.stdin.write(command)
            except Exception as exception:
                f.write(f'{exception}\n'.encode('utf-8'))
                continue
        proc.communicate()