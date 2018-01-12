#! /usr/bin/python
# -*- coding: utf8 -*-

#####
# Imports
#####

import os
import datetime
import posix_ipc as pos

#####
# Global var declaration
#####


# TODO: Change during install

STDOUT_FILE = 'log-stdout'
STDERR_FILE = 'log-stderr'

#####
# Function declaration
#####


def P(semaphore, name):
    try:
        logMessage('[{}]: Acquiring semaphore'.format(name), STDOUT_FILE, 2)
        semaphore.acquire()
        logMessage('[{}]: Semaphore acquired'.format(name), STDOUT_FILE, 2)

    except:
        semaphore.release()


def V(semaphore, name):
    try:
        logMessage('[{}]: Releasing semaphore'.format(name), STDOUT_FILE, 2)
        semaphore.release()
        logMessage('[{}]: Semaphore released'.format(name), STDOUT_FILE, 2)

    except:
        semaphore.release()


def logMessage(message, file, severity):
    if severity == 0:
        message = '[FATAL]: ' + message

    elif severity == 1:
        message = '[WARNING]: ' + message

    now = datetime.datetime.now()
    date = '[{}:{}:{}.{}][PID:{}]'.format(now.hour, now.minute, now.second, now.microsecond, os.getpid())
    message = date + message + '\n'

    info_file = open(file, 'a')
    info_file.write(message)
    info_file.close()


def logInfo(info_message, stdout_log):
    info_semaphore = info_init()
    try:
        P(info_semaphore, 'INFO_LOGGER')
        logMessage(info_message, STDOUT_FILE, 2)

    finally:
        V(info_semaphore, 'INFO_LOGGER')

    if stdout_log:
        print(info_message)


def logError(error_message, stdout_log, is_fatal):
    error_semaphore = error_init()
    try:
        P(error_semaphore, 'INFO_LOGGER')
        logMessage(error_message, STDERR_FILE, is_fatal)

    finally:
        V(error_semaphore, 'INFO_LOGGER')

    if stdout_log:
        print(error_message)


#####
# Function declaration
#####

def info_init():
    # Semaphore for information log file critical ressource
    try:
        # Creating semaphore
        logMessage('[INFO_LOGGER]: Creating semaphore', STDOUT_FILE, 2)
        info_semaphore = pos.Semaphore('/Info_Logger', pos.O_CREAT|pos.O_EXCL, initial_value=1)
        logMessage('[INFO_LOGGER]: Created semaphore', STDOUT_FILE, 2)

    except pos.ExistentialError:
        # Semaphore already created
        logMessage('[INFO_LOGGER]: Semaphore already created', STDOUT_FILE, 2)
        info_semaphore = pos.Semaphore('/Info_Logger', pos.O_CREAT)
        logMessage('[INFO_LOGGER]: Using existing semaphore', STDOUT_FILE, 2)

    return info_semaphore


def error_init():
    # Semaphore for error log file critical ressource
    #error_semaphore = None
    try:
        # Creating semaphore
        logMessage('[ERROR_LOGGER]: Creating semaphore', STDOUT_FILE, 2)
        error_semaphore = pos.Semaphore('/Error_Logger', pos.O_CREAT|pos.O_EXCL, initial_value=1)
        logMessage('[ERROR_LOGGER]: Created semaphore', STDOUT_FILE, 2)

    except pos.ExistentialError:
        # Semaphore already created
        logMessage('[ERROR_LOGGER]: Semaphore already created', STDOUT_FILE, 2)
        error_semaphore = pos.Semaphore('/Error_Logger', pos.O_CREAT)
        logMessage('[ERROR_LOGGER]: Using existing semaphore', STDOUT_FILE, 2)

    return error_semaphore


# TODO: Kill (clean semaphore)