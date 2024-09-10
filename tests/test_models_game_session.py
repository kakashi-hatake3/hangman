import pytest
from src.models import GameSession, Word


@pytest.fixture
def game_session():
    mock_word = Word(value='тест', level='easy', category='general', hint='just guess')
    result_count = 5
    return GameSession(mock_word, result_count)


def test_initialization(game_session):
    assert game_session.users_answer == '____'
    assert game_session.count_of_tries == 5
    assert game_session.users_count == 5
    assert len(game_session.alphabet) == 32


def test_check_answer_correct(game_session):
    game_session.letter = 'т'
    game_session.check_answer()
    assert game_session.users_answer == 'т__т'
    assert game_session.users_count == 5


def test_check_answer_incorrect(game_session):
    game_session.letter = 'м'
    game_session.check_answer()
    assert game_session.users_answer == '____'
    assert game_session.users_count == 4


def test_check_answer_final(game_session):
    for letter in ['т', 'е', 'с', 'т']:
        game_session.letter = letter
        game_session.check_answer()
    assert game_session.users_answer == 'тест'
    assert game_session.users_count == 5
