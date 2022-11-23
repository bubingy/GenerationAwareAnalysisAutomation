import os
import configparser

from Service.utils import *
from Model.configuration import *

class ConfigurationService:
    @classmethod
    def load_configuration_from_file(cls, config_file_path: str):
        config = configparser.ConfigParser()
        config.read(config_file_path)
        cls.__init_test_configuration(config)
        cls.__init_diagnostics_configuration(config)

    @staticmethod
    def __init_test_configuration(config: configparser.ConfigParser):
        TestConfiguration.test_bed = config['Test']['TestBed']
        
        RuntimeConfiguration.root = os.path.join(TestConfiguration.test_bed, 'runtime')
        RuntimeConfiguration.commit = config['Test']['RuntimeCommit']

        GenAwareDemoConfiguration.root = os.path.join(TestConfiguration.test_bed, 'blog-samples', 'GenAwareDemo')
        GenAwareDemoConfiguration.commit = config['Test']['GenAwareDemoCommit']

    @staticmethod
    def __init_diagnostics_configuration(config: configparser.ConfigParser):
        DiagnosticsConfiguration.root = os.path.join(TestConfiguration.test_bed, 'diagnostics')
        DiagnosticsConfiguration.version = config['Diagnostics']['Version']
        DiagnosticsConfiguration.feed = config['Diagnostics']['Feed']
        os_name = get_os_name()
        if 'win' in os_name: os.environ['PATH'] = f'{DiagnosticsConfiguration.root};' + os.environ['PATH'] 
        else: os.environ['PATH'] = f'{DiagnosticsConfiguration.root}:' + os.environ['PATH']
        