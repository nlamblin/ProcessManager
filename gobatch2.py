#! /usr/bin/python3
# -*- coding: utf-8 -*

import os
import sys
from datetime import datetime
from time import sleep

while True:

    sleep(60 - datetime.utcnow().second)

    pid = os.fork()
    if pid == 0:
        os.execl('findCommand.py', 'a')

    continue
