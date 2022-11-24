import os
import time
import glob
import shutil
import zipfile
from urllib import request
from subprocess import Popen, PIPE

from Model.configuration import *

class AppService:
    command = ''
    @classmethod
    def download_github_repo(cls, owner: str, repo: str, ref: str='') -> None:
        BUFFERSIZE = 64*1024*1024
        download_link = f'https://api.github.com/repos/{owner}/{repo}/zipball/{ref}'
        print(f'downloading {owner}/{repo} from github')
        try:
            response = request.urlopen(
                request.Request(
                    download_link
                )
            )
            compressed_file_path = os.path.join(
                TestConfiguration.test_bed,
                f'{repo}.zip'
            )
            with open(compressed_file_path, 'wb+') as fs:
                while True:
                    buffer = response.read(BUFFERSIZE)
                    if buffer == b'' or len(buffer) == 0: break
                    fs.write(buffer)
        except Exception as e:
            ex_message = f'fail to download {repo} from github: {e}'
            print(ex_message)
            if os.path.exists(compressed_file_path): os.remove(compressed_file_path)
            raise Exception(ex_message)

        print(f'decompressing downloaded {repo}')
        decompressed_file_path = os.path.join(
            TestConfiguration.test_bed,
            f'{repo}-temp'
        )
        try:
            with zipfile.ZipFile(compressed_file_path, 'r') as zip_ref:
                zip_ref.extractall(decompressed_file_path)
            real_root = glob.glob(os.path.join(decompressed_file_path, '*'))[0]
            os.rename(
                real_root, 
                os.path.join(TestConfiguration.test_bed, repo)
            )
        except Exception as e:
            ex_message = f'fail to decompress downloaded {repo}: {e}'
            print(ex_message)
            if os.path.exists(decompressed_file_path): shutil.rmtree(decompressed_file_path)
            raise Exception(ex_message)
        finally:
            os.remove(compressed_file_path)
            shutil.rmtree(decompressed_file_path)


    @classmethod
    def download_runtime(cls, ):
        cls.download_github_repo('dotnet', 'runtime', RuntimeConfiguration.commit)

    
    @classmethod
    def download_genawaredemo(cls, ):
        cls.download_github_repo('cshung', 'blog-samples', GenAwareDemoConfiguration.commit)


    @classmethod
    def __init_command(cls):
        corerun = ''
        corerun_candidates = glob.glob(
            os.path.join(
                RuntimeConfiguration.root, 'artifacts', 'tests',
                'coreclr', '*', 'Tests', 'Core_Root', 'corerun*'
            )
        )
        if len(corerun_candidates) == 0: return
        corerun = corerun_candidates[0]

        genawaredemo = ''
        genawaredemo_candidates = glob.glob(
            os.path.join(
                GenAwareDemoConfiguration.root, 
                'bin', 'Debug', '*', 'GenAwareDemo.dll'
            )
        )
        if len(genawaredemo_candidates) == 0: return
        genawaredemo = genawaredemo_candidates[0]

        os.environ['COMPlus_GCGenAnalysisGen'] = '1'
        os.environ['COMPlus_GCGenAnalysisBytes'] = '16E360'
        cls.command = f'{corerun} {genawaredemo}'.split(' ')


    @classmethod
    def run_app(cls, test_result_root: str, scenario_env: list):
        cls.__init_command()
        if len(cls.command) < 2: Exception(f'invalid command: {cls.command}')
        tmp_file_path = os.path.join(test_result_root, 'tmp.txt')
        if os.path.exists(tmp_file_path): os.remove(tmp_file_path)

        tmp_fp = open(tmp_file_path, 'w+')
        
        p = Popen(cls.command, stdin=PIPE, stdout=tmp_fp, cwd=test_result_root, env=scenario_env)
        while True:
            with open(tmp_file_path, 'r') as tmp_reader:
                if 'My process id is' in tmp_reader.read(): 
                    break
            time.sleep(1)

        p.stdin.write(b'123\n')
        p.communicate()
        
    
    @classmethod
    def run_trace_only_scenario(cls):
        print('run trace only scenario')
        test_result_root = os.path.join(TestConfiguration.test_bed, 'TraceOnly')
        if not os.path.exists(test_result_root): os.makedirs(test_result_root)
        scenario_env = os.environ.copy()
        scenario_env['COMPlus_GCGenAnalysisDump'] = '0'
        scenario_env['COMPlus_GCGenAnalysisTrace'] = '1'

        cls.run_app(test_result_root, scenario_env)
        return test_result_root


    @classmethod
    def run_dump_only_scenario(cls):
        print('run dump only scenario')
        test_result_root = os.path.join(TestConfiguration.test_bed, 'DumpOnly')
        if not os.path.exists(test_result_root): os.makedirs(test_result_root)
        scenario_env = os.environ.copy()
        scenario_env['COMPlus_GCGenAnalysisDump'] = '1'
        scenario_env['COMPlus_GCGenAnalysisTrace'] = '0'

        cls.run_app(test_result_root, scenario_env)
        return test_result_root


    @classmethod
    def run_trace_dump_scenario(cls):
        print('run dump and trace scenario')
        test_result_root = os.path.join(TestConfiguration.test_bed, 'TraceDump')
        if not os.path.exists(test_result_root): os.makedirs(test_result_root)
        scenario_env = os.environ.copy()
        scenario_env['COMPlus_GCGenAnalysisDump'] = '1'
        scenario_env['COMPlus_GCGenAnalysisTrace'] = '1'

        cls.run_app(test_result_root, scenario_env)
        return test_result_root
