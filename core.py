# coding=utf-8

import json
import vk_api
import cryptograph as chiper
import qr_encoder as qr
import img_processor as blur
import os
from bot import Bot
from user import User
from vk_api.longpoll import VkLongPoll, VkEventType
from random import randint
import requests



def create_keyboard(keyboard):
    """
    Создание json-клавиатуры
    :param keyboard:    словарь содержащий параметры клавиатуры
    :return:            json-объект клавиатуры
    """
    return json.dumps(keyboard, ensure_ascii=False).encode('utf-8')


def send_message(bot, user, text):
    """
    Отправка сообщения указанному пользователю
    :param bot:         объект класса Bot
    :param user:        id-пользователя
    :param text:        текст сообщения
    """
    bot.vk.method('messages.send', {'user_id': user, 'message': text, 'random_id': randint(-10000, 10000)})


def send_button(bot, user, text, keyboard):
    """
    Отправка сообщения с прикреплённой клавиатурой
    :param bot:         объект класса Bot
    :param user:        id-пользователя
    :param text:        текст сообщения
    :param keyboard:    прикрепляемая клавиатура
    """
    bot.vk.method('messages.send', {'peer_id': user, 'message': text, 'random_id': randint(-10000, 10000),
                                    'keyboard': create_keyboard(keyboard)})


def send_photo_to_user(bot, user=None, text=None, photos=None):
    """
    Отправка фото пользователю
    :param bot:         объект класса Bot
    :param user:        id-пользователя
    :param text:        текст сообщения
    :param photos:      список с фотографиями
    """
    if photos is None:
        photos = []
    upload = vk_api.VkUpload(bot.vk)
    uploaded_photos = upload.photo_messages(photos)
    attachments = []

    for photo in uploaded_photos:
        attachments.append('photo{}_{}'.format(photo['owner_id'], photo['id']))

    bot.vk_session.messages.send(user_id=user, random_id=randint(-10000, 10000),
                                 attachment=','.join(attachments), message=text)


def download(file_link, id):
    """
    Скачивание фотографии по vk-ссылке на неё
    :param file_link:   ссылка на фотографию
    :return: сохранённая фотография
    """
    with open("savedFile_{0}.jpg".format(id), 'wb') as handle:
        response = requests.get(file_link, stream=True)
        if not response.ok:
            print(response)
        for block in response.iter_content(1024):
            if not block:
                break
            handle.write(block)
    return "savedFile_{0}.jpg".format(id)


def get_size_index(attach, size):
    """
    Находит индекс элемента во вложениях по заданным размерам.
    Если фотографии нужного размера нет во вложениях, вернёт первый по порядку размер из json-списка.
    :param attach:          вложения
    :param size:            нужный размер изображения
    :return:
    """
    for el in size:
        for i in range(len(attach)):
            if attach[i]['type'] == el:
                print('find_it', el)
                return i
    return 0


def parse_json_format(attachments):
    """
    Парсинг вложений сообщения json-формата. Получение из полученного json-файла ссылок на вложения
    :param attachments:     вложения
    :return:                словарь с ссылками на вложения
    """
    url_l = []
    attach_has_photo = False

    for attach in attachments:
        if attach['type'] == 'photo':
            attach_has_photo = True
            url = attach['photo']['sizes']
            size_url = get_size_index(url, ['w', 'z', 'y', 'x', 'r'])
            url_l.append(url[size_url]['url'])

    return [url_l, attach_has_photo]


def blur_photo(bot, event, id):
    """
    Скачивание принятой фотографии, её обработка фильтром и отправка пользователю. В случае если во вложениях не будет
    найдено фотографий, бот отправит соответствующее сообщение.
    :param bot:         объект класса Bot
    :param event:       объект класса Event, содержащий данные о принятом сообщении
    :param id:          id-пользователя
    """
    json_output = bot.vk_session.messages.getHistory(user_id=event.peer_id, count=1)['items'][0]['attachments']
    parse_result = parse_json_format(json_output)
    blured_photo = []
    counter = 0

    for key in parse_result[0]:  #
        blur.blur_photo(download(key, id), id, counter)
        blured_photo.append("blured_{0}_{1}.jpg".format(id, counter))
        counter += 1

    if not parse_result[1]:
        send_message(bot, id, "Во вложениях нет фотографий")
    else:
        send_photo_to_user(bot, id, photos=blured_photo)
        os.remove("savedFile_{0}.jpg".format(id))
    for i in blured_photo:
        os.remove(i)


