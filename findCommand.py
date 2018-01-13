#! /usr/bin/python
# -*- coding: utf-8 -*

import os
import datetime
import calendar
import posix_ipc as pos

from logger import logError
from logger import logInfo


# Function that converts in seconds between the current day and the next trigger
# according to the parameters entered in fbatch
def secondsLeft(minute, hour, day, month, repeat):
    now = datetime.datetime.now()

    if repeat == "daily":
        canExecuteToday = now.replace(hour=int(hour), minute=int(minute))
        if now > canExecuteToday:
            tomorrow = now + datetime.timedelta(days=1)
            tomorrow = tomorrow.replace(hour=int(hour), minute=int(minute))
            second = (tomorrow - now).total_seconds()
        else:
            second = (canExecuteToday - now).total_seconds()
    elif repeat == "weekly":
        nextWeek = now + datetime.timedelta(days=7)
        dayOfNextWeek = nextWeek.isoweekday()
        diff = int(day) - dayOfNextWeek
        diff = diff + 7
        nextWeek = now + datetime.timedelta(days=diff)
        nextWeek = nextWeek.replace(hour=int(hour), minute=int(minute))
        second = (nextWeek - now).total_seconds()
    elif repeat == "monthly":
        month_days = calendar.monthrange(now.year, now.month)[1]
        nextmonth = now + datetime.timedelta(days=month_days)
        if nextmonth.day != now.day:
            nextmonth.replace(day=1) - datetime.timedelta(days=1)
        nextmonth = nextmonth.replace(day=int(day), hour=int(hour), minute=int(minute))
        second = (nextmonth - now).total_seconds()
    elif repeat == "yearly":
        nextYear = now.replace(year=now.year + 1, month=int(month), day=int(day), hour=int(hour), minute=int(minute))
        second = (nextYear - now).total_seconds()

    return int(second)


# Get the message and convert the string (which contains the file content) to array
def convertStringToArray():
    # get the message
    logInfo('[GOBATCH]: Receive the message with the queue', False)
    queue = pos.MessageQueue('/queue', pos.O_CREAT)
    stringReceived = queue.receive()[0]

    # split the message and remove the last element because it is empty
    stringSplitted = stringReceived.split(';')[:-1]

    commandList = []
    for arrayTemp in stringSplitted:
        # split the message and remove the last element because it is empty
        commandList.append(arrayTemp.split('\t')[:-1])

    return commandList


fileContent = convertStringToArray()

# cross the array which contains the file content
for line in fileContent:
    minute = line[0]
    hour = line[1]
    day = line[2]
    month = line[3]
    repeat = line[4]
    command = line[5]

    # get seconds left before the command execution
    seconds = secondsLeft(minute, hour, day, month, repeat)
    if seconds == 0:
        logInfo('[GOBATCH]: Command ' + command + ' executes', False)
        os.system(command)
