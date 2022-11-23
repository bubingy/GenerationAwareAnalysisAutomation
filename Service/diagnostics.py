from subprocess import Popen, PIPE

from Model.configuration import *

class DiagToolService:
    @classmethod
    def insatll_dotnet_sos():
        command = ' '.join(
            [
                f'dotnet tool install dotnet-sos',
                f'--tool-path {DiagnosticsConfiguration.root}',
                f'--version {DiagnosticsConfiguration.version}',
                f'--add-source {DiagnosticsConfiguration.feed}'
            ]
        ).split(' ')

        p = Popen(command, stdin=PIPE, stdout=PIPE)
        outs, errs = p.communicate()
        
        print(outs.decode())
        print(errs.decode())