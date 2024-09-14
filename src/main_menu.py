import json

from src.menu import Menu
from src.utils import clear_screen, random_choice, sleep, random_int
from src.word import Word


class MainMenu(Menu):
    """
    Основное меню
    :param LIST_OF_WORDS: список из объектов слов
    """
    options: list = ['Начать игру',
                     'Зарандомить',
                     'Выбрать категорию',
                     'Выбрать сложность',
                     'Выбрать количество попыток',
                     'Добавить слово',
                     'Удалить слово',
                     'Выйти']
    LIST_OF_WORDS = []
    LIST_OF_CATEGORIES = []
    LIST_OF_LEVELS = []

    def __init__(self, filename: str = 'word_list.json'):
        """
        :param filename: json файл, из которого берутся слова.
        :param self.users_category, self.users_level, self.users_count: параметры категории,
         уровня сложности и количество попыток, которые выбрал пользователь.
        :param self.choice_category_flag, self.choice_level_flag, self.choice_count_flag: флаги,
         которые означают какой параметр пользователь поменял сам,
          а какой нужно будет зарандомить при создании игровой сессии
        """
        self.users_category: str
        self.users_level: str
        self.users_count: int
        self.choice_category_flag: bool = False
        self.choice_level_flag: bool = False
        self.choice_count_flag: bool = False
        self.filename = filename

    def start_game(self):
        """
        Рандомит слово перед игрой
        :return: итоговое слово для игры и количество попыток
        """
        filtered_words = self.filter_words()
        result_word = ''
        try:
            result_word = random_choice(filtered_words)
        except IndexError:
            self.exit_menu()
        else:
            self.random_fields()
        try:
            return result_word, self.users_count
        except AttributeError:
            self.exit_menu()

    def filter_words(self):
        """
        Подбирает список слов соответствующие, выбранным сложности и категории
        :return: список слов
        """
        return [word
                for word in self.LIST_OF_WORDS
                if word.category == self.users_category and
                word.level == self.users_level]

    def choice_category(self, new_category) -> None:
        """
        Меняет категорию с рандомной на выбранную и меняет флаг выбора категории
        :param new_category: выбранная в меню категорий категория
        :return: None
        """
        self.users_category = new_category
        self.choice_category_flag = True

    def choice_level(self, new_level) -> None:
        """
        Меняет уровень сложности с рандомного на выбранный и меняет флаг выбора категории,
         а также если после выбора категории и сложности соответствующего слова не оказалось в json файле,
          то он подбирает рандомную категорию для слова, сложность оставляют ту же
        :param new_level: выбранный в меню уровней сложности уровень
        :return: None
        """
        self.users_level = new_level
        if len(self.filter_words()) == 0:
            self.choice_category_flag = False
            self.random_fields()
        self.choice_level_flag = True

    def choice_count_of_tries(self, new_count) -> None:
        self.users_count = new_count
        self.choice_count_flag = True

    def add_word(self) -> None:
        """
        Функция для добавления слова в json файл,
         в случае удачи вызывает функцию create_and_add_word и возвращается в главное меню
        :return: None
        """
        clear_screen()
        print("Введите: слово, уровень сложности, категорию для этого слова, подсказку."
              " Разделяя ', '. Для того чтобы вернуться введите 'выход'\n")
        sleep(0.15)
        while True:
            args = input().split(', ')
            if args[0] == 'выход':
                break
            elif len(args) == 4 and args[0] not in [word.value for word in self.LIST_OF_WORDS] and len(
                    args[0]) < 20:
                self.create_and_add_word(
                    args[0].lower().replace(' ', '_'),
                    args[1].lower(),
                    args[2].lower(),
                    args[3].lower()
                )
                break
            else:
                print('Вы где-то допустили ошибку!\n')

    def delete_word(self, value) -> None:
        """
        Функция удаления слова из json файла
        :param value: слово, которое пользователь выбрал в меню удаления
        :return: None
        """
        self.LIST_OF_WORDS = [word for word in self.LIST_OF_WORDS if word.value != value]
        self.save_words()

    def create_and_add_word(self, value, level, category, hint) -> None:
        """
        Создаем объект слова и добавляем его в список, а также вызывает save_words()
        :param value:
        :param level:
        :param category:
        :param hint:
        :return: None
        """
        word = Word(value, level, category, hint)
        self.LIST_OF_WORDS.append(word)
        self.save_words()

    def save_words(self) -> None:
        """
        Функция, которая сохраняет изменения в json файле, а также вызывает refresh_lists()
        :return:
        """
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump([word.to_dict() for word in self.LIST_OF_WORDS], f, ensure_ascii=False, indent=4)
        self.refresh_lists()

    def load_words(self) -> None:
        """
        Функция подгружает слова из json файла в LIST_OF_WORDS,
         в случае неудачи печатает сообщение об ошибке и завершает работу меню
        :return:
        """
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                self.LIST_OF_WORDS = [Word.from_dict(data) for data in json.load(f)]
        except FileNotFoundError:
            self.exit_menu()
            print('Файл не найден')
        except KeyError:
            self.exit_menu()
            print('В json файле некорректные данные')
        except json.decoder.JSONDecodeError:
            self.exit_menu()
            print('json файл некорректен')

    def refresh_lists(self) -> None:
        """
        Обновляет списки с уровнями и категориями, в соответствии с текущим LIST_OF_WORDS
        :return:
        """
        self.LIST_OF_LEVELS = list(set([word.level for word in self.LIST_OF_WORDS]))
        self.LIST_OF_CATEGORIES = list(set([word.category for word in self.LIST_OF_WORDS]))

    def random_fields(self) -> None:
        """
        Если пользователь не выбирал параметры слова, то просто их рандомит
        :return: None
        """
        self.refresh_lists()
        try:
            if not self.choice_level_flag:
                self.users_level = random_choice(self.LIST_OF_LEVELS)
            if not self.choice_category_flag:
                self.users_category = random_choice([word.category
                                                     for word in self.LIST_OF_WORDS
                                                     if word.level == self.users_level])
            if not self.choice_count_flag:
                self.users_count = random_int(6, 10)
        except IndexError:
            self.exit_menu()
            print('В json файле недостаточно слов')

    def reset_fields(self) -> None:
        """
        Обнавляет флаги изменения параметров слова, обычно вызывается после окончания игровой сессии
        :return: None
        """
        self.choice_category_flag = False
        self.choice_level_flag = False
        self.choice_count_flag = False
