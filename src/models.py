import random
from abc import ABC, abstractmethod
from lib2to3.pgen2.grammar import opmap

from utils import clear_screen


class Word:
    def __init__(self, value='Значения нет',
                 level='Сложности нет',
                 category='Категории нет',
                 hint='Подсказки нет'):
        self.__value = value
        self.__level = level
        self.__category = category
        self.__hint = hint
        self.__length = len(self.__value)

    # def set_value(self, value):
    #     self.value = value
    #
    # def set_level(self, level):
    #     self.level = level
    #
    # def set_category(self, category):
    #     self.category = category
    #
    # def set_hint(self, hint):
    #     self.hint = hint

    def get_value(self):
        return self.__value

    def get_level(self):
        return self.__level

    def get_category(self):
        return self.__category

    def get_hint(self):
        return self.__hint

    def get_length(self):
        return self.__length


class Session:
    def __init__(self):
        self.answer: Word
        self.users_answer: str
        self.max_count: int
        self.users_count: int


class Menu:
    options: list
    exit = False
    selected_index: int = 0

    def exit_menu(self):
        self.exit = True

    def print_menu(self):
        clear_screen()
        print("Выберите опцию:")
        for i, option in enumerate(self.options):
            if i == self.selected_index:
                print(f"> {option}")
            else:
                print(f"  {option}")

    def handle_key(self, key):
        if key == 'enter':
            return 'enter'
        elif key == 'up':  # Up arrow
            self.selected_index = (self.selected_index - 1) % len(self.options)
        elif key == 'down':  # Down arrow
            self.selected_index = (self.selected_index + 1) % len(self.options)
        elif key == 'esc':
            self.exit = True
        return None


class MainMenu(Menu):
    options: list = ['Начать игру',
                     'Выбрать категорию',
                     'Выбрать сложность',
                     'Добавить слово',
                     'Удалить слово',
                     'Выйти']
    # selected_index: int = 0
    LIST_OF_WORDS = []
    LIST_OF_CATEGORIES = []
    LIST_OF_LEVELS = []
    # exit = False

    def __init__(self):
        self.users_category: str
        self.users_level: str

    def start_game(self):
        pass

    def choice_category(self, new_category):
        self.users_category = new_category

    def choice_level(self, new_level):
        self.users_level = new_level

    def add_word(self, value, category, level, hint):
        self.create_and_add_word(value, category, level, hint)

    def delete_word(self):
        pass

    # def exit_menu(self):
    #     self.exit = True
    #
    # def print_menu(self):
    #     clear_screen()
    #     print("Выберите опцию:")
    #     for i, option in enumerate(self.options):
    #         if i == self.selected_index:
    #             print(f"> {option}")
    #         else:
    #             print(f"  {option}")

    def create_and_add_word(self, value, level, category, hint) -> None:
        """
        Создаем объект слова и добавляем его в список
        :param value:
        :param level:
        :param category:
        :param hint:
        :return:
        """
        word = Word(value, level, category, hint)
        self.LIST_OF_WORDS.append(word)
        self.add_level(level)
        self.add_category(category)

    def add_category(self, new_category) -> None:
        if new_category not in self.LIST_OF_CATEGORIES:
            self.LIST_OF_CATEGORIES.append(new_category)

    def add_level(self, new_level) -> None:
        if new_level not in self.LIST_OF_LEVELS:
            self.LIST_OF_LEVELS.append(new_level)

    def fill_lists(self) -> None:
        """
        Заполняем списки слов, категорий и сложностей
        :return:
        """
        self.create_and_add_word('лев', 'легкий', 'животные', 'король зверей')
        self.create_and_add_word('корова', 'средний', 'животные', 'лицо популярной шоколадки')
        self.create_and_add_word('капибара', 'тяжелый', 'животные', 'любит арбузы')

        self.create_and_add_word('монитор', 'легкий', 'компьютер', 'отображает картинку')
        self.create_and_add_word('ноутбук', 'средний', 'компьютер', 'портативный пк')
        self.create_and_add_word('кулер', 'тяжелый', 'компьютер', 'охлаждает воздух')

        self.create_and_add_word('велосипед', 'легкий', 'транспорт', 'имеет два колеса')
        self.create_and_add_word('скейт', 'средний', 'транспорт', 'связан с культурой одежды')
        self.create_and_add_word('гидроцикл', 'тяжелый', 'транспорт', 'движется по воде')

        # self.add_category('легкий')
        # self.add_category('средний')
        # self.add_category('тяжелый')
        #
        # self.add_level('животные')
        # self.add_level('компьютер')
        # self.add_level('транспорт')

        self.users_category = random.choice(self.LIST_OF_CATEGORIES)
        self.users_level = random.choice(self.LIST_OF_LEVELS)


class CategoryMenu(Menu):
    options: list
    def get_list_from_main_menu(self, main_menu: MainMenu):
        self.options = main_menu.LIST_OF_CATEGORIES


class LevelMenu(Menu):
    options: list
    def get_list_from_main_menu(self, main_menu: MainMenu):
        self.options = main_menu.LIST_OF_LEVELS
