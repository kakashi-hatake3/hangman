import json
from unittest import mock

import pytest
from src.models import MainMenu


def test_load_words_success():
    class Word:
        def __init__(self, word):
            self.word = word

        @staticmethod
        def from_dict(data):
            return Word(data)

    class MainMenu:
        def __init__(self, filename):
            self.filename = filename
            self.LIST_OF_WORDS = []
            self.Word = Word

        def load_words(self):
            with open(self.filename, "r") as file:
                words_data = json.load(file)
                self.LIST_OF_WORDS = [self.Word.from_dict(word) for word in words_data]

    filename = '/src/word_list.json'
    with mock.patch("builtins.open", mock.mock_open(read_data='["word1", "word2", "word3"]')), \
            mock.patch("json.load", return_value=["word1", "word2", "word3"]):
        menu = MainMenu(filename)
        menu.load_words()

        assert len(menu.LIST_OF_WORDS) == 3  # Ensure we have 3 items in the list
        assert all(isinstance(word, Word) for word in menu.LIST_OF_WORDS)  # Check all items are instances of Word
        assert [word.word for word in menu.LIST_OF_WORDS] == ["word1", "word2", "word3"]  # Check the content


@pytest.fixture
def mock_exit_menu():
    with mock.patch.object(MainMenu, 'exit_menu') as mock_exit_menu_:
        yield mock_exit_menu_


def test_load_words_file_not_found_error(mock_exit_menu):
    filename = '/src/non_existent_file.json'
    menu = MainMenu(filename)

    with mock.patch('builtins.print') as mock_print:
        menu.load_words()
        mock_print.assert_called_once_with('Файл не найден')

    assert mock_exit_menu.called


def test_load_words_key_error(mock_exit_menu):
    class Word:
        @staticmethod
        def from_dict(data):
            required_keys = ['value', 'level', 'category', 'hint']
            for key in required_keys:
                if key not in data:
                    raise KeyError(f'Missing {key} in data')
            return data

    MainMenu.Word = Word
    filename = '/src/word_list.json'

    with mock.patch("builtins.open", mock.mock_open(read_data=json.dumps([{"non_existent_key": "value"}]))), \
            mock.patch("json.load", return_value=[{"non_existent_key": "value"}]):
        menu = MainMenu(filename)

        with mock.patch('builtins.print') as mock_print:
            menu.load_words()
            mock_print.assert_called_once_with("В json файле некорректные данные")

    assert mock_exit_menu.called


def test_load_words_json_decode_error(mock_exit_menu):
    filename = '/src/word_list.json'
    with mock.patch("builtins.open", mock.mock_open(read_data="non_json_data")):
        menu = MainMenu(filename)

        with mock.patch('builtins.print') as mock_print:
            menu.load_words()
            mock_print.assert_called_once_with('json файл некорректен')

    assert mock_exit_menu.called
