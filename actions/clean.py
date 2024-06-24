import os
import shutil

from configuration import GenerationAwareAnalyzeConfiguration
from tools.sysinfo import SysInfo
from tools import dotnet_app


def remove_dotnet_temp(test_conf: GenerationAwareAnalyzeConfiguration) -> None:
    '''Remove dotnet temporary files and folders
    
    :return: None
    '''
    temp_files_collection_root = os.path.join(
        test_conf.test_bed,
        'temp_files_folders'
    )

    if 'win' in SysInfo.rid:
        home_path = os.environ['USERPROFILE']
    else:
        home_path = os.environ['HOME']

    to_be_removed = [
        os.path.join(home_path, '.aspnet'),
        os.path.join(home_path, '.debug'),
        os.path.join(home_path, '.dotnet'),
        os.path.join(home_path, '.nuget'),
        os.path.join(home_path, '.templateengine'),
        os.path.join(home_path, '.local')
    ]
    for f in to_be_removed:
        if not os.path.exists(f):
            continue
        try:
            shutil.move(f, temp_files_collection_root)
        except Exception as e:
            print(f'fail to remove {f}: {e}')


def remove_registry_keys(test_conf: GenerationAwareAnalyzeConfiguration):
    core_root = dotnet_app.get_core_root(test_conf.runtime_root)
    # set registry keys
    if 'win' not in SysInfo.rid:
        return
    
    import winreg
    with winreg.OpenKeyEx(
        winreg.HKEY_LOCAL_MACHINE, 
        r'SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\KnownManagedDebuggingDlls',
        0,
        winreg.KEY_ALL_ACCESS
    ) as debug_dll:
        winreg.DeleteKeyEx(
            debug_dll,
            os.path.join(core_root, 'mscordaccore.dll'),
            winreg.KEY_ALL_ACCESS,
            0
        )

    with winreg.OpenKeyEx(
        winreg.HKEY_LOCAL_MACHINE, 
        r'SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\MiniDumpAuxiliaryDlls',
        0,
        winreg.KEY_ALL_ACCESS
    ) as auxiliary_dll:
        winreg.DeleteKeyEx(
            auxiliary_dll,
            os.path.join(core_root, 'coreclr.dll'),
            winreg.KEY_ALL_ACCESS,
            0
        )  