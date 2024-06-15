import os

from tools.terminal import run_command_sync

#  git config --system core.longpaths true

def git_clone(repo: str, dest: os.PathLike) -> None:
    '''clone the repo

    :param owner: owner of the repo
    :param repo: name of repo
    :param parent_folder: where to clone the repo.
        if `dest` exists, clone runtime under `dest`
    :return: None 
    '''
    if os.path.exists(dest):
        assert os.path.isdir(dest)
        repo_name = os.path.basename(repo)
        repo_folder = os.path.join(dest, repo_name)

    else:
        repo_folder = dest
    
    command = ['git', 'clone', repo, repo_folder]
    command, out, err = run_command_sync(command, stdout=None, stderr=None)


def git_reset(repo_folder: os.PathLike, commit_number: str, reset_type: str='soft') -> None:
    '''reset the repo

    :param repo_folder: the root of the repo
    :param commit_number: commit number
    :param reset_type: soft reset or hard reset 
    :return: None 
    '''
    assert reset_type in ['hard', 'soft']
    assert '.git' in os.listdir(repo_folder)

    command = ['git', 'reset', f'--{reset_type}', commit_number]
    command, out, err = run_command_sync(command, stdout=None, stderr=None, cwd=repo_folder)

