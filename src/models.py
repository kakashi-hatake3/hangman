import json
import random
from time import sleep

import keyboard

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

    def to_dict(self):
        return {
            'value': self.__value,
            'level': self.__level,
            'category': self.__category,
            'hint': self.__hint
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            data['value'],
            data['level'],
            data['category'],
            data['hint']
        )

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


class GameSession:
    def __init__(self, result_word, result_count):
        self.word: Word = result_word
        self.users_answer: str = '_' * self.word.get_length()
        self.count_of_tries: int = result_count
        self.users_count: int = result_count
        self.alphabet: str = ''.join([chr(code) for code in range(ord('а'), ord('я') + 1)])
        self.letter = ''
        self.hint = False
        self.exit = False

    def show(self):
        while not self.exit:
            clear_screen()
            self.print_hangman()
            self.print_count_of_tries()
            self.print_fields()
            self.print_word()
            self.print_hint()
            self.print_alphabet()
            self.get_hint()
            self.get_input()
            if not self.exit:
                self.get_exit()

    def end(self):
        if self.users_count == 0:
            clear_screen()
            print('Вы проиграли ;(')
            sleep(3)
            self.exit = True
        else:
            clear_screen()
            print('Вы выиграли!!!')
            sleep(3)
            self.exit = True

    def print_count_of_tries(self):
        print('Кол-во оставшихся попыток: ', self.users_count, '\n')

    def print_fields(self):
        print('Сложность: ', self.word.get_level(), '\n')
        print('Категория: ', self.word.get_category(), '\n')

    def print_word(self):
        print('Слово: ', self.users_answer + '\n')

    def print_hint(self):
        if self.hint:
            print('Подсказка: ', self.word.get_hint(), '\n')
        else:
            print('Подсказка: ___\n')

    def print_alphabet(self):
        print('Оставшиеся буквы: ', self.alphabet, '\n')

    def get_hint(self):
        if not self.hint:
            if input('Чтобы показать подсказку напишите Y: ').lower() == 'y':
                self.hint = True

    def get_exit(self):
        if input('Чтобы выйти из игры напишите "выход": ').lower() == 'выход':
            self.exit = True

    def get_input(self):
        try:
            self.letter = input('Введите букву: ').lower()
            if len(self.letter) == 1:
                if self.letter in self.alphabet:
                    self.check_answer()
                else:
                    print('Буква должна быть в алфавите')
            else:
                print('Символ должен быть длины 1')
        except ValueError:
            print('Вводите букву!')

    def check_answer(self):
        self.alphabet = self.alphabet.replace(self.letter, '_')
        if self.letter in self.word.get_value():
            indexes = [ind for ind, letter in enumerate(list(self.word.get_value())) if letter == self.letter]
            for i in indexes:
                self.users_answer = self.users_answer[:i] + self.letter + self.users_answer[i + 1:]
            if self.users_answer == self.word.get_value():
                self.end()
        else:
            self.users_count -= 1
            if self.users_count == 0:
                self.end()

    def print_hangman(self):
        stages = [
            """
                -----
                |   |
                |
                |
                |
                |
                |
            """,
            """
                -----
                |   |
                |   O
                |
                |
                |
                |
            """,
            """
                -----
                |   |
                |   O
                |   |
                |
                |
                |
            """,
            """
                -----
                |   |
                |   O
                |  /|
                |
                |
                |
            """,
            """
                -----
                |   |
                |   O
                |  /|\\
                |
                |
                |
            """,
            """
                -----
                |   |
                |   O
                |  /|\\
                |  /
                |
                |
            """,
            """
                -----
                |   |
                |   O
                |  /|\\
                |  / \\
                |
                |
            """,
            """
                -----
                |   |
                |   O
                |  /|\\
                |   |
                |  / \\
                |
                |
            """,
            """
                -----
                |   |
                |   O
                |  /|\\
                |   |
                |   |
                |  / \\
                |
                |
            """,
            """
                -----
                |   |
                |   O
                |  /|\\
                |   |
                |   |
                |   |
                |  / \\
                |
                |
            """,
            """
                -----
                |   |
                |   O
                |  /|\\
                |   |
                |   |
                |   |
                |   |
                |  / \\
                |
                |
            """
        ]
        print(stages[self.count_of_tries - self.users_count] + '\n')



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
                     'Зарандомить'
                     'Выбрать категорию',
                     'Выбрать сложность',
                     'Выбрать количество попыток',
                     'Добавить слово',
                     'Удалить слово',
                     'Выйти']
    LIST_OF_WORDS = []
    LIST_OF_CATEGORIES = []
    LIST_OF_LEVELS = []

    def __init__(self, filename: str = 'word_list.json'):
        self.users_category: str
        self.users_level: str
        self.users_count: int
        self.choice_category_flag: bool = False
        self.choice_level_flag: bool = False
        self.choice_count_flag: bool = False
        self.filename = filename

    def start_game(self):
        self.random_fields()
        filtered_words = self.filter_words()
        result_word = random.choice(filtered_words)
        return result_word, self.users_count

    def filter_words(self):
        return [word
                for word in self.LIST_OF_WORDS
                if word.get_category() == self.users_category and
                word.get_level() == self.users_level]

    def choice_category(self, new_category):
        self.users_category = new_category
        self.choice_category_flag = True

    def choice_level(self, new_level):
        self.users_level = new_level
        self.choice_level_flag = True

    def choice_count_of_tries(self, new_count):
        self.users_count = new_count
        self.choice_count_flag = True

    def add_word(self):
        clear_screen()
        print("Введите: слово, уровень сложности, категорию для этого слова, подсказку."
              " Разделяя ', '. Для того чтобы вернуться нажмите 'enter+esc'\n")
        sleep(0.15)
        while True:
            args = input().split(', ')
            if len(args) == 4 and args[0] not in [word.get_value() for word in self.LIST_OF_WORDS]:
                self.create_and_add_word(args[0], args[1], args[2], args[3])
                break
            else:
                print('Вы где-то допустили ошибку!\n')
                if keyboard.is_pressed('esc'):
                    break

    def delete_word(self, value):
        self.LIST_OF_WORDS = [word for word in self.LIST_OF_WORDS if word.get_value() != value]
        self.save_words()

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
        self.save_words()

    def save_words(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump([word.to_dict() for word in self.LIST_OF_WORDS], f, ensure_ascii=False, indent=4)
        self.refresh_lists()

    def load_words(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                self.LIST_OF_WORDS = [Word.from_dict(data) for data in json.load(f)]
        except FileNotFoundError:
            return []

    def refresh_lists(self):
        self.LIST_OF_LEVELS = list(set([word.get_level() for word in self.LIST_OF_WORDS]))
        self.LIST_OF_CATEGORIES = list(set([word.get_category() for word in self.LIST_OF_WORDS]))

    def random_fields(self):
        self.refresh_lists()
        while True:
            if not self.choice_category_flag:
                self.users_category = random.choice(self.LIST_OF_CATEGORIES)
            if not self.choice_level_flag:
                self.users_level = random.choice(self.LIST_OF_LEVELS)
            if not self.choice_count_flag:
                self.users_count = random.randint(6, 10)
            if len(self.filter_words()) > 0:
                break


    def reset_fields(self):
        self.choice_category_flag = False
        self.choice_level_flag = False
        self.choice_count_flag = False


class CategoryMenu(Menu):
    options: list
    def get_list_from_main_menu(self, main_menu: MainMenu):
        self.options = [word.get_category()
                        for word in main_menu.LIST_OF_WORDS
                        if word.get_level() == main_menu.users_level]


class LevelMenu(Menu):
    options: list
    def get_list_from_main_menu(self, main_menu: MainMenu):
        self.options = main_menu.LIST_OF_LEVELS


class DeleteMenu(Menu):
    options: list

    def get_list_from_main_menu(self, main_menu: MainMenu):
        self.options = [word.get_value() for word in main_menu.LIST_OF_WORDS]
