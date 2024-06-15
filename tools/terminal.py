'''wrappers for Popen'''

from subprocess import Popen, PIPE
from typing import Union, Iterable, Tuple

import app


def log_terminal_command():
    def decorator(func: callable):
        def wrapper(*args, **kwargs):
            if func.__name__ == 'run_command_sync':
                command, stdout, stderr = func(*args, **kwargs)
                if stdout is None:
                    out = ''
                else:
                    out = stdout
                if stderr is None:
                    err = ''
                else:
                    err = stderr
                if app.logger is not None:
                    app.logger.info(
                        '\n'.join(
                            [
                                f'run command: {command}',
                                out,
                                err
                            ]
                        )
                    )
                return command, stdout, stderr
            elif func.__name__ == 'run_command_async':
                command, p = func(*args, **kwargs)
                if app.logger is not None:
                    app.logger.info(f'run command: {command}')
                return command, p
            else:
                return Exception('not a valid command call')
        return wrapper
    return decorator


@log_terminal_command()
def run_command_sync(args: Union[Iterable[str], str], stdout=PIPE, stderr=PIPE, **kwargs) -> Tuple[str, str, str]:
    '''Run command and wait for the process to be terminated.

    :param command: sequence of program arguments
    :return: tuple of stdout and stderr
    '''
    # shell not set case
    if 'shell' not in kwargs.keys():
        assert isinstance(args, list)
    # shell is set case
    else:
        if kwargs['shell'] is False:
            assert isinstance(args, list[str])
        else:
            assert isinstance(args, str)

    command = ' '.join(args)
    print(f'run command: {command}')
    p = Popen(args, stdout=stdout, stderr=stderr, **kwargs)
    stdout, stderr = p.communicate()

    if stdout is not None:
        out = stdout.decode()
        print(out)
    else:
        out = None
    if stderr is not None:
        err = stderr.decode()
        print(err)
    else:
        err = None
    '''
    # not safe
    while p.poll() is None:
        if p.stdout is None:
            time.sleep(1)
            continue
        output = p.stdout.readline().decode().strip()
        if output != '':
            print(output)
            stdout += f'{output}\n'

        if p.stderr is None:
            time.sleep(1)
            continue
        error = p.stderr.readline().decode().strip()
        if error != '':
            print(error)
            stderr += f'{error}\n'
    '''
    return command, out, err


@log_terminal_command()
def run_command_async(args: Iterable[str], **kwargs) -> Tuple[str, Popen]:
    '''Run command and and return the process object without waiting for the process to be terminated.

    :param command: sequence of program arguments
    :return: Popen object
    '''
    command = ' '.join(args)
    # shell must be False 
    if 'shell' in  kwargs.keys():
        kwargs.pop('shell')
    print(f'run command: {command}:')
    p = Popen(args, **kwargs)
    return command, p
