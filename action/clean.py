import os
import shutil

import config
from utils.git import git_reset


def remove_dotnet_temp() -> None:
    '''Remove dotnet temporary files and folders
    
    :return: None
    '''
    if 'win' in config.rid: home_path = os.environ['USERPROFILE']
    else: home_path = os.environ['HOME']

    to_be_removed = [
        os.path.join(home_path, '.aspnet'),
        os.path.join(home_path, '.debug'),
        os.path.join(home_path, '.dotnet'),
        os.path.join(home_path, '.nuget'),
        os.path.join(home_path, '.templateengine'),
        os.path.join(home_path, '.local')
    ]

    print('The following folders and files will be deleted if exists:')
    for f in to_be_removed: print(f)
    print('Press y or Y to continue. Press other keys to cancel.')

    response = input()
    if response.lower() != 'y': return

    for f in to_be_removed:
        if not os.path.exists(f): continue
        try:
            if os.path.isdir(f): shutil.rmtree(f)
            else: os.remove(f)
        except Exception as e:
            print(f'fail to remove {f}: {e}')


def clean_test_bed() -> None:
    '''Remove runtime, blog-samples, dotnet-dump and testresult folder
    
    :return: None
    '''
    to_be_removed = [
        config.result_bed,
        config.tool_root, 
        config.blog_samples_root,
        config.runtime_root
    ]

    print('The following folders and files will be deleted if exists:')
    for f in to_be_removed: print(f)
    print('Press y or Y to continue. Press other keys to cancel.')

    response = input()
    if response.lower() != 'y': return

    for f in to_be_removed:
        if not os.path.exists(f): continue
        try:
            if os.path.isdir(f): shutil.rmtree(f)
            else: os.remove(f)
        except Exception as e:
            print(f'fail to remove {f}: {e}')


def clean_all() -> None:
    '''clean dotnet/runtime and cshung/blog-samples

    :return: None
    '''
    remove_dotnet_temp()
    clean_test_bed()
