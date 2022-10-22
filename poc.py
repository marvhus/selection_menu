import os
from colorama import Fore

# https://stackoverflow.com/a/40492207
class _Getch:
    """
    Gets a single character from standard input.
    Does not echo to the screen.
    """
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()
    def __call__(self): return self.impl()

class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()

class Menu:
    # Initialize stuff
    def __init__(self):
        self.selection = 0
        self.getch = _Getch()
        self.keybinds = {
            'w': {'callback': self.select_up,      'name': 'select up'},
            's': {'callback': self.select_down,    'name': 'select down'},
            ' ': {'callback': self.make_selection, 'name': 'make selection'},
            'q': {'callback': self.exit_menu,      'name': 'exit'},
        }
        self.actions = {
            0: {'callback': self.option_1, 'name': 'option 1'},
            1: {'callback': self.option_2, 'name': 'option 2'},
            2: {'callback': self.exit_menu, 'name': 'Exit'},
        }

    # Helper
    def change_selection(self, change):
        self.selection += change
        self.selection %= len(self.actions.keys())
        self.draw()
        
    # Callbacks

    ## Selection changing
    def select_up(self):
        self.change_selection(-1)
        
    def select_down(self):
        self.change_selection(+1)
        
    def make_selection(self):
        if self.selection in self.actions.keys():
            self.actions[self.selection]['callback']()

    ## Selection actions
    def option_1(self):
        print(f'{Fore.GREEN}ACTION: {Fore.WHITE}option_1')

    def option_2(self):
        print(f'{Fore.GREEN}ACTION: {Fore.WHITE}option_2')

    def exit_menu(self):
        print(f'{Fore.RED}Exiting{Fore.WHITE}')
        exit(0)
            
    # Call callback
    def use_keybind(self):
        if self.char in self.keybinds:
            self.keybinds[self.char]['callback']()
        #else:
            #print(f'Unknown keybind "{self.char}"')

    # Draw menu
    def draw(self):
        # clear
        os.system('cls' if os.name == 'nt' else 'clear')
        #print('\033[H')
        print(f'{Fore.YELLOW}####### KEYBINDS #######{Fore.WHITE}')
        for k, v in self.keybinds.items():
            print(
                f'{Fore.YELLOW}###'
            ,   f'"{Fore.MAGENTA}{k}{Fore.WHITE}"'
            ,   f'{Fore.GREEN}---'
            ,   f'{Fore.BLUE}{v["name"]}{Fore.WHITE}'
            )
        print(f'{Fore.YELLOW}######### MENU #########{Fore.WHITE}')
        for k, v in self.actions.items():
            selected = f"{Fore.GREEN}x" if self.selection == k else " "
            print(
                f'{Fore.YELLOW}###'
            ,   f'{Fore.CYAN}[{selected}{Fore.CYAN}]'
            ,   f'{Fore.GREEN}---'
            ,   f'{Fore.BLUE}{v["name"]}{Fore.WHITE}'
            )
        print(f'{Fore.YELLOW}########################{Fore.WHITE}')

    # Start menu
    def start(self):
        self.draw()
        self.char = ''
        while self.char != 'q':
            self.char = self.getch()
            self.use_keybind()
        
Menu().start()
