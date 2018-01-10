#! /usr/bin/python
# -*- coding: utf-8 -*

import os
import sys
import posix_ipc as pos

from datetime import datetime
from time import sleep


# Function to read the fbatch file
def readFile():
    with open("FBatch", "r") as f:
        array = []
        for line in f:
            line = line.rstrip()
            array.append(line.split('\t'))
    return array

# first reading of the fbatch file
fbatchContent = readFile()

# creating the queue
filemess = pos.MessageQueue('/queue', pos.O_CREAT)

while True:
    stringToSend = ""

    sleep(60 - datetime.utcnow().second)

    pid = os.fork()
    if pid == 0:
        for line in fbatchContent:
            for column in line:
                stringToSend += column + "\t"
            stringToSend += ";"

        filemess.send(stringToSend, 1)

        os.execl('findCommand.py', 'a')

    continue
