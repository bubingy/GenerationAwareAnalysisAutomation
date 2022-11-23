import os

from Model.sysinfo import *
from Model.configuration import TestConfiguration
from Service.utils import *

class OSInfoService:
    @staticmethod
    def init_os_name():
        OSInfo.os_name = get_os_name()

    @staticmethod
    def init_debugger(os: str):
        os_name = get_os_name()
        OSInfo.debugger = get_debugger(os_name)


class DotNetInfoService:
    @staticmethod
    def init_dotnet_info():
        DotNetInfo.dotnet_root = os.path.join(TestConfiguration.test_bed, 'runtime', '.dotnet')
        for sdk in os.listdir(os.path.join(DotNetInfo.dotnet_root, 'sdk')):
            DotNetInfo.sdk_version = sdk
            break

        os_name = get_os_name()
        
        if 'win' in os_name: os.environ['PATH'] = f'{DotNetInfo.dotnet_root};' + os.environ['PATH'] 
        else: os.environ['PATH'] = f'{DotNetInfo.dotnet_root}:' + os.environ['PATH']

        os.environ['DOTNET_ROOT'] = DotNetInfo.dotnet_root