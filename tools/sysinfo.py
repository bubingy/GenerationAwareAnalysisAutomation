'''Provide system information'''

import re
import glob
import platform
from typing import Union


def _get_os_type() -> Union[str, Exception]:
    '''get name of operation system
    
    :return: name of os or Exception if failed
    '''
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
        os = Exception('unknown os')
    return os


def _get_cpu_type() -> Union[str, Exception]:
    '''get type of CPU
    
    :return: type of cpu or Exception if failed
    '''
    machine_type = platform.machine().lower()
    if machine_type in ['x86_64', 'amd64']:
        cpu_arch = 'x64'
    elif machine_type in ['aarch64', 'arm64']:
        cpu_arch = 'arm64'
    elif machine_type in ['armv7l']:
        cpu_arch = 'arm'
    else:
        cpu_arch = Exception('unknown cpu')
    return cpu_arch


def _get_rid() -> Union[str, Exception]:
    '''Get .Net RID of current platform

    :return: .Net RID of current platform or Exception if failed
    '''
    os_type = _get_os_type()
    cpu_arch = _get_cpu_type()
    if isinstance(os_type, Exception):
        return os_type
    if isinstance(cpu_arch, Exception):
        return cpu_arch
    else:
        return f'{os_type}-{cpu_arch}'


class SysInfo:
    rid: str = _get_rid()
    bin_ext: str = None
    env_connector: str = None

    if 'win' in rid:
        bin_ext: str = '.exe'
        env_connector: str = ';'
    else:
        bin_ext: str = ''
        env_connector: str = ':'

    