#! /usr/bin/python
#-*- coding: utf-8 -*-
import os
import sys
import signal
import time
import datetime as dt

def readFile():
    with open("FBatch", "r") as f:
        array = []
        for line in f:
            line = line.rstrip()
            array.append(line.split('\t'))

    return array

def closeProg(signal, frame):
    sys.exit(0);

signal.signal(signal.SIGINT, closeProg)

commandList = readFile()

for line in commandList:
    for column in line:
        split = column.split('  ')

        boolean_alarm = split[0]
        minute = split[1]
        heure = split[2]
        jour = split[3]
        mois = split[4]
        repet = split[5]
        command = split[6]

        now = dt.datetime.now()
        print(now)
        # if repet == "daily":
        #
        # elif repet == "weekly":
        #
        # elif repet == "monthly";
        #
        # elif repet == "yearly":
        #
        #
        # (b-a).total_seconds()
        #
        # print(minute)
        # if(column[0] == "0"):
        #     time_in_seconde()
        #     signal.signal(signal.SIGALRM, handler)
        #     signal.alarm()
while True:
    continue
