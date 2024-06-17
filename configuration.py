import os
import configparser

from tools.sysinfo import SysInfo


class GenerationAwareAnalyzeConfiguration:
    def __init__(self, conf_file_path: str):
        self.__parse_conf_file(conf_file_path)

        self.conf_file_path = conf_file_path
            
        self.test_result_folder = os.path.join(self.test_bed, f'TestResult')

        self.runtime_root = os.path.join(self.test_bed, 'runtime')
        self.blog_samples_root = os.path.join(self.test_bed, 'blog-samples')

        self.diag_tool_root = os.path.join(self.test_bed, f'diag-tool')

        env = os.environ.copy()
        if 'win' in SysInfo.rid:
            self.sdk_root = ''
            self.dotnet_bin = 'dotnet'
            env['PATH'] = f'{self.diag_tool_root}{SysInfo.env_connector}' + env['PATH']

        else:
            self.dotnet_root = os.path.join(self.runtime_root, '.dotnet')
            self.dotnet_bin = os.path.join(self.dotnet_root, f'dotnet{SysInfo.bin_ext}')
            
            env['DOTNET_ROOT'] = self.dotnet_root
            env['PATH'] = f'{self.dotnet_root}{SysInfo.env_connector}{self.diag_tool_root}{SysInfo.env_connector}' + env['PATH']

        self.basic_env: dict = env    


    def __parse_conf_file(self, conf_file_path: str) -> None:
        '''Parse configuration file 
        
        :param conf_file_path: path to configuration file
        :return: DiagToolsTestConfiguration instance or Exception
        '''
        try:
            config = configparser.ConfigParser()
            config.read(conf_file_path)
            # DotNet section
            self.runtime_repo: str = config['Runtime']['repo']
            self.runtime_commit: str = config['Runtime']['commit']
            self.blog_samples_repo: str = config['Blog-Samples']['repo']
            self.blog_samples_commit: str = config['Blog-Samples']['commit']
            self.test_bed: str = config['Test']['testbed']
            self.vcvars64_activation_path = config['Build']['vcvars64']
            self.perfview_bin = config['Test']['perfview']

        except Exception as ex:
            raise Exception(f'fail to parse conf file {conf_file_path}: {ex}')  