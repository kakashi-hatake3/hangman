import logging
import platform
from time import sleep

from models import MainMenu
import keyboard

from models import CategoryMenu, LevelMenu

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)


def main() -> None:
    logger.info(platform.python_version())

    menu = MainMenu()
    menu.load_words()
    menu.random_fields()
    while not menu.exit:
        menu.print_menu()
        key = keyboard.read_key()
        if menu.handle_key(key) == 'enter':
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
                    sleep(0.15)
                    category_menu.print_menu()
                    category_key = keyboard.read_key()
                    if category_menu.handle_key(category_key) == 'enter':
                        """
                        выбираем категорию
                        """
                        menu.choice_category(category_menu.options[category_menu.selected_index])
                        category_menu.exit_menu()
                    sleep(0.15)

            elif menu.options[menu.selected_index] == 'Выбрать сложность':
                level_menu = LevelMenu()
                level_menu.get_list_from_main_menu(menu)
                if 'Выйти' not in level_menu.options:
                    level_menu.options.append('Выйти')
                while not level_menu.exit:
                    sleep(0.15)
                    level_menu.print_menu()
                    category_key = keyboard.read_key()
                    if level_menu.handle_key(category_key) == 'enter':
                        """
                        выбираем уровень
                        """
                        menu.choice_level(level_menu.options[level_menu.selected_index])
                        level_menu.exit_menu()
                    sleep(0.15)

            elif menu.options[menu.selected_index] == 'Добавить слово':
                """
                Добавляем слово               
                """

                menu.add_word()

            elif menu.options[menu.selected_index] == 'Удалить слово':
                menu.delete_word()

            elif menu.options[menu.selected_index] == 'Выйти':
                menu.exit_menu()
                break
        sleep(0.15)


if __name__ == "__main__":
    main()