def message_handler(event, bot):
    """
    :param  event   - событие полученное от longpool
    :param  bot     - объект класса Bot

    event.text      - получение текста сообщения из event
    event.user_id   - получение id пользователя из event
    """
    text = event.text
    id = event.user_id

    if not Bot.get_user_by_id(bot, id):  # проверка наличия пользователя в users_list
        bot.users_list.append(User(id))  # создание объекта пользователя и добавление его в список

    user = Bot.get_user_by_id(bot, id)  # получение объекта отправителя сообщения

    if user.art_now and event.attachments == {} and text.lower() != "назад":
        send_message(bot, id, "Вы не отправили фотографию")
        return

    if text.lower() == 'привет' and not user.qr_now:
        send_button(bot, id, bot.message["hello"], bot.keyboard1)
    elif text.lower() == 'клавиатура' and not user.qr_now:
        send_button(bot, id, bot.message["keyboard"], bot.keyboard1)
    elif text.lower() == 'шифр' and not user.qr_now:
        send_button(bot, id, bot.message["encrypt"], bot.keyboard2)
        User.set_crypt_func(user, "encrypt")
    elif text.lower() == 'дешифр' and not user.qr_now:
        send_button(bot, id, bot.message["decrypt"], bot.keyboard3)
        User.set_crypt_func(user, "decrypt")
    elif (text.lower() == 'caesar' or text.lower() == 'vijenere') and not user.qr_now and not user.crypt_now:
        if not user.crypt_func is None:
            send_button(bot, id, bot.message["chipper"], bot.keyboard4)
            User.set_crypt_now(user, True)
            User.set_crypt_method(user, text.lower())
            print()
        else:
            send_button(bot, id, "Сначала нужно выбрать действия с текстом ( шифрование / дешифрование )",
                        bot.keyboard1)
    elif text.lower() == 'qr' and not user.qr_now and not user.crypt_now:
        if user.crypt_func == "encrypt":
            send_button(bot, id, bot.message["qr"], bot.keyboard4)
            User.set_qr_now(user, True)
        else:
            send_button(bot, id, "Сначала нужно выбрать действия с текстом ( шифрование / дешифрование )",
                        bot.keyboard1)
    elif text.lower() == 'art' and not user.qr_now:
        send_button(bot, id, bot.message["art"], bot.keyboard4)
        User.set_art_now(user, True)
    elif text.lower() == 'назад':
        send_button(bot, id, bot.message["cancel"], bot.keyboard1)
        User.set_art_now(user)
        User.set_crypt_func(user)
        User.set_crypt_method(user)
        User.set_crypt_now(user)
        User.set_qr_now(user)
    elif text.lower() == 'помощь' and not user.qr_now:
        send_button(bot, id, bot.message["cancel"], bot.keyboard1)
    elif user.crypt_now and text != "" and user.crypt_text is None:
        User.set_crypt_text(user, text)
        if user.crypt_method == "caesar":
            if user.crypt_func == "encrypt":
                send_message(bot, id,
                             "Ваш текст: " + chiper.crypt_text(user.crypt_text, user.crypt_key, user.crypt_method, 1)
                             + ".\n Введите текст")
            else:
                send_message(bot, id,
                             "Ваш текст: " + chiper.crypt_text(user.crypt_text, user.crypt_key, user.crypt_method, -1)
                             + ".\n Введите текст")
            User.set_crypt_text(user)
        else:
            send_message(bot, id, "Введи ключ.")
    elif user.crypt_now and text != "" and user.crypt_key is None and user.crypt_text != "" and user.crypt_method == "vijenere":
        User.set_crypt_key(user, text)
        if user.crypt_func == "encrypt":
            send_message(bot, id,
                         "Ваш текст: " + chiper.crypt_text(user.crypt_text, user.crypt_key, user.crypt_method, 1)
                         + ".\n Введите текст")
        else:
            send_message(bot, id,
                         "Ваш текст: " + chiper.crypt_text(user.crypt_text, user.crypt_key, user.crypt_method, -1)
                         + ".\n Введите текст")
        User.set_crypt_key(user)
        User.set_crypt_text(user)
    elif user.qr_now:
        if text != "":
            qr.make_qr(text, id)
            send_photo_to_user(bot, user=id, photos=['qr_photo_{0}.jpg'.format(id)])
            os.remove('qr_photo_{0}.jpg'.format(id))
        else:
            send_message(bot, id, "Вы не отправили текст.")
    elif event.attachments != {} and user.art_now:
        blur_photo(bot, event, id)
    else:
        send_button(bot, id, bot.message["unknown"], bot.keyboard1)


def bot_vk(token):
    """
        Bot             - создаёт класс бота, принимающий в качестве аргумента токен
        :param  token   - токен-ключ бота

        VkLongPool      - использование метода "длинных опросов"
        message_handler - обработчик принятых сообщений
    """
    bot = Bot(token)  # Создаём класс Bot
    long_poll = VkLongPoll(bot.vk)  # Используем метод "длинных опросов"

    for event in long_poll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:  # Если при опросе найдено новое сообщение не от бота
            message_handler(event, bot)  # Обработчик сообщений


if __name__ == '__main__':
    bot_vk('token')
