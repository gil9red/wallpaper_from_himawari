#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# Info: http://tproger.ru/tools/himawari-8-downloader/
# Source: https://gist.github.com/anonymous/c453ebfb9c7e3149d84e


def download_from_himawari():
    print('Download from himawari...')

    PATTERN_URL = "http://himawari8-dl.nict.go.jp/himawari8/img/D531106/{level}/{width}/{year}/{month}/{day}/{time}"

    from datetime import datetime, timedelta
    now = datetime.utcnow()
    now -= timedelta(minutes=30 + now.minute % 10, seconds=now.second)
    print('Date time image: {}.'.format(now))

    LEVEL = "4d"  # Level can be 4d, 8d, 16d, 20d
    NUMBLOCKS = int(LEVEL[:-1])  # For 4d will 4, for 20d -- 20
    WIDTH = 550

    data_url = {
        'level': LEVEL,
        'width': WIDTH,
        'year': now.strftime('%Y'),
        'month': now.strftime('%m'),
        'day': now.strftime('%d'),
        'time': now.strftime('%H%M%S'),
    }

    url = PATTERN_URL.format(**data_url)
    print('Pattern url: {}.'.format(url))

    IMAGE_WIDTH = WIDTH * NUMBLOCKS
    print('Create image with size {0}x{0}.'.format(IMAGE_WIDTH))

    from PIL import Image
    im = Image.new('RGB', (IMAGE_WIDTH, IMAGE_WIDTH))

    from urllib.request import urlopen
    import io
    import time

    for i in range(NUMBLOCKS):
        for j in range(NUMBLOCKS):
            url_part = url + '_{}_{}.png'.format(i, j)
            print('Download url: {}.'.format(url_part))

            while True:
                try:
                    with urlopen(url_part) as f:
                        part_im = Image.open(io.BytesIO(f.read()))
                        im.paste(part_im, (i * WIDTH, j * WIDTH))

                # TODO: do for exception timeout
                except Exception as e:
                    print(e)
                    time.sleep(60)
                    continue

                break

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
def set_wallpaper(path):
    import ctypes
    # import win32con

    # This code is based on the following two links
    # http://mail.python.org/pipermail/python-win32/2005-January/002893.html
    # http://code.activestate.com/recipes/435877-change-the-wallpaper-under-windows/
    cs = ctypes.c_buffer(path.encode())
    # return ctypes.windll.user32.SystemParametersInfoA(win32con.SPI_SETDESKWALLPAPER, 0, cs, 0)
    SPI_SETDESKWALLPAPER = 0x14
    return ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, cs, 0)


def run():
    try:
        img_path = download_from_himawari()

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
