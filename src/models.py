from abc import ABC, abstractmethod

from src.utils import random_choice, LIST_OF_CATEGORIES, LIST_OF_LEVELS, create_and_add_word


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
    def __init__(self):
        self.users_category: str = random_choice(LIST_OF_CATEGORIES)
        self.users_level: str = random_choice(LIST_OF_LEVELS)

    def start_game(self):
        pass

    def choice_category(self, new_category):
        self.users_category = new_category

    def choice_level(self, new_level):
        self.users_level = new_level

    def add_word(self, value, category, level, hint):
        create_and_add_word(value, category, level, hint)

    def delete_word(self):
        pass
