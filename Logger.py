#! /usr/bin/python3
# -*- coding: utf8 -*-

# TODO: Change during install
STDOUT_FILE = 'STDOUT'
STDERR_FILE = 'STDERR'


def logMessage(message, file, is_fatal):
    if is_fatal:
        message = 'FATAL: ' + message

    else:
        message = 'WARNING: ' + message

    info_file = open(file, 'a')
    info_file.write(file)
    info_file.close()


def logInfo(info_message, stdout_log, is_fatal):
    logMessage(info_message, STDOUT_FILE, is_fatal)
    if stdout_log:
        print(info_message)


def logError(error_message, stdout_log, is_fatal):
    logMessage(error_message, STDERR_FILE, is_fatal)
    if stdout_log:
        print(error_message)