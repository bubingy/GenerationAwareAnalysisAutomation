import os
import time
from subprocess import Popen, PIPE

from configuration import Configuration

class RunTest:
    command = ''

    @classmethod
    def init_command(cls):
        # TODO: use regular expression
        platform_id = list(
            filter(
                lambda dir_name: 'Checked' in dir_name,
                os.listdir(os.path.join(
                    Configuration.runtime_root, 'artifacts', 'tests', 'coreclr')
                )
            )
        )[0]
        corerun = os.path.join(
            Configuration.runtime_root, 'artifacts', 'tests', 'coreclr', 
            platform_id, 'Tests', 'Core_Root', 'corerun'
        )

        dotnet_id = os.listdir(os.path.join(
                Configuration.genawaredemo_root, 
                'bin', 'Debug')
        )[0]
        genawaredemo = os.path.join(
            Configuration.genawaredemo_root, 
            'bin', 'Debug', dotnet_id, 'GenAwareDemo.dll'
        )

        cls.command = f'{corerun} {genawaredemo}'.split(' ')

    @classmethod
    def run_command(cls, test_result_root: str, scenario_env: list):
        tmp_file_path = os.path.join(test_result_root, 'tmp.txt')
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
        test_result_root = os.path.join(Configuration.test_bed, 'TraceOnly')
        if not os.path.exists(test_result_root): os.mkdir(test_result_root)
        scenario_env = os.environ.copy()
        scenario_env['COMPlus_GCGenAnalysisDump'] = '0'
        scenario_env['COMPlus_GCGenAnalysisTrace'] = '1'

        cls.run_command(test_result_root, scenario_env)

    @classmethod
    def run_dump_only_scenario(cls):
        print('run dump only scenario')
        test_result_root = os.path.join(Configuration.test_bed, 'DumpOnly')
        if not os.path.exists(test_result_root): os.mkdir(test_result_root)
        scenario_env = os.environ.copy()
        scenario_env['COMPlus_GCGenAnalysisDump'] = '1'
        scenario_env['COMPlus_GCGenAnalysisTrace'] = '0'

        cls.run_command(test_result_root, scenario_env)

    @classmethod
    def run_trace_dump_scenario(cls):
        print('run dump and trace scenario')
        test_result_root = os.path.join(Configuration.test_bed, 'TraceDump')
        if not os.path.exists(test_result_root): os.mkdir(test_result_root)
        scenario_env = os.environ.copy()
        scenario_env['COMPlus_GCGenAnalysisDump'] = '1'
        scenario_env['COMPlus_GCGenAnalysisTrace'] = '1'

        cls.run_command(test_result_root, scenario_env)