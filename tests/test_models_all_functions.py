import json
import random
import os

from src.main_menu import MainMenu

from src.word import Word


def setup_function():
    MainMenu.LIST_OF_WORDS = []
    if os.path.exists('word_list.json'):
        os.remove('word_list.json')


def test_start_game(mocker):
    mocker.patch.object(random, 'choice', return_value="word")
    menu = MainMenu()
    menu.users_category = "category"
    menu.users_level = "level"
    menu.users_count = 7
    menu.LIST_OF_WORDS = [Word("word", "level", "category", "hint")]
    assert menu.start_game()[0] == "word"


def test_filter_words():
    menu = MainMenu()
    menu.users_category = "category"
    menu.users_level = "level"
    menu.LIST_OF_WORDS = [Word("word", "level", "category", "hint")]
    assert len(menu.filter_words()) == 1


def test_choice_category():
    menu = MainMenu()
    menu.choice_category("category")
    assert menu.choice_category_flag is True
    assert menu.users_category == "category"


def test_choice_level():
    menu = MainMenu()
    menu.users_category = "category"
    menu.LIST_OF_WORDS = [Word("word", "level", "category", "hint")]
    menu.choice_level("level")
    assert menu.choice_level_flag is True
    assert menu.users_level == "level"


def test_choice_count_of_tries():
    menu = MainMenu()
    menu.choice_count_of_tries(3)
    assert menu.choice_count_flag is True
    assert menu.users_count == 3


def test_add_word(mocker):
    mocker.patch('builtins.input', return_value="word, level, category, hint")
    menu = MainMenu()
    menu.add_word()
    assert len(menu.LIST_OF_WORDS) == 1
    assert menu.LIST_OF_WORDS[0].value == "word"
    assert menu.LIST_OF_WORDS[0].level == "level"
    assert menu.LIST_OF_WORDS[0].category == "category"
    assert menu.LIST_OF_WORDS[0].hint == "hint"


def test_delete_word():
    menu = MainMenu()
    menu.LIST_OF_WORDS = [Word("word", "level", "category", "hint")]
    menu.delete_word("word")
    assert len(menu.LIST_OF_WORDS) == 0


def test_create_and_add_word():
    menu = MainMenu()
    menu.create_and_add_word("word", "level", "category", "hint")
    assert len(menu.LIST_OF_WORDS) == 1
    assert menu.LIST_OF_WORDS[0].value == "word"
    assert menu.LIST_OF_WORDS[0].level == "level"
    assert menu.LIST_OF_WORDS[0].category == "category"
    assert menu.LIST_OF_WORDS[0].hint == "hint"


def test_save_words():
    menu = MainMenu()
    menu.create_and_add_word("word", "level", "category", "hint")
    menu.save_words()
    with open('word_list.json', 'r', encoding='utf-8') as f:
        list_of_words = json.load(f)
    assert len(list_of_words) == 1
    assert list_of_words[0]['value'] == "word"
    assert list_of_words[0]['level'] == "level"
    assert list_of_words[0]['category'] == "category"
    assert list_of_words[0]['hint'] == "hint"


def test_load_words():
    menu = MainMenu()
    menu.create_and_add_word("word", "level", "category", "hint")
    menu.save_words()
    new_menu = MainMenu()
    new_menu.load_words()
    assert len(new_menu.LIST_OF_WORDS) == 1


def test_random_fields(mocker):
    menu = MainMenu()
    mock_randint = mocker.patch.object(random, 'randint', return_value=6)
    menu.LIST_OF_WORDS = [Word("word", "level", "category", "hint")]
    menu.random_fields()
    assert mock_randint.call_count == 1
    assert menu.users_level == "level"
    assert menu.users_category == "category"
    assert menu.users_count == 6


def test_refresh_lists():
    menu = MainMenu()
    menu.LIST_OF_WORDS = [Word("word", "level", "category", "hint"),
                          Word("word2", "level2", "category2", "hint2")]
    menu.refresh_lists()
    assert len(menu.LIST_OF_LEVELS) == 2
    assert len(menu.LIST_OF_CATEGORIES) == 2
    assert "level" in menu.LIST_OF_LEVELS
    assert "category" in menu.LIST_OF_CATEGORIES


def test_reset_fields():
    menu = MainMenu()
    menu.choice_category("category")
    menu.choice_level("level")
    menu.choice_count_of_tries(3)
    menu.reset_fields()
    assert menu.choice_category_flag is False
    assert menu.choice_level_flag is False
    assert menu.choice_count_flag is False
