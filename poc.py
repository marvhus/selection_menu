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
            'w': self.select_up,
            's': self.select_down,
            ' ': self.make_selection,
        }
        self.actions = {
            0: self.option_1,
            1: self.option_2,
        }

    # Helper
    def change_selection(self, change):
        self.selection += change
        self.selection %= len(self.actions.keys())
        print(self.selection)
        
    # Callbacks

    ## Selection changing
    def select_up(self):
        self.change_selection(1)
        
    def select_down(self):
        self.change_selection(-1)
        
    def make_selection(self):
        if self.selection in self.actions.keys():
            self.actions[self.selection]()

    ## Selection actions
    def option_1(self):
        print('ACTION: option_1')

    def option_2(self):
        print('ACTION* option_2')
            
    # Call callback
    def use_keybind(self):
        if self.char in self.keybinds:
            self.keybinds[self.char]()
        else:
            print(f'Unknown keybind "{self.char}"')
        
    def start(self):
        self.char = self.getch()
        while self.char != 'q':
            self.char = self.getch()
            self.use_keybind()
                
        
Menu().start()
