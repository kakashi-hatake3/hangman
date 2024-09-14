from src.word import Word
from utils import clear_screen, sleep


class GameSession:
    def __init__(self, result_word, result_count):
        """
        :param self.users_answer: это слово, которое в данный момент получается у пользователя,
         изначально равняется '_' * длину загаданного слова
        :param self.users_count: это оставшиеся попытки у пользователя
        :param self.alphabet: это алфавит оставшихся букв для угадывания
        :param self.letter: это буква, которую ввел пользователь
        :param self.exit: это флаг проверяющий не вышел ли пользователь из игровой сессии
        :param self.hint: это флаг, проверяющий взял ли пользователь подсказку
        :param result_word: это объект класса Word, который был выбран в MainMenu для данной игровой сессии
        :param result_count: это количество попыток, которые были выбраны или зарандомлены в MainMenu
        """
        self.word: Word = result_word
        self.users_answer: str = '_' * self.word.length
        self.count_of_tries: int = result_count
        self.users_count: int = result_count
        self.alphabet: str = ''.join([chr(code) for code in range(ord('а'), ord('я') + 1)])
        self.letter = ''
        self.hint = False
        self.exit = False

    def show(self) -> None:
        """
        Функция отрисовывающая всю игровую сессию
        :return: None
        """
        while not self.exit:
            clear_screen()
            self.print_hangman()
            self.print_count_of_tries()
            self.print_fields()
            self.print_word()
            self.print_hint()
            self.print_alphabet()
            self.get_hint()
            self.get_input()
            if not self.exit:
                self.get_exit()

    def end(self) -> None:
        """
        Функция завершающая игру
        :return: None
        """
        if self.users_count == 0:
            clear_screen()
            print('Вы проиграли ;(')
            sleep(3)
            self.exit = True
        else:
            clear_screen()
            print('Вы выиграли!!!')
            sleep(3)
            self.exit = True

    def print_count_of_tries(self) -> None:
        print('Кол-во оставшихся попыток: ', self.users_count, '\n')

    def print_fields(self) -> None:
        print('Сложность: ', self.word.level, '\n')
        print('Категория: ', self.word.category, '\n')

    def print_word(self) -> None:
        print('Слово: ', self.users_answer + '\n')

    def print_hint(self) -> None:
        """
        Пишет подсказку
        :return: None
        """
        if self.hint:
            print('Подсказка: ', self.word.hint, '\n')
        else:
            print('Подсказка: ___\n')

    def print_alphabet(self) -> None:
        print('Оставшиеся буквы: ', self.alphabet, '\n')

    def get_hint(self) -> None:
        """
        Проверяет нужно ли давать подсказку
        :return: None
        """
        if not self.hint:
            if input('Чтобы показать подсказку напишите Y: ').lower() == 'y':
                self.hint = True

    def get_exit(self) -> None:
        """
        Проверяет нужно ли выходить из игровой сессии
        :return: None
        """
        if input('Чтобы выйти из игры напишите "выход": ').lower() == 'выход':
            self.exit = True

    def get_input(self) -> None:
        """
        Принимает букву пользователя, а также возвращает ошибку, при некорректности ввода
        :return: None
        """
        try:
            self.letter = input('Введите букву: ').lower()
            if len(self.letter) == 1:
                if self.letter in self.alphabet:
                    self.check_answer()
                else:
                    print('Буква должна быть в алфавите')
            else:
                print('Символ должен быть длины 1')
        except ValueError:
            print('Вводите букву!')

    def check_answer(self) -> None:
        """
        Вызывается, если была введена корректная буква, проверяет есть ли буква в слове и меняет self.users_answer,
        а также вызывает конец игры, если кончились попытки или слово было угадано
        :return: None
        """
        self.alphabet = self.alphabet.replace(self.letter, '_')
        if self.letter in self.word.value:
            indexes = [ind for ind, letter in enumerate(list(self.word.value)) if letter == self.letter]
            for i in indexes:
                self.users_answer = self.users_answer[:i] + self.letter + self.users_answer[i + 1:]
            if self.users_answer == self.word.value:
                self.end()
        else:
            self.users_count -= 1
            if self.users_count == 0:
                self.end()

    def print_hangman(self) -> None:
        """
        Печатает виселицу, в зависимости от оставшихся попыток пользователя
        :return: None
        """
        stages = [
            """
                -----
                |   |
                |
                |
                |
                |
                |
            """,
            """
                -----
                |   |
                |   O
                |
                |
                |
                |
            """,
            """
                -----
                |   |
                |   O
                |   |
                |
                |
                |
            """,
            """
                -----
                |   |
                |   O
                |  /|
                |
                |
                |
            """,
            """
                -----
                |   |
                |   O
                |  /|\\
                |
                |
                |
            """,
            """
                -----
                |   |
                |   O
                |  /|\\
                |  /
                |
                |
            """,
            """
                -----
                |   |
                |   O
                |  /|\\
                |  / \\
                |
                |
            """,
            """
                -----
                |   |
                |   O
                |  /|\\
                |   |
                |  / \\
                |
                |
            """,
            """
                -----
                |   |
                |   O
                |  /|\\
                |   |
                |   |
                |  / \\
                |
                |
            """,
            """
                -----
                |   |
                |   O
                |  /|\\
                |   |
                |   |
                |   |
                |  / \\
                |
                |
            """,
            """
                -----
                |   |
                |   O
                |  /|\\
                |   |
                |   |
                |   |
                |   |
                |  / \\
                |
                |
            """
        ]
        print(stages[self.count_of_tries - self.users_count] + '\n')
