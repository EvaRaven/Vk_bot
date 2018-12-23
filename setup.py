# coding=utf-8

from setuptools import setup, find_packages

import vk_bot

setup(
    name='vk_bot',
    version=vk_bot.__version__,
    packages=find_packages(),

    entry_points={
            'console_scripts': [
                    'run = vk_bot.start_bot:main'
                ]
        },
    install_requires=[
            'vk_api==11.3.0',
            'qrcode==6.0',
            'requests==2.20',
            'Pillow==5.3.0'
        ]

)
