import logging
import platform
from time import sleep

from unicodedata import category

from models import MainMenu
import keyboard

from models import CategoryMenu

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)


def main() -> None:
    logger.info(platform.python_version())

    menu = MainMenu()
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
                category_menu = CategoryMenu()
                category_menu.get_list_from_main_menu(menu)
                if 'Выйти' not in category_menu.options:
                    category_menu.options.append('Выйти')
                while not category_menu.exit:
                    sleep(0.1)
                    category_menu.print_menu()
                    category_key = keyboard.read_key()
                    if category_key == 'enter':
                        """
                        выбираем категорию
                        """
                        menu.choice_category(category_menu.options[category_menu.selected_index])
                        category_menu.exit_menu()
                    elif category_key == 'up':  # Up arrow
                        category_menu.selected_index = (category_menu.selected_index - 1) % len(category_menu.options)
                    elif category_key == 'down':  # Down arrow
                        category_menu.selected_index = (category_menu.selected_index + 1) % len(category_menu.options)
                    elif category_key == 'esc' or category_menu.exit is True:
                        break
                    sleep(0.1)
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
