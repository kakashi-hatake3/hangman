import logging
import platform

from src.models import Menu
from src.utils import get_key

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)


def main() -> None:
    logger.info(platform.python_version())

    menu = Menu()
    menu.fill_lists()
    while True:
        menu.print_menu()
        key = get_key()
        if key:
            if ord(key) == 13:  # Enter key
                return menu.options[menu.selected_index]
            elif ord(key) == 65 or ord(key) == 72:  # Up arrow
                menu.selected_index = (menu.selected_index - 1) % len(menu.options)
            elif ord(key) == 66 or ord(key) == 80:  # Down arrow
                menu.selected_index = (menu.selected_index + 1) % len(menu.options)


if __name__ == "__main__":
    main()
