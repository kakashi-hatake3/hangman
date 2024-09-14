from src.main_menu import MainMenu
from src.menu import Menu


class CategoryMenu(Menu):
    """
    Меню для выбора категории, наследуется от Menu
    """
    options: list

    def get_list_from_main_menu(self, main_menu: MainMenu) -> None:
        """
        Принимает экземлпяр MainMenu и заполняет список категорий,
         в соответствии с актуальными данными из LIST_OF_WORDS
        :param main_menu:
        :return: None
        """
        self.options = [word.category
                        for word in main_menu.LIST_OF_WORDS
                        if word.level == main_menu.users_level]
