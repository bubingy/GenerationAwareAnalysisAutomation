import os
import sys
import configparser

import config
from utils.sysinfo import get_rid


def load_config(config_file_path: os.PathLike) -> None:
    '''load config from conf file

    :param config_file_path: abs path of config file
    :return: None
    '''
    conf = configparser.ConfigParser()
    conf.read(config_file_path)
    
    config.rid = get_rid()
    if 'win' in config.rid:
        env_connector = ';'
        bin_ext = '.exe'
    else: 
        env_connector = ':'
        bin_ext = ''

    config.test_bed = conf['Test']['testbed']
    config.perfview_bin = conf['Test']['perfview']
    config.result_bed = os.path.join(config.test_bed, 'TestResult')
    
    config.vcvars64_activation_path = conf['Build']['vcvars64']

    config.runtime_root = os.path.join(config.test_bed, 'runtime')
    config.runtime_commit = conf['Runtime']['commit']

    config.blog_samples_root = os.path.join(config.test_bed, 'blog-samples')
    config.blog_samples_commit = conf['Blog-Samples']['commit']

    config.sdk_root = os.path.join(
        config.runtime_root,
        '.dotnet'
    )
    config.dotnet_bin = os.path.join(
        config.sdk_root,
        f'dotnet{bin_ext}'
    )
    config.tool_root = os.path.join(
        config.test_bed,
        'dotnet-dump'
    )

    env = os.environ.copy()
    env['DOTNET_ROOT'] = config.sdk_root
    env['PATH'] = f'{config.sdk_root}{env_connector}{config.tool_root}{env_connector}' + env['PATH']
    config.basic_env_variables = env


def init_test() -> None:
    config_file_path = os.path.join(
        os.path.dirname(
            os.path.abspath(
                sys.argv[0]
            )
        ),
        'run.conf'
    )
    load_config(config_file_path)
    if not os.path.exists(config.test_bed): os.makedirs(config.test_bed)
    if not os.path.exists(config.result_bed): os.makedirs(config.result_bed)
    