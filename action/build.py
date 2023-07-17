import os

import config
from utils.terminal import run_command_sync


def build_runtime():
    print('build runtime')
    if 'win' in config.rid: 
        print('run build command in x64 Native Tools Command Prompt manually')
        return
    
    if 'osx' in config.rid:
        script_engine = '/bin/zsh'
    else:
        script_engine = '/bin/bash'

    command_list = [
        f'{script_engine} ./build.sh -c checked -s clr',
        f'{script_engine} ./build.sh -c release -s libs',
        f'{script_engine} ./src/tests/build.sh generatelayoutonly checked',
    ]

    for command in command_list:
        print(f'run command {command}')
        run_command_sync(
            command,
            cwd=config.runtime_root,
            env=config.basic_env_variables
        )

def build_genawaredemo():
    print('build blog-samples')
    run_command_sync(
        'dotnet build', 
        cwd=os.path.join(config.blog_samples_root, 'GenAwareDemo'),
        env=config.basic_env_variables
    )


def build_all():
    assert os.path.exists(config.runtime_root)
    assert os.path.exists(config.blog_samples_root)
    build_runtime()
    build_genawaredemo()
