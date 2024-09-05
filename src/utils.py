import os
import random
import sys
# import tty

import select


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def get_key(termios=None):
    if os.name == 'nt':
        import msvcrt
        return msvcrt.getch()
    else:
        def is_data():
            return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

        old_settings = termios.tcgetattr(sys.stdin)
        try:
            # tty.setcbreak(sys.stdin.fileno())
            if is_data():
                return sys.stdin.read(1)
            return None
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
