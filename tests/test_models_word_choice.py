import random
import unittest
from unittest.mock import MagicMock

from src import models


class TestMainMenu(unittest.TestCase):

    def setUp(self):
        self.main_menu = models.MainMenu()
        self.main_menu.LIST_OF_WORDS = [MagicMock() for _ in range(20)]
        self.main_menu.LIST_OF_LEVELS = ['beginner', 'intermediate', 'advanced']
        self.main_menu.refresh_lists = MagicMock()

    def test_random_fields_no_flags_set(self):
        self.main_menu.choice_level_flag = False
        self.main_menu.choice_category_flag = False
        self.main_menu.choice_count_flag = False

        mock_random_choice = MagicMock()
        mock_random_choice.side_effect = ['intermediate', 'sports']
        random.choice = mock_random_choice

        self.main_menu.random_fields()

        self.assertEqual(self.main_menu.users_level, 'intermediate')
        self.assertEqual(self.main_menu.users_category, 'sports')

    def test_random_fields_some_flags_set(self):
        self.main_menu.choice_level_flag = True
        self.main_menu.choice_category_flag = False
        self.main_menu.choice_count_flag = False
        self.main_menu.users_level = 'beginner'

        mock_random_choice = MagicMock()
        mock_random_choice.side_effect = ['city']
        random.choice = mock_random_choice

        self.main_menu.random_fields()

        self.assertEqual(self.main_menu.users_level, 'beginner')
        self.assertEqual(self.main_menu.users_category, 'city')

    def test_random_fields_all_flags_set(self):
        self.main_menu.choice_level_flag = True
        self.main_menu.choice_category_flag = True
        self.main_menu.choice_count_flag = True
        self.main_menu.users_level = 'beginner'
        self.main_menu.users_category = 'sports'
        self.main_menu.users_count = 6

        self.main_menu.random_fields()

        self.assertEqual(self.main_menu.users_level, 'beginner')
        self.assertEqual(self.main_menu.users_category, 'sports')
        self.assertEqual(self.main_menu.users_count, 6)
