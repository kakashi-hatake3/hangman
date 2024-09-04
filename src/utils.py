import random

from models import Word

LIST_OF_WORDS = []
LIST_OF_CATEGORIES = []
LIST_OF_LEVELS = []


def create_and_add_word(value, level, category, hint) -> None:
    """
    Создаем объект слова и добавляем его в список
    :param value:
    :param level:
    :param category:
    :param hint:
    :return:
    """
    word = Word(value, level, category, hint)
    LIST_OF_WORDS.append(word)


def fill_lists() -> None:
    """
    Заполняем списки слов, категорий и сложностей
    :return:
    """
    create_and_add_word('лев', 'легкий', 'животные', 'король зверей')
    create_and_add_word('корова', 'средний', 'животные', 'лицо популярной шоколадки')
    create_and_add_word('капибара', 'тяжелый', 'животные', 'любит арбузы')

    create_and_add_word('монитор', 'легкий', 'компьютер', 'отображает картинку')
    create_and_add_word('ноутбук', 'средний', 'компьютер', 'портативный пк')
    create_and_add_word('кулер', 'тяжелый', 'компьтер', 'охлаждает воздух')

    create_and_add_word('велосипед', 'легкий', 'транспорт', 'имеет два колеса')
    create_and_add_word('скейт', 'средний', 'транспорт', 'связан с культурой одежды')
    create_and_add_word('гидроцикл', 'тяжелый', 'транспорт', 'движется по воде')

    add_category('легкий')
    add_category('средний')
    add_category('тяжелый')

    add_level('животные')
    add_level('компьютер')
    add_level('транспорт')


def add_category(new_category) -> None:
    LIST_OF_CATEGORIES.append(new_category)


def add_level(new_level) -> None:
    LIST_OF_LEVELS.append(new_level)


def random_choice(list_of_categories_or_levels):
    return random.choice(list_of_categories_or_levels)


create_and_add_word('slovo', 'easy', 'lingvistika', 'word na russkom')
