#! /usr/bin/python
#-*- coding: utf-8 -*-
import os
import sys
import signal
import time

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

for commande in readFile():
    print commande

while True:
    continue
