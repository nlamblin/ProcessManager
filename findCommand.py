#! /usr/bin/python3
# -*- coding: utf-8 -*

import os
import sys
import datetime
import calendar
import posix_ipc as pos


# Function that converts in seconds between the current day and the next trigger
# according to the parameters entered in fbatch
def convertInSecond(minute, hour, day, month, repeat):
    now = datetime.datetime.now()

    if repeat == "daily":
        canExecuteToday = now.replace(hour=int(heure), minute=int(minute))
        if now > canExecuteToday:
            tomorrow = now + datetime.timedelta(days=1)
            tomorrow = tomorrow.replace(hour=int(heure), minute=int(minute))
            second = (tomorrow - now).total_seconds()
        else:
            second = (canExecuteToday - now).total_seconds()
    elif repeat == "weekly":
        nextWeek = now + datetime.timedelta(days=7)
        dayOfNextWeek = nextWeek.isoweekday()
        diff = dayOfNextWeek - int(day)
        if diff > 0:
            diff = diff + 7
            nextWeek = now - datetime.timedelta(days=diff)
        else:
            diff = diff * (-1)
            diff = diff + 7
            nextWeek = now + datetime.timedelta(days=diff)
        nextWeek = nextWeek.replace(hour=int(hour), minute=int(minute))
        second = (nextWeek - now).total_seconds()
    elif repeat == "monthly":
        month_days = calendar.monthrange(now.year, now.month)[1]
        nextmonth = now + datetime.timedelta(days=month_days)
        if nextmonth.day != now.day:
            nextmonth.replace(day=1) - datetime.timedelta(days=1)
        nextmonth = nextmonth.replace(day=int(day), hour=int(heure), minute=int(minute))
        second = (nextmonth - now).total_seconds()
    elif repeat == "yearly":
        nextYear = now.replace(year=now.year + 1, month=int(month), day=int(day), hour=int(hour), minute=int(minute))
        second = (nextYear - now).total_seconds()

    return int(second)

def main():
    filemess = pos.MessageQueue('/queue', pos.O_CREAT)
    stringReceived = filemess.receive()

    commandList = []
    for arrayTemp in stringReceived.split(";"):
        commandList.append(arrayTemp.split('\t'))

    commandList = commandList[1:-1]

    for line in commandList:
        minute = line[1]
        heure = line[2]
        jour = line[3]
        mois = line[4]
        repet = line[5]
        command = line[6]

    seconds = convertInSecond(minute, heure, jour, mois, repet)
    if seconds == 0:
        os.system(command)



main()
