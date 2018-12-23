# coding=utf-8

import qrcode


def make_qr(text, id):
    """
    :param text:    текст, преобразуемый в QR-код
    """
    qrcode.make(text).save('qr_photo_{0}.jpg'.format(id))
