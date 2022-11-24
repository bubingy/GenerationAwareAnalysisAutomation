import os
import glob
from subprocess import Popen, PIPE

from Model.configuration import *
from Model.sysinfo import *

class DiagToolService:
    @classmethod
    def insatll_dotnet_sos(cls):
        command = ' '.join(
            [
                f'{DotNetInfo.dotnet} tool install dotnet-sos',
                f'--tool-path {DiagnosticsConfiguration.root}',
                f'--version {DiagnosticsConfiguration.version}',
                f'--add-source {DiagnosticsConfiguration.feed}'
            ]
        ).split(' ')

        p = Popen(command, stdin=PIPE, stdout=PIPE)
        outs, errs = p.communicate()
        
        print(outs.decode())
        print(errs.decode())

        tool_path_pattern = f'{DiagnosticsConfiguration.root}/.store/dotnet-sos/{DiagnosticsConfiguration.version}/dotnet-sos/{DiagnosticsConfiguration.version}/tools/*/any/dotnet-sos.dll'
        tool_path = glob.glob(tool_path_pattern)[0]
        tool_bin = f'{DotNetInfo.dotnet} {tool_path}'

        command = f'{tool_bin} install'

        p = Popen(command, stdin=PIPE, stdout=PIPE)
        outs, errs = p.communicate()
        
        print(outs.decode())
        print(errs.decode())
    
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
                p = Popen(stdout=fs, stderr=fs)
                p.communicate()
            
        else:
            analyze_commands = [
                b'dumpheap\n',
                b'exit\n',
                b'y\n'
            ]

            with open(analyze_output_path, 'w+') as fs:
                command = f'{OSInfo.debugger} -c {dump_path}'
                p = Popen(command, stdin=PIPE,stdout=fs, stderr=fs)
                for command in analyze_commands:
                    p.stdin.write(command)
                    
                p.communicate()