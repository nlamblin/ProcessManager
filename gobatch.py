#! /usr/bin/python
# -*- coding: utf-8 -*

import os
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

def convertFileToString():
    # first reading of the fbatch file
    fbatchContent = readFile()
    stringToSend = ''
    for line in fbatchContent:
        for column in line:
            stringToSend += column + "\t"
        stringToSend += ";"
    return stringToSend

# creating the queue
filemess = pos.MessageQueue('/queue', pos.O_CREAT)
stringToSend = convertFileToString()

def addToString(stringUpdated):
    global stringToSend
    strRead = ""
    for line in stringUpdated:
        for column in line:
            strRead += column + "\t"
        strRead += ";"
    stringToSend = strRead


while True:
    sleep(60 - datetime.utcnow().second)

    pid = os.fork()
    if pid == 0:
        # send the file content
        filemess.send(stringToSend, 1)

        # executs findCommand.py program
        os.execl('findCommand.py', 'a')

    continue
