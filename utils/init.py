import os
import sys
import configparser

import config


def load_config(config_file_path: os.PathLike) -> None:
    '''load config from conf file

    :param config_file_path: abs path of config file
    :return: None
    '''
    conf = configparser.ConfigParser()
    conf.read(config_file_path)
    config.test_bed = conf['Test']['testbed']
    config.result_bed = os.path.join(config.test_bed, 'TestResult')

    config.runtime_root = os.path.join(config.test_bed, 'runtime')
    config.runtime_commit = conf['Runtime']['commit']

    config.blog_samples_root = os.path.join(config.test_bed, 'blog-samples')
    config.blog_samples_commit = conf['Blog-Samples']['commit']


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
    