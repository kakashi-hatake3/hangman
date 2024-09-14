from src.main_menu import MainMenu
from src.menu import Menu


class LevelMenu(Menu):
    """
    Меню для выбора сложности игры
    """
    options: list

    def get_list_from_main_menu(self, main_menu: MainMenu) -> None:
        """
        Принимает экземпляр MainMenu и заполняет список уровней в соответствии с актуальными данными из LIST_OF_LEVELS
        :param main_menu:
        :return: None
        """
        self.options = main_menu.LIST_OF_LEVELS
