#! /usr/bin/python3
# -*- coding: utf8 -*-

STDOUT_FILE = 'STDOUT'
STDERR_FILE = 'STDERR'


def logMessage(message, file):
    info_file = open(file, 'a')
    info_file.write(file)
    info_file.close()


def logInfo(info_message, stdout_log):
    logMessage(info_message, STDOUT_FILE)
    if stdout_log:
        print(info_message)


def logError(error_message, stdout_log):
    logMessage(error_message, STDERR_FILE)
    if stdout_log:
        print(error_message)