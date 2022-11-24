import os
import glob
from subprocess import PIPE

from Model.configuration import *
from Model.sysinfo import *
from Service.utils import *


class DiagToolService:
    @classmethod
    def insatll_dotnet_sos(cls):
        tool_path_pattern = os.path.join(
            DiagnosticsConfiguration.root,
            '.store', 'dotnet-sos', '*', 'dotnet-sos', '*', 'tools', '*', 'any', 'dotnet-sos.dll'
        )
        if DiagnosticsConfiguration.version != '' and DiagnosticsConfiguration.feed != '':
            command = ' '.join(
                [
                    f'{DotNetInfo.dotnet} tool install dotnet-sos',
                    f'--tool-path {DiagnosticsConfiguration.root}',
                    f'--version {DiagnosticsConfiguration.version}',
                    f'--add-source {DiagnosticsConfiguration.feed}'
                ]
            )
        else:
            command = ' '.join(
                [
                    f'{DotNetInfo.dotnet} tool install dotnet-sos',
                    f'--tool-path {DiagnosticsConfiguration.root}'
                ]
            )
        
        if len(glob.glob(tool_path_pattern)) == 0: 
            outs, errs = run_command_sync(command, stdin=PIPE, stdout=PIPE)
            
            print(outs)
            print(errs)

        tool_path = glob.glob(tool_path_pattern)[0]
        tool_bin = f'{DotNetInfo.dotnet} {tool_path}'

        command = f'{tool_bin} install'
        outs, errs = run_command_sync(command, stdin=PIPE, stdout=PIPE)
        
        print(outs)
        print(errs)


    @classmethod
    def run_dumpheap(cls, dump_root: str):
        dump_path = glob.glob(os.path.join(dump_root, '*.dmp'))[0]
        analyze_output_path = os.path.join(dump_root, 'debug_dump.log')

        if 'win' in OSInfo.os_name:
            plugin_path = os.path.join(
                os.environ['USERPROFILE'],
                '.dotnet', 'sos', 'sos.dll'
            )
            analyze_commands = [
                b'sxe ld coreclr\n',
                f'.load {plugin_path}\n'.encode('utf-8'),
                b'!dumpheap\n',
                b'.detach\n',
                b'q\n'
            ]
            debug_script = os.path.join(
                TestConfiguration.test_bed,
                'cdb_debug_script'
            )
            with open(debug_script, 'wb+') as fs:
                fs.writelines(analyze_commands)

            with open(analyze_output_path, 'w+') as fs:
                command = f'{OSInfo.debugger} -z {dump_path} -cf {debug_script}'
                run_command_sync(command, stdout=fs, stderr=fs)
            
        else:
            analyze_commands = [
                b'dumpheap\n',
                b'exit\n',
                b'y\n'
            ]

            with open(analyze_output_path, 'w+') as fs:
                command = f'{OSInfo.debugger} -c {dump_path}'
                p = run_command_async(command, stdin=PIPE, stdout=fs, stderr=fs)
                for command in analyze_commands:
                    p.stdin.write(command)
                    
                p.communicate()