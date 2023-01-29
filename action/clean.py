import os

import config
from utils.git import git_reset


def clean_runtime() -> None:
    '''clean dotnet/runtime

    :return: None
    '''
    assert os.path.exists(config.runtime_root)
    git_reset(config.runtime_root, config.runtime_commit, 'hard')


def clean_blog_samples() -> None:
    '''clean cshung/blog-samples

    :return: None
    '''
    assert os.path.exists(config.blog_samples_root)
    git_reset(config.blog_samples_root, config.blog_samples_commit, 'hard')


def clean_all() -> None:
    '''clean dotnet/runtime and cshung/blog-samples

    :return: None
    '''
    assert os.path.exists(config.runtime_root)
    assert os.path.exists(config.blog_samples_root)
    clean_runtime()
    clean_blog_samples()
