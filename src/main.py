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
            if menu.options[menu.selected_index] == 'Начать игру':
                menu.start_game()
                """
                Реализовать внутренности(можно создавать объект сессии, туда закинуть все данные и продумать отрисовку)
                """
            elif menu.options[menu.selected_index] == 'Выбрать категорию':
                """
                добавить менюшку где можно выбрать одну из существующий категорий
                """
                # menu.choice_category()
            elif menu.options[menu.selected_index] == 'Выбрать сложность':
                """
                добавить менюшку где можно выбрать одну из существующий сложностей
                """
                # menu.choice_level()
            elif menu.options[menu.selected_index] == 'Добавить слово':
                """
                можно почистить экран, и чтобы через пробел/интер вводились слово, категория итд                
                """
                # menu.add_word()
            elif menu.options[menu.selected_index] == 'Удалить слово':
                menu.delete_word()
            elif menu.options[menu.selected_index] == 'Выйти':
                menu.exit_menu()
                continue
        elif key == 'up':  # Up arrow
            menu.selected_index = (menu.selected_index - 1) % len(menu.options)
        elif key == 'down':  # Down arrow
            menu.selected_index = (menu.selected_index + 1) % len(menu.options)
        elif key == 'esc' or menu.exit is True:
            break
        sleep(0.1)


if __name__ == "__main__":
    main()
