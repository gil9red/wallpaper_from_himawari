#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


if __name__ == '__main__':
    import time
    import main

    while True:
        main.run()
        print('\n\n')

        # Every 30 minutes
        time.sleep(60 * 30)
