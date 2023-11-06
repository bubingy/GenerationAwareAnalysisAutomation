import os
from urllib import request

from utils.terminal import run_command_sync


def get_repo(owner: str, repo: str) -> bool:
    '''determine whether the repo is valid

    :param owner: owner of the repo
    :param repo: name of repo
    :return: return True if the repo is valid, otherwise return False 
    '''
    url = f'https://api.github.com/repos/{owner}/{repo}'
    req = request.Request(url)
    try:
        resp = request.urlopen(req)
        return True
    except Exception as e:
        print('fail to find the repo')
        return False


def git_clone(owner: str, repo: str, parent_folder: os.PathLike) -> None:
    '''clone the repo

    :param owner: owner of the repo
    :param repo: name of repo
    :param parent_folder: where to clone the repo
    :return: None 
    '''
    assert os.path.isdir(parent_folder)
    assert get_repo(owner, repo)
    
    run_command_sync('git config --system core.longpaths true'.split(' '))
    run_command_sync(f'git clone https://github.com/{owner}/{repo}.git'.split(' '), cwd=parent_folder)


def git_pull(repo_folder: os.PathLike) -> None:
    '''update the repo

    :param repo_folder: the root of the repo
    :return: None 
    '''
    assert '.git' in os.listdir(repo_folder)
    run_command_sync('git config --system core.longpaths true'.split(' '))
    run_command_sync('git pull'.split(' '), cwd=repo_folder)


def git_reset(repo_folder: os.PathLike, commit_number: str, reset_type: str='soft') -> None:
    '''reset the repo

    :param repo_folder: the root of the repo
    :param commit_number: commit number
    :param reset_type: soft reset or hard reset 
    :return: None 
    '''
    assert reset_type in ['hard', 'soft']
    assert '.git' in os.listdir(repo_folder)
    run_command_sync('git config --system core.longpaths true'.split(' '))
    run_command_sync(f'git reset --{reset_type} {commit_number}'.split(' '), cwd=repo_folder)

