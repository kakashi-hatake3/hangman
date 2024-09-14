class Word:
    """
    Класс для слова, который содержит само слово, сложность слова, категорию слова и подсказку к нему
    """

    def __init__(self, value='Значения нет',
                 level='Сложности нет',
                 category='Категории нет',
                 hint='Подсказки нет'):
        self.value = value
        self.level = level
        self.category = category
        self.hint = hint
        self.length = len(self.value)

    def to_dict(self):
        """
        Функция для перевода параметров слова к словарю для занесения в json файл
        :return: возвращает словарь параметров слова
        """
        return {
            'value': self.value,
            'level': self.level,
            'category': self.category,
            'hint': self.hint
        }

    @classmethod
    def from_dict(cls, data: dict):
        """
        Функция обратная предыдущей, конвертирует из словаря в отдельные параметры
        :param data: словарь параметров
        :return: возвращает параметры для слова из словаря
        """
        return cls(
            data['value'],
            data['level'],
            data['category'],
            data['hint']
        )
