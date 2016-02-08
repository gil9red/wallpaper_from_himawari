#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


if __name__ == '__main__':
    import time
    from main import run

    while True:
        run()
        print('\n\n')

        # Every 30 minutes
        time.sleep(60 * 30)
