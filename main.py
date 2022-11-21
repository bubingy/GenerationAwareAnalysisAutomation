import os

from Model import Configuration
from test import RunTest

workdir = os.path.dirname(os.path.abspath(__file__))
conf_file_path = os.path.join(workdir, 'config.conf')

Configuration.load_configuration_from_file(conf_file_path)
RunTest.run_dump_only_scenario()
RunTest.run_trace_only_scenario()
RunTest.run_trace_dump_scenario()
