import re
import glob
import platform

class SysInfo:
    @staticmethod
    def get_os_name():
        system = platform.system().lower()
        if system == 'windows':
            os = 'win'
        elif system == 'linux':
            release_files = glob.glob('/etc/*release')
            content = ''
            for release_file in release_files:
                with open(release_file, 'r') as f:
                    content += f.read().lower()
            if 'alpine' in content:
                os = 'linux-musl'
            else:
                os = 'linux'
        elif system== 'darwin':
            os = 'osx'
        else:
            raise Exception(f'unsupported OS: {system}')
        return os

    @staticmethod
    def get_debugger(os: str):
        '''Get full name of debugger.
        
        Args:
            rid - `.Net RID` of current platform.
        Return: full name of debugger.
        '''
        if 'musl' in os:
            return ''
        elif 'win' in os:
            debugger = 'cdb'
            return debugger
        else: # linux or osx
            candidate_debuggers = glob.glob('/usr/bin/lldb*')
            if '/usr/bin/lldb' in candidate_debuggers:
                debugger = 'lldb'
                return debugger
            else:
                pattern = re.compile(r'/usr/bin/lldb-\d+')
                for candidate_debugger in candidate_debuggers:
                    if pattern.match(candidate_debugger) is not None:
                        debugger = candidate_debugger.split('/')[-1]
                        return debugger

