import os 

import config
from utils.git import git_clone, git_reset


def download_runtime() -> None:
    '''clone dotnet/runtime to testbed

    :return: None
    '''
    assert not os.path.exists(config.runtime_root)
    print(f'clone runtime from github')
    git_clone('dotnet', 'runtime', config.test_bed)
    git_reset(config.runtime_root, config.runtime_commit)


def download_blog_samples() -> None:
    '''clone cshung/blog-samples to testbed

    :return: None
    '''
    assert not os.path.exists(config.blog_samples_root)
    print(f'clone blog-samples from github')
    git_clone('cshung', 'blog-samples', config.test_bed)
    git_reset(config.blog_samples_root, config.blog_samples_commit)


def download_all() -> None:
    '''clone dotnet/runtime and cshung/blog-samples to testbed

    :return: None
    '''
    assert not os.path.exists(config.runtime_root)
    assert not os.path.exists(config.blog_samples_root)
    download_runtime()
    download_blog_samples()
