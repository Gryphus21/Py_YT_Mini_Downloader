import pprint as pp
import inspect

from colorama import Fore


def debug(text, inspection_enable = False):
    frame = inspect.currentframe()
    frame = inspect.getouterframes(frame)[1]
    string = inspect.getframeinfo(frame[0]).code_context[0].strip()
    args = string[string.find('(') + 1:-1].split(',')
    
    v_name = list()
    for i in args:
        if (i.find('=') != -1):
            v_name.append(i.split('=')[1].strip())
        else:
            v_name.append(i)
    
    part = '({})'.format(v_name[0]) if inspection_enable else ''
    print(f'{Fore.YELLOW}DEBUG {part}{Fore.RESET}: {Fore.YELLOW}{text}{Fore.RESET}')

def pprint(*args):
    print(f'{Fore.YELLOW}DEBUG{Fore.RESET}:{Fore.YELLOW}')
    pp.pprint(*args)
    print(f'{Fore.RESET}')

def print_cyan(text):
    print(f'{Fore.CYAN}{text}{Fore.RESET}')

def print_green(text):
    print(f'{Fore.GREEN}{text}{Fore.RESET}')

def print_red(text):
    print(f'{Fore.RED}{text}{Fore.RESET}')