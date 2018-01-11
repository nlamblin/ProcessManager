#! /usr/bin/python3
# -*- coding: utf8 -*-

# TODO: Change during install
STDOUT_FILE = 'STDOUT'
STDERR_FILE = 'STDERR'


def logMessage(message, file, is_fatal):
    if is_fatal == 0:
        message = 'FATAL: ' + message

    elif is_fatal == 1:
        message = 'WARNING: ' + message

    elif is_fatal == 2:
        message = 'INFO: ' + message

    info_file = open(file, 'a')
    info_file.write(file)
    info_file.close()


def logInfo(info_message, stdout_log):
    logMessage(info_message, STDOUT_FILE, 2)
    if stdout_log:
        print(info_message)


def logError(error_message, stdout_log, is_fatal):
    logMessage(error_message, STDERR_FILE, is_fatal)
    if stdout_log:
        print(error_message)