# coding=utf-8


class User:
    """
    :param crypt_method - метод шифрования
    :param crypt_func   - шифрование/дешифрование используется
    :param crypt_now    - флаг, определяющий что следующее сообщение будет текстом для шифрования/дешифрования
    :param qr_now       - флаг, определяющий что следующее сообщение нужно будет зашифровать qr-кодом
    :param art_now      - флаг, определяющий что в данный момент будет
    :param id           - id-пользователя

    Методы:
    :set_crypt_method:  - устанавливает метод шифрования для пользователя
    :param self     - указатель на себя
    :param method   - метод шифрования( "ecnrypt / decrypt" )
    :set_crypt_func:    - устанавливает тип ( шифрование / дешифрование )
    :param self     - указатель на себя
    :param func     - метод шифрования( "caesar" / "vijener" )
    :set_crypt_now:     - устанавливает флаг, определяющий момент для шифрования сообщения
    :param self     - указатель на себя
    :param state    - флаг-указатель
    :set_qr_now:        - устанавливает флаг, определяющий момент для шифрования qr-кодом
    :param self     - указатель на себя
    :param state    - флаг-указатель
    :set_art_now:       - устанавливает флаг, определяющий момент для обработки фотографии
    :param self     - указатель на себя/передаваемый объект класса
    :param state    - флаг-указатель
    """
    crypt_method = None
    crypt_func = None
    crypt_now = None
    qr_now = None
    art_now = None
    id = None
    crypt_text = None
    crypt_key = None

    def set_crypt_method(self, method=None):
        self.crypt_method = method

    def set_crypt_func(self, func=None):
        self.crypt_func = func

    def set_crypt_now(self, state=False):
        self.crypt_now = state

    def set_qr_now(self, state=False):
        self.qr_now = state

    def set_art_now(self, state=False):
        self.art_now = state

    def set_crypt_text(self, text=None):
        self.crypt_text = text

    def set_crypt_key(self, key=None):
        self.crypt_key = key

    def __init__(self, user_id):
        self.crypt_method = None
        self.crypt_func = None
        self.crypt_now = False
        self.qr_now = False
        self.art_now = False
        self.id = user_id
        self.crypt_text = None
        self.crypt_key = None
