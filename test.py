import os
import glob
import time
from subprocess import Popen, PIPE

from Model import Configuration

class RunTest:
    command = ''

    @classmethod
    def __init_command(cls):
        corerun = ''
        corerun_candidates = glob.glob(
            os.path.join(
                Configuration.runtime_root, 'artifacts', 'tests',
                'coreclr', '*', 'Tests', 'Core_Root', 'corerun*'
            )
        )
        if len(corerun_candidates) == 0: return
        corerun = corerun_candidates[0]

        genawaredemo = ''
        genawaredemo_candidates = glob.glob(
            os.path.join(
                Configuration.genawaredemo_root, 
                'bin', 'Debug', '*', 'GenAwareDemo.dll'
            )
        )
        if len(genawaredemo_candidates) == 0: return
        genawaredemo = genawaredemo_candidates[0]

        cls.command = f'{corerun} {genawaredemo}'.split(' ')

    @classmethod
    def run_app(cls, test_result_root: str, scenario_env: list):
        cls.__init_command()
        if len(cls.command) < 2: Exception(f'invalid command: {cls.command}')
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
        if not os.path.exists(test_result_root): os.makedirs(test_result_root)
        scenario_env = os.environ.copy()
        scenario_env['COMPlus_GCGenAnalysisDump'] = '0'
        scenario_env['COMPlus_GCGenAnalysisTrace'] = '1'

        cls.run_app(test_result_root, scenario_env)

    @classmethod
    def run_dump_only_scenario(cls):
        print('run dump only scenario')
        test_result_root = os.path.join(Configuration.test_bed, 'DumpOnly')
        if not os.path.exists(test_result_root): os.makedirs(test_result_root)
        scenario_env = os.environ.copy()
        scenario_env['COMPlus_GCGenAnalysisDump'] = '1'
        scenario_env['COMPlus_GCGenAnalysisTrace'] = '0'

        cls.run_app(test_result_root, scenario_env)

    @classmethod
    def run_trace_dump_scenario(cls):
        print('run dump and trace scenario')
        test_result_root = os.path.join(Configuration.test_bed, 'TraceDump')
        if not os.path.exists(test_result_root): os.makedirs(test_result_root)
        scenario_env = os.environ.copy()
        scenario_env['COMPlus_GCGenAnalysisDump'] = '1'
        scenario_env['COMPlus_GCGenAnalysisTrace'] = '1'

        cls.run_app(test_result_root, scenario_env)