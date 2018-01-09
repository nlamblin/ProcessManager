#! /usr/bin/python
#-*- coding: utf-8 -*-
import os
import sys
import signal
import time
import datetime
import calendar

                                                #############
                                                # FUNCTIONS #
                                                #############

#Fonction permettant de lire le fichier fbatch
def readFile():
    with open("FBatch", "r") as f:
        array = []
        for line in f:
            line = line.rstrip()
            array.append(line.split('\t'))
    return array

#Fonction qui convertit en seconde entre le jour courant et le prochain declenchement
#en fonction des paramètres inscrit dans fbatch
def convertInSecond(minute, heure, jour, mois, repet):
    now = datetime.datetime.now()
    if repet == "daily":
        tomorrow = now + datetime.timedelta(days=1)
        tomorrow = tomorrow.replace(hour=int(heure), minute = int(minute))
        seconde = (tomorrow - now).total_seconds()
    elif repet == "weekly":
        nextWeek = now + datetime.timedelta(days=7)
        dayOfNextWeek = nextWeek.isoweekday()
        diff = dayOfNextWeek - int(jour)
        if diff > 0:
            diff = diff + 7
            nextWeek = now - datetime.timedelta(days=diff)
        else:
            diff = diff * (-1)
            diff = diff + 7
            nextWeek = now + datetime.timedelta(days=diff)
        nextWeek = nextWeek.replace(hour=int(heure), minute = int(minute))
        seconde = (nextWeek - now).total_seconds()
    elif repet == "monthly":
        month_days = calendar.monthrange(now.year, now.month)[1]
        nextmonth = now + datetime.timedelta(days=month_days)
        if nextmonth.day != now.day:
            nextmonth.replace(days=1) - datetime.timedelta(days=1)
        nextmonth = nextmonth.replace(day=int(jour),hour=int(heure), minute = int(minute))
        seconde = (nextmonth - now).total_seconds()
    elif repet == "yearly":
        nextYear = now.replace(year=now.year + 1, month=int(mois),day=int(jour),hour=int(heure), minute = int(minute))
        seconde = (nextYear - now).total_seconds()
        print (nextYear)

    return seconde

#Execution de la commande
def handler(commande):
    os.system(commande)

                                                ########
                                                # MAIN #
                                                ########


commandList = readFile()

for line in commandList:
    boolean_alarm = line[0]
    minute = line[1]
    heure = line[2]
    jour = line[3]
    mois = line[4]
    repet = line[5]
    command = line[6]

    seconde = convertInSecond(minute, heure, jour, mois, repet)

    if(boolean_alarm == "0"):
        #On creer une alarme qui s'activera dans x secondes et executera le handler
        signal.signal(signal.SIGALRM, handler(command))
        signal.alarm(seconde)


while True:
    continue
