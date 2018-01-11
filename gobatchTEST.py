#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import datetime
import calendar
import posix_ipc as pos


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

def readFile():
    with open("FBatch", "r") as f:
        array = []
        for line in f:
            line = line.rstrip()
            array.append(line.split('\t'))
    return array


fileContent = readFile()


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

    print(seconds)

    if seconds == 0:
        os.system(command)
