# coding=utf-8

import json
import vk_api


def get_button(label, color, payload=''):
    return {
        'action': {
            'type': 'text',
            'payload': json.dumps(payload),
            'label': label
        },
        'color': color
    }


class Bot:
    """
    :param vk           - vk_api.VkApi ( регистрация токена на сервере VK API )
    :param vk_session   - Возвращает VkApiMethod(self). Позволяет обращаться к методам API как к обычным классам.
    :param users_list   - список содержащий пользователей обращавшихся к боту
    :param message      - сообщения, отправляемые в ответ на команды боту
    :param keyboard0    - "пустая" клавиатура
    :param keyboard1    - клавиатура выбора действий ( Шифр / Дешифр / Обработка фото )
    :param keyboard2    - клавиатура выбора метода шифрования ( Цезарь / Виженер / QR-код )
    :param keyboard3    - клавиатура выбора метода дешифрования ( Цезарь / Винежер )
    :param token        -

    Методы:
    :get_user_by_id:    - проверяет наличие пользователя в списке, и возвращает его объект ( класс User ) при нахождении
    :param self         - указатель на себя
    :param id           - id пользователя
    :return object User - объект класса User
    """
    vk = None
    vk_session = None
    users_list = None
    message = None
    keyboard0 = None
    keyboard1 = None
    keyboard2 = None
    keyboard3 = None
    keyboard4 = None
    token = None

    def get_user_by_id(self, id):
        for i in self.users_list:
            if i.id == id:
                return i
        return False

    def __init__(self, token):
        self.vk = vk_api.VkApi(token=token)
        self.vk_session = self.vk.get_api()
        self.users_list = []
        self.message = {
            "hello": "Сап! Нажми на кнопку - получишь результат \n"
                     "И твоя мечта осуществитсяяяяяя, \n"
                     "То просто нажми кнопку (назад) и это вернет тебя к началу",
            "encrypt": "Выбери метод.",
            "decrypt": "Выбери метод.",
            "keyboard": "Выбери кнопку.",
            "qr": "Введи текст.",
            "art": "Отправь мне фото, чтобы я применил фильтр.",
            "cancel": "Попробуй снова. Выбери кнопку.",
            "chipper": "Введите текст.",
            "key_input": "Введите ключ.",
            "unknown": "Я не понял тебя!\n"
                       "Попробуй снова!",

        }
        self.keyboard1 = {
            'one_time': False,
            'buttons': [
                [get_button(label='Шифр', color='primary')],
                [get_button(label='Дешифр', color='primary')],
                [get_button(label='ART', color='default')]
            ]
        }
        self.keyboard2 = {
            'one_time': False,
            'buttons': [
                [get_button(label='Caesar', color='primary')],
                [get_button(label='Vijenere', color='primary')],
                [get_button(label='QR', color='default')],
                [get_button(label='Назад', color='positive')]
            ]
        }
        self.keyboard3 = {
            'one_time': False,
            'buttons': [
                [get_button(label='Caesar', color='primary')],
                [get_button(label='Vijenere', color='primary')],
                [get_button(label='Назад', color='positive')]

            ]
        }
        self.keyboard4 = {
            'one_time': False,
            'buttons': [
                [get_button(label='Назад', color='positive')]

            ]
        }
