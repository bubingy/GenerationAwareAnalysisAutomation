from subprocess import Popen


def run_command_sync(command: str, **kwargs) -> None:
    '''run command and wait for return
    
    :param command: command to run
    :param kwargs: see Popen kwargs for details
    :return: None
    '''
    if 'shell' in kwargs.keys() and kwargs['shell'] == True:
        arg = command
    else:
        arg = command.split(' ')
    print(command)
    p = Popen(arg, **kwargs)
    p.communicate()


def run_command_async(command: str, **kwargs) -> Popen:
    '''run command but not wait for return
    
    :param command: command to run
    :param kwargs: see Popen kwargs for details
    :return: None
    '''
    if 'shell' in kwargs.keys() and kwargs['shell'] == True:
        arg = command
    else:
        arg = command.split(' ')
    print(command)
    return Popen(arg, **kwargs)