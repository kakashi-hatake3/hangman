import logging
import platform
from time import sleep

from models import Menu
import keyboard

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)


def main() -> None:
    logger.info(platform.python_version())

    menu = Menu()
    menu.fill_lists()
    while True:
        menu.print_menu()
        key = keyboard.read_key()
        if key == 'enter':  # Enter key
            print(menu.options[menu.selected_index])
        elif key == 'up':  # Up arrow
            menu.selected_index = (menu.selected_index - 1) % len(menu.options)
        elif key == 'down':  # Down arrow
            menu.selected_index = (menu.selected_index + 1) % len(menu.options)
        sleep(0.1)


if __name__ == "__main__":
    main()
