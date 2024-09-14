from src.main_menu import MainMenu
from src.menu import Menu


class DeleteMenu(Menu):
    """
    Меню для выбора слова для удаления
    """
    options: list

    def get_list_from_main_menu(self, main_menu: MainMenu):
        """
        Заполняет список слов для удаления
        :param main_menu:
        :return: None
        """
        self.options = [word.value for word in main_menu.LIST_OF_WORDS]
