import os

from Model.configuration import *
from Model.sysinfo import *
from Service.utils import *

class ProjectService:
    @staticmethod
    def download_runtime():
        command = 'git clone https://github.com/dotnet/runtime.git'
        outs, errs = run_command_sync(command, cwd=TestConfiguration.test_bed)
        print(outs)
        print(errs)

        command = f'git reset --soft {TestConfiguration.runtime_commit}'
        outs, errs = run_command_sync(command, cwd=TestConfiguration.runtime_root)
        print(outs)
        print(errs)

    @staticmethod
    def build_runtime():
        pass

    @staticmethod
    def download_genawaredemo():
        command = 'git clone https://github.com/cshung/blog-samples.git'
        outs, errs = run_command_sync(command, cwd=TestConfiguration.test_bed)
        print(outs)
        print(errs)

        command = f'git reset --soft {TestConfiguration.genawaredemo_commit}'
        outs, errs = run_command_sync(command, cwd=os.path.join(TestConfiguration.test_bed, 'blog-samples'))
        print(outs)
        print(errs)

    @staticmethod
    def build_genawaredemo():
        change_project_framework(TestConfiguration.genawaredemo_root, DotNetInfo.sdk_version)
        command = 'dotnet build'
        outs, errs = run_command_sync(command, cwd=TestConfiguration.genawaredemo_root)
        print(outs)
        print(errs)