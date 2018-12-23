# coding=utf-8

from PIL import Image, ImageFilter


def blur_photo(file_name, id, counter):
    """
    :param counter:     счетчик
    :param id:          id-пользователя
    :param file_name:   путь к обрабатываемому файлу
    """
    Image.open(file_name).filter(ImageFilter.BLUR).save("blured_{0}_{1}.jpg".format(id, counter))
