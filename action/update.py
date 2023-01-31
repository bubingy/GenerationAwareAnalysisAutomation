import os

import config
from utils.git import git_pull, git_reset


def update_runtime() -> None:
    '''update dotnet/runtime

    :return: None
    '''
    assert os.path.exists(config.runtime_root)
    git_pull(config.runtime_root)
    git_reset(config.runtime_root, config.runtime_commit)


def update_blog_samples() -> None:
    '''update cshung/blog-samples

    :return: None
    '''
    assert os.path.exists(config.blog_samples_root)
    git_pull(config.blog_samples_root)
    git_reset(config.blog_samples_root, config.blog_samples_commit)


def update_all() -> None:
    '''update dotnet/runtime and cshung/blog-samples

    :return: None
    '''
    assert os.path.exists(config.runtime_root)
    assert os.path.exists(config.blog_samples_root)
    update_runtime()
    update_blog_samples()
