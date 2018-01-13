#! /usr/bin/python
# -*- coding: utf-8 -*

import os
import atexit
import posix_ipc as pos

from logger import logError
from logger import logInfo
from pgcycl import useSemaphore
from pgcycl import listAllTasks
from pgcycl import createSemaphore
from datetime import datetime
from time import sleep


# Function to read the fbatch file
def readFile():
    list = useSemaphore(listAllTasks, False, False)
    array = []
    for line in list:
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


# Get semaphore FBatch-Updated
def getSemaphore():
    try:
        # Creating semaphore
        logInfo('[GOBATCH]: Creating semaphore', False)
        semaphore = pos.Semaphore('/FBatch_Updated', pos.O_CREAT | pos.O_EXCL, initial_value=1)
        logInfo('[GOBATCH]: Created semaphore', False)

    except pos.ExistentialError:
        # Semaphore already created
        logInfo('[GOBATCH]: Semaphore already created', False)
        semaphore = pos.Semaphore('/FBatch_Updated', pos.O_CREAT)
        logInfo('[GOBATCH]: Using existing semaphore', False)

    return semaphore


# Handler to atexit function
def exit_handler():
    pos.Semaphore('/FBatch_Updated', pos.O_CREAT).unlink()


# create semaphore
createSemaphore()

# creating the queue
logInfo('[GOBATCH]: Creating the queue', False)
queueContentFile = pos.MessageQueue('/queue', pos.O_CREAT)
stringToSend = convertFileToString()

# Use when gobatch.py is kill
atexit.register(exit_handler)

# Create and get semaphore
semaphore = getSemaphore()

while True:

    # wait until the next minute
    sleep(60 - datetime.utcnow().second)

    # try to get the semaphore to know if the file has been updated
    try:
        semaphore.acquire(0)
        stringToSend = convertFileToString()

        # clear the semaphore
        while semaphore.acquire(0):
            continue

    except pos.BusyError:
        logInfo('[GOBATCH]: Semaphore acquired', False)

    finally:
        logInfo('[GOBATCH]: Creating child process', False)
        if os.fork() == 0:
            # send the file content
            logInfo('[GOBATCH]: Send the message with the queue', False)
            queueContentFile.send(stringToSend, 1)

            # executs findCommand.py program
            os.execl('findCommand.py', 'a')

    continue
