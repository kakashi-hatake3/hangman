import logging
import platform
from time import sleep

from models import MainMenu, DeleteMenu
import keyboard

from models import CategoryMenu, LevelMenu, GameSession
from utils import clear_screen

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
        if menu.handle_key(key) == 'enter' and menu.exit is False:
            if menu.options[menu.selected_index] == 'Начать игру':
                result_word, count_of_tries = menu.start_game()
                game_session = GameSession(
                    result_word,
                    count_of_tries
                )
                menu.random_fields()
                game_session.show()
                menu.reset_fields()
                """
                Реализовать внутренности(можно создавать объект сессии, туда закинуть все данные и продумать отрисовку)
                """

            elif menu.options[menu.selected_index] == 'Зарандомить':
                """
                выбирает случайные сложность, категорию и количесвто попыток
                """
                menu.reset_fields()
                menu.random_fields()

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
                        if category_menu.options[category_menu.selected_index] != 'Выйти':
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
                    level_key = keyboard.read_key()
                    if level_menu.handle_key(level_key) == 'enter':
                        """
                        выбираем уровень
                        """
                        if level_menu.options[level_menu.selected_index] != 'Выйти':
                            menu.choice_level(level_menu.options[level_menu.selected_index])
                        level_menu.exit_menu()
                    sleep(0.15)

            elif menu.options[menu.selected_index] == 'Выбрать количество попыток':
                clear_screen()
                print('Введите число попыток от 6 до 10, чтобы вернуться нажмите "enter+esc"\n')
                sleep(0.15)
                while True:
                    try:
                        new_count = int(input())
                        if 6 <= new_count <= 10:
                            menu.choice_count_of_tries(new_count)
                            break
                        else:
                            print('Число должно быть от 6 до 10!\n')
                    except ValueError:
                        print('Вводите число!\n')
                        if keyboard.is_pressed('esc'):
                            break

            elif menu.options[menu.selected_index] == 'Добавить слово':
                """
                добавляем слово               
                """

                menu.add_word()

            elif menu.options[menu.selected_index] == 'Удалить слово':
                delete_menu = DeleteMenu()
                delete_menu.get_list_from_main_menu(menu)
                if 'Выйти' not in delete_menu.options:
                    delete_menu.options.append('Выйти')
                while not delete_menu.exit:
                    sleep(0.15)
                    delete_menu.print_menu()
                    delete_key = keyboard.read_key()
                    if delete_menu.handle_key(delete_key) == 'enter':
                        """
                        выбираем слово для удаления
                        """
                        menu.delete_word(delete_menu.options[delete_menu.selected_index])
                        delete_menu.exit_menu()
                    sleep(0.15)

            elif menu.options[menu.selected_index] == 'Выйти':
                menu.exit_menu()
                break
        sleep(0.15)


if __name__ == "__main__":
    main()
