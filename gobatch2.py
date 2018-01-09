#! /usr/bin/python3
# -*- coding: utf-8 -*

import os
import sys
from time import sleep

while True:

    sleep(60)

    pid = os.fork()
    if pid == 0:
        os.execl('findCommand.py', 'a')

    continue
