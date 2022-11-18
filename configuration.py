import os
import configparser

from sysinfo import SysInfo

class Configuration:
    test_bed = ''

    dotnet_root = ''
    dotnet = ''

    diagnostics_tool_root = ''

    runtime_root = ''
    genawaredemo_root = ''

    debugger = ''

    @classmethod
    def load_configuration_from_file(cls, config_file_path: str):
        config = configparser.ConfigParser()
        config.read(config_file_path)

        cls.test_bed = config['Test']['TestBed']
        cls.runtime_root = config['Runtime']['root']
        cls.genawaredemo_root = config['GenAwareDemo']['root']

        cls.dotnet_root = os.path.join(cls.runtime_root, '.dotnet')
        cls.diagnostics_tool_root = os.path.join(cls.test_bed, 'dotnet-tool')

        os_name = SysInfo.get_os_name()
        cls.debugger = SysInfo.get_debugger(os_name)

        os.environ['COMPlus_GCGenAnalysisGen'] = '1'
        os.environ['COMPlus_GCGenAnalysisBytes'] = '16E360'
        os.environ['DOTNET_ROOT'] = cls.dotnet_root
        if 'win' in os_name:
            os.environ['PATH'] = f'{cls.dotnet_root};{cls.diagnostics_tool_root};' + os.environ['PATH'] 
            cls.dotnet = 'dotnet'
        else:
            os.environ['PATH'] = f'{cls.dotnet_root}:{cls.diagnostics_tool_root}:' + os.environ['PATH']
            cls.dotnet = os.path.join(cls.dotnet_root, 'dotnet')