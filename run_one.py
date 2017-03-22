#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# Info: http://tproger.ru/tools/himawari-8-downloader/
# Source: https://gist.github.com/anonymous/c453ebfb9c7e3149d84e


class NoImageException(Exception):
    pass


PATTERN_URL = "http://himawari8-dl.nict.go.jp/himawari8/img/D531106/{level}/{width}/{year}/{month}/{day}/{time}"

with open('No Image.png', 'rb') as f:
    NO_IMAGE_BYTES = f.read()


def download_from_himawari() -> str:
    """
    Function return file name to wallpaper image or None, if "No Image" return from himawari.

    """

    print('Download from himawari...')

    from datetime import datetime, timedelta
    print('Current date: {}.'.format(datetime.now().strftime('%d/%m/%Y %H:%M:%S')))

    now = datetime.utcnow()
    # now -= timedelta(minutes=30 + now.minute % 10, seconds=now.second)
    now -= timedelta(hours=2, minutes=30 + now.minute % 10, seconds=now.second)
    print('Date time image: {}.'.format(now))

    level = "4d"  # Level can be 4d, 8d, 16d, 20d
    numblocks = int(level[:-1])  # For 4d will 4, for 20d -- 20
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
    print('Pattern url: {}'.format(url))

    image_width = width * numblocks
    print('Create image with size {0}x{0}'.format(image_width))

    from PIL import Image
    im = Image.new('RGB', (image_width, image_width))

    from urllib.request import urlopen
    import io
    import time

    try:
        for i in range(numblocks):
            for j in range(numblocks):
                url_part = url + '_{}_{}.png'.format(i, j)
                print('Download url: {}'.format(url_part))

                while True:
                    try:
                        with urlopen(url_part) as f:
                            img_bytes = f.read()

                            # Если картинка пришла неправильная, прерываем скачивание
                            if img_bytes == NO_IMAGE_BYTES:
                                raise NoImageException()

                            part_im = Image.open(io.BytesIO(img_bytes))
                            im.paste(part_im, (i * width, j * width))

                    except NoImageException as e:
                        raise e

                    # Например, если проблема с подключением к инету
                    except Exception as e:
                        timeout = 60
                        print('Error: "{}". Next attempt through {} seconds.'.format(e, timeout))
                        time.sleep(timeout)
                        continue

                    break

    except NoImageException:
        return

    import os.path
    img_path = os.path.expanduser('~/Pictures/Himawari/wallpaper.jpg')
    img_path = os.path.normpath(img_path)
    print('Image path: {}.'.format(img_path))

    # Если папки не существует, создаем
    if not os.path.exists(os.path.dirname(img_path)):
        os.makedirs(os.path.dirname(img_path))

    im.save(img_path)

    return img_path


# SOURCE: http://www.blog.pythonlibrary.org/2014/10/22/pywin32-how-to-set-desktop-background/
def set_wallpaper(path: str) -> int:
    import ctypes

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
        import traceback
        tb = traceback.format_exc()
        print(tb)


if __name__ == '__main__':
    run()
