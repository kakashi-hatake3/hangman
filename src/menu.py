from src.utils import clear_screen


class Menu:
    """
    Родительский класс для всех меню
    :param options: для каждой меню принимает разные значения,
     это кнопки в меню, по которым передвигается пользователь
    :param exit: флаг, проверяющий вышел ли пользователь из меню
    :param selected_index: это индекс определяющий на какой кнопке меню сейчас стрелка
    """
    options: list
    exit = False
    selected_index: int = 0

    def exit_menu(self) -> None:
        self.exit = True

    def print_menu(self) -> None:
        """
        Чистит экран с помощью clear_screen() и рисует кнопки меню из options и стрелку напротив соответствующей кнопки
        :return: None
        """
        clear_screen()
        print("Выберите опцию:")
        for i, option in enumerate(self.options):
            if i == self.selected_index:
                print(f"> {option}")
            else:
                print(f"  {option}")

    def handle_key(self):
        """
        Обрабатывает ввод пользователя с помощью input.
        :return: 'enter' если была нажата клавиша Enter, иначе None.
        """
        key = input("Введите 'w' для вверх, 's' для вниз, 'Enter' для выбора, 'e' для выхода: ").strip().lower()

        if key == '':  # Enter
            return 'enter'
        elif key == 'w':  # Up (вверх)
            self.selected_index = (self.selected_index - 1) % len(self.options)
        elif key == 's':  # Down (вниз)
            self.selected_index = (self.selected_index + 1) % len(self.options)
        elif key == 'e':  # Escape (выход)
            self.exit = True
        return None
