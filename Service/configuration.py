import os
import configparser

from Service.utils import *
from Model.configuration import *

class ConfigurationService:
    @classmethod
    def load_configuration_from_file(cls, config_file_path: str):
        config = configparser.ConfigParser()
        config.read(config_file_path)
        cls.__init_test_configuration()
        cls.__init_diagnostics_configuration()

    @staticmethod
    def __init_test_configuration(config: configparser.ConfigParser):
        TestConfiguration.test_bed = config['Test']['TestBed']
        TestConfiguration.runtime_root = os.path.join(TestConfiguration.test_bed, 'runtime')
        TestConfiguration.runtime_commit = config['Test']['RuntimeCommit']
        TestConfiguration.genawaredemo_root = os.path.join(TestConfiguration.test_bed, 'blog-samples', 'GenAwareDemo')
        TestConfiguration.genawaredemo_commit = config['Test']['GenAwareDemoCommit']

    @staticmethod
    def __init_diagnostics_configuration(config: configparser.ConfigParser):
        DiagnosticsConfiguration.diagnostics_root = os.path.join(TestConfiguration.test_bed, 'diagnostics')
        DiagnosticsConfiguration.diagnostics_version = config['Diagnostics']['version']
        os_name = get_os_name()
        if 'win' in os_name: os.environ['PATH'] = f'{DiagnosticsConfiguration.diagnostics_root};' + os.environ['PATH'] 
        else: os.environ['PATH'] = f'{DiagnosticsConfiguration.diagnostics_root}:' + os.environ['PATH']

        os.environ['COMPlus_GCGenAnalysisGen'] = '1'
        os.environ['COMPlus_GCGenAnalysisBytes'] = '16E360'
        