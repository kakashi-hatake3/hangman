import os
import time
import random


def clear_screen():
    os.system('cls')


def sleep(seconds: float):
    time.sleep(seconds)


def random_choice(lst: list):
    return random.choice(lst)


def random_int(start, end):
    return random.randint(start, end)
