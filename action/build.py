import os

import config
from utils.terminal import run_command_sync, run_command_async, PIPE


def build_runtime():
    print('build runtime')

    if 'win' in config.rid: 
        script_engine = 'cmd.exe'
        command = [script_engine, '/k', config.vcvars64_activation_path]
        p = run_command_async(
            command, 
            stdin=PIPE,
            cwd=config.runtime_root
        )
        p.stdin.write(b'build.cmd -c checked -s clr\n')
        p.stdin.write(b'build.cmd -c release -s libs\n')
        p.stdin.write(b'src\\tests\\build.cmd generatelayoutonly checked\n')
        p.communicate()
    else:
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
                command.split(' '),
                cwd=config.runtime_root,
                env=config.basic_env_variables
            )

def build_genawaredemo():
    print('build blog-samples')
    print(config.dotnet_bin)
    run_command_sync(
        f'{config.dotnet_bin} build'.split(' '), 
        cwd=os.path.join(config.blog_samples_root, 'GenAwareDemo'),
        env=config.basic_env_variables
    )


def build_all():
    assert os.path.exists(config.runtime_root)
    assert os.path.exists(config.blog_samples_root)
    build_runtime()
    build_genawaredemo()
