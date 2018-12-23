# coding=utf-8

dictionary = [
    'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz',
    'абвгдеёжзийклмнопрстуфхцчшщъыьэюяабвгдеёжзийклмнопрстуфхцчшщъыьэюя',
    'ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ',
    'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ',
]


def shift_char(char, shift, new_dict):
    """
    Смещает шифруемый символ на указанное количество сдвигов
    :param char:        смещаемый символ
    :param shift:       количество смещений
    :param new_dict:    используемый алфавит
    :return:            полученный символ
    """
    print(char)
    dict_str = dictionary[new_dict]
    pos = dict_str.index(char)
    return dict_str[pos + shift]


def get_char_dict(char):
    """
    Определяет к какому алфавиту относится символ
    :param char:        определяемый символ
    :return:            индекс переменной в dictionary ( содержит алфавиты латиницы и кириллицы )
    """
    for i in range(4):
        if char in dictionary[i]:
            return i


def char_2_shift(char):
    """
    Возвращает количество смещений для буквы ( шифр виженера )
    :param char:        символ определяющий количество смещений
    :return:            количество смещений
    """
    for i in range(4):
        if char in dictionary[i]:
            return ord(char) - ord(dictionary[i][0])


def key_filter(key):
    result = ""

    for i in key:
        if i in dictionary[0] + dictionary[1] + dictionary[2] + dictionary[3]:
            result += i

    if result != "":
        return result
    else:
        return "__bad_key__"


def crypt_text(text, key, crypt_method, crypt_direction):
    result = ""
    key_counter = 0

    if crypt_method == "vijenere":
        key = key_filter(key)

    if key != "__bad_key__":
        for i in text:
            if i in dictionary[0] + dictionary[1] + dictionary[2] + dictionary[3]:
                if crypt_method == "caesar":
                    result += shift_char(i, 3 * crypt_direction, get_char_dict(i))
                else:
                    result += shift_char(i, char_2_shift(key[key_counter]) * crypt_direction, get_char_dict(i))
                    if key_counter < len(key) - 1:
                        key_counter += 1
                    else:
                        key_counter = 0
            else:
                result += i
        return result
    else:
        return "Введён неправильный ключ"
