import os 

import app
from configuration import GenerationAwareAnalyzeConfiguration
from tools.git import git_clone, git_reset


@app.function_monitor(
    pre_run_msg='------ start to clone runtime from github ------',
    post_run_msg='------ clone runtime completed ------'
)
def download_runtime(test_conf: GenerationAwareAnalyzeConfiguration) -> None:
    '''clone dotnet/runtime to testbed

    :return: None
    '''
    assert not os.path.exists(test_conf.runtime_root)

    git_clone(test_conf.runtime_repo, test_conf.runtime_root)
    git_reset(test_conf.runtime_root, test_conf.runtime_commit)


@app.function_monitor(
    pre_run_msg='------ start to clone blog-samples from github ------',
    post_run_msg='------ clone blog-samples completed ------'
)
def download_blog_samples(test_conf: GenerationAwareAnalyzeConfiguration) -> None:
    '''clone cshung/blog-samples to testbed

    :return: None
    '''
    assert not os.path.exists(test_conf.blog_samples_root)
    
    git_clone(test_conf.blog_samples_repo, test_conf.blog_samples_root)
    git_reset(test_conf.blog_samples_root, test_conf.blog_samples_commit)


def download_all(test_conf: GenerationAwareAnalyzeConfiguration) -> None:
    '''clone dotnet/runtime and cshung/blog-samples to testbed

    :return: None
    '''
    assert not os.path.exists(test_conf.runtime_root)
    assert not os.path.exists(test_conf.blog_samples_root)
    download_runtime()
    download_blog_samples()
