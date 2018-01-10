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
try:
    filemess = pos.MessageQueue('/queue', pos.O_CREAT)
except pos.ExistentialError:
    S = pos.unlink_message_queue('/queue') # detruit la file
    filemess = pos.MessageQueue('/queue', pos.O_CREAT) # puis redemande la creation
    stringToSend = ""
    # while True:
        # sleep(60 - datetime.utcnow().second)
pid = os.fork()
if pid == 0:
    # on envoie les données avec la file mais passer un tableau ne fonctionne pas !!!
    # il faut trouver un autre moyen
    # envoyer line par line ????
    for line in fbatchContent:
        for column in line:
            stringToSend += column + "\t"
        stringToSend += ";"
        filemess.send(stringToSend, None, 1)

    os.execl('findCommand.py', 'a')
        # continue
