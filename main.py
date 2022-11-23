import os
import shutil
import argparse

from Model.configuration import *
from Model.sysinfo import *
from Service.configuration import ConfigurationService
from Service.sysinfo import *
from Service.app import AppService


if __name__ == '__main__':
    workdir = os.path.dirname(os.path.abspath(__file__))
    conf_file_path = os.path.join(workdir, 'config.conf')

    # init
    ConfigurationService.load_configuration_from_file(conf_file_path)
    OSInfoService.init_os_name()
    OSInfoService.init_debugger(OSInfo.os_name)

    parser = argparse.ArgumentParser()
    parser.add_argument('action',
                    choices=['download', 'run', 'clean'],
                    help='specify the action')
    args = parser.parse_args()

    if args.action == 'download': 
        # AppService.download_runtime()
        AppService.download_genawaredemo()

    if args.action == 'run': 
        AppService.run_trace_only_scenario()
        AppService.run_dump_only_scenario()
        AppService.run_trace_dump_scenario()

    if args.action == 'clean':
        if 'win' in OSInfo.os_name: home_path = os.environ['USERPROFILE']
        else: home_path = os.environ['HOME']

        to_be_removed = [
            os.path.join(home_path, '.aspnet'),
            os.path.join(home_path, '.dotnet'),
            os.path.join(home_path, '.nuget'),
            os.path.join(home_path, '.templateengine'),
            os.path.join(home_path, '.lldb'),
            os.path.join(home_path, '.lldbinit'),
            os.path.join(home_path, '.local'),
            TestConfiguration.test_bed
        ]

        print('Following files or dirs would be removed:')
        for f in to_be_removed: print(f'    {f}')
        key = input('input `y` to continue, other input will be take as a no:')
        if key != 'y': exit(0)

        for f in to_be_removed:
            if not os.path.exists(f): continue
            if os.path.isdir(f): shutil.rmtree(f)
            else: os.remove(f)
