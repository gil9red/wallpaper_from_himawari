#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# Info: http://tproger.ru/tools/himawari-8-downloader/
# SOURCE: https://gist.github.com/anonymous/c453ebfb9c7e3149d84e


import ctypes
import io
import time
import os.path
import traceback
from urllib.request import urlopen
from typing import Optional
from datetime import datetime, timedelta

from PIL import Image


# TODO: поломанное изображение: http://himawari8-dl.nict.go.jp/himawari8/img/D531106/4d/550/2017/03/24/140000_0_3.png


class NoImageException(Exception):
    pass


PATTERN_URL = "https://himawari8-dl.nict.go.jp/himawari8/img/D531106/{level}/{width}/{year}/{month}/{day}/{time}"


with open('No Image.png', 'rb') as f:
    NO_IMAGE_BYTES = f.read()


def download_from_himawari() -> Optional[str]:
    """
    Function return file name to wallpaper image or None, if "No Image" return from himawari.

    """

    print('Download from himawari...')
    print(f'Current date: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}.')

    now = datetime.utcnow()
    now -= timedelta(hours=4, minutes=30 + now.minute % 10, seconds=now.second)
    print(f'Date time image: {now}.')

    level = "4d"  # Level can be 4d, 8d, 16d, 20d
    num_blocks = int(level[:-1])  # For 4d will 4, for 20d -- 20
    width = 550

    data_url = {
        'level': level,
        'width': width,
        'year': now.strftime('%Y'),
        'month': now.strftime('%m'),
        'day': now.strftime('%d'),
        'time': now.strftime('%H%M%S'),
    }

    url = PATTERN_URL.format(**data_url)
    print(f'Pattern url: {url}')

    image_width = width * num_blocks
    print(f'Create image with size {image_width}x{image_width}')

    img = Image.new('RGB', (image_width, image_width))

    attempts = 30

    try:
        for i in range(num_blocks):
            for j in range(num_blocks):
                url_part = f'{url}_{i}_{j}.png'
                print(f'Download url: {url_part}')

                while True:
                    try:
                        with urlopen(url_part) as f:
                            img_bytes = f.read()

                            # Если картинка пришла неправильная, прерываем скачивание
                            if img_bytes == NO_IMAGE_BYTES:
                                raise NoImageException()

                            part_im = Image.open(io.BytesIO(img_bytes))
                            img.paste(part_im, (i * width, j * width))

                    except NoImageException as e:
                        raise e

                    # Например, если проблема с подключением к инету
                    except Exception as e:
                        attempts -= 1
                        if attempts == 0:
                            return

                        timeout = 60
                        print(f'Error: "{e}". Next attempt through {timeout} seconds.')
                        time.sleep(timeout)
                        continue

                    break

    except NoImageException:
        return

    img_path = os.path.expanduser('~/Pictures/Himawari/wallpaper.jpg')
    img_path = os.path.normpath(img_path)
    print(f'Image path: {img_path}.')

    # Если папки не существует, создаем
    if not os.path.exists(os.path.dirname(img_path)):
        os.makedirs(os.path.dirname(img_path))

    img.save(img_path)

    return img_path


# SOURCE: http://www.blog.pythonlibrary.org/2014/10/22/pywin32-how-to-set-desktop-background/
def set_wallpaper(path: str) -> int:
    # This code is based on the following two links
    # http://mail.python.org/pipermail/python-win32/2005-January/002893.html
    # http://code.activestate.com/recipes/435877-change-the-wallpaper-under-windows/
    cs = ctypes.c_buffer(path.encode())
    spi_setdeskwallpaper = 0x14
    return ctypes.windll.user32.SystemParametersInfoA(spi_setdeskwallpaper, 0, cs, 0)


def run():
    try:
        img_path = download_from_himawari()
        if img_path is None:
            print('No image!')
            return

        print('Setting Wallpaper...')
        set_wallpaper(img_path)

        print('Done!')

    except Exception as e:
        # Выводим ошибку в консоль
        tb = traceback.format_exc()
        print(tb)


if __name__ == '__main__':
    run()
