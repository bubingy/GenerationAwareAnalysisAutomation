import re
import os
import glob
import platform
from xml.etree import ElementTree as ET
from subprocess import Popen, PIPE


def get_os_name():
    system = platform.system().lower()
    if system == 'windows':
        os = 'win'
    elif system == 'linux':
        release_files = glob.glob('/etc/*release')
        content = ''
        for release_file in release_files:
            with open(release_file, 'r') as f:
                content += f.read().lower()
        if 'alpine' in content:
            os = 'linux-musl'
        else:
            os = 'linux'
    elif system== 'darwin':
        os = 'osx'
    else:
        raise Exception(f'unsupported OS: {system}')
    return os


def get_debugger(os: str):
    if 'musl' in os:
        return ''
    elif 'win' in os:
        debugger = 'cdb'
        return debugger
    else: # linux or osx
        candidate_debuggers = glob.glob('/usr/bin/lldb*')
        if '/usr/bin/lldb' in candidate_debuggers:
            debugger = 'lldb'
            return debugger
        else:
            pattern = re.compile(r'/usr/bin/lldb-\d+')
            for candidate_debugger in candidate_debuggers:
                if pattern.match(candidate_debugger) is not None:
                    debugger = candidate_debugger.split('/')[-1]
                    return debugger


def change_project_framework(project_dir: os.PathLike, dotnet_sdk_version: str):
    project_file = glob.glob(f'{project_dir}/*.csproj')[0]
    tree = ET.parse(project_file)
    root = tree.getroot()
    if dotnet_sdk_version[0] == '3':
        framework = 'netcoreapp' + dotnet_sdk_version[0][:3]
    else:
        framework = 'net' + dotnet_sdk_version[0][:3]

    lang_version_element = ET.Element("LangVersion")
    lang_version_element.text = "latest"

    root.find('PropertyGroup').append(lang_version_element)
    root.find('PropertyGroup').find('TargetFramework').text = framework
    tree.write(project_file)


def run_command_sync(command, stdin=None, stdout=PIPE, stderr=PIPE, cwd=None, **kwargs)->tuple:
    print(command)
    args = command.split(' ')
    try:
        p = Popen(args, stdin=stdin,
            stdout=stdout, stderr=stderr, cwd=cwd, **kwargs)
        outs, errs = p.communicate()
        outs = outs.decode()
        errs = errs.decode()
    except Exception as e:
        outs, errs = '', e
    return outs, errs
    

def run_command_async(command: str, stdin=None, stdout=None, stderr=None, cwd=None, **kwargs)->Popen:
    print(command)
    args = command.split(' ')
    p = Popen(args, stdin=stdin,
        stdout=stdout, stderr=stderr, cwd=cwd, **kwargs)
    return p