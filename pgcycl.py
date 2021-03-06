#! /usr/bin/python
# -*- coding: utf8 -*-

#####
# Imports
#####

import sys
import os
import posix_ipc as pos

from logger import logInfo
from logger import logError
from os.path import expanduser

#####
# Global var declaration
#####

FBATCH = expanduser('~') + '/.fbatch'


#####
# Functions definition
#####


# TODO: Better man page
def printUsage():
    print('Usage : pgcycl man page\n'
          'PGCYCL\n'
          '     Used to manage programs launched by the daemon gobatch \n\n'
          ''
          'SYNOPSIS\n'
          '     pgcycl add command hour minute [-d day]\n\n'
          ''
          'DESCRIPTION\n'
          '     Specifiy informations on the date of execution of a command\n\n'
          ''
          'OPTIONS\n'
          '     add\n'
          '         -d, --daily\n'
          '             Planned recurrent execution on a daily basis\n\n'
          ''
          '         -w, --weekly\n'
          '             Planned recurrent execution on a weekly basis\n\n'
          ''
          '         -m, --monthly\n'
          '             Planned recurrent execution on a monthly basis\n\n'
          ''
          '         -y, --yearly\n'
          '             Planned recurrent execution on a yearly basis\n\n'
          '     del\n'
          '         Lists all recurrent tasks added to fbatch and allow\n'
          '         you to choose which one to delete\n'
          '     list\n'
          '         Lists all recurrent tasks added to fbatch'
          ''
          '     help\n'
          '         Display this man page')
    exit(2)


def getinput():
    try:
        x = input()
    except NameError as e:
        for pname, pvalue in vars(e).iteritems():
            print((pname, ": ", pvalue))
        error_string = str(e)
        x = error_string[error_string.index('\'') + 1: error_string.rfind('\'')]
    return x


def verifyParam(name, value, inf_bound, sup_bound):
    if value < inf_bound or value > sup_bound:
        logError(
            '[PGCYCL]: Error, {} must be in the range [{},{}], given : {}'.format(name, inf_bound, sup_bound, value),
            True, True)
        exit(2)
    else:
        return value


def writeToFBatch(**kwargs):
    return '{minute}\t{hour}\t{day}\t{month}\t{frequency}\t{command}'.format(**kwargs)


def addNewTask(args):
    #####
    # Var initialization
    #####

    index = 0  # Index of the first optional arg
    arg = 0  # Current argument

    data = {'command': '', 'minute': 0, 'hour': 0, 'frequency': '0', 'day': '0', 'month': '0'}

    args_length = len(args)

    if args_length < 3:
        printUsage()

    else:
        data.update({'command': args[index]})
        file = open(FBATCH, 'a')
        try:
            index += 1
            minute = verifyParam('minute', int(args[index]), 0, 59)
            data.update({'minute': minute})
            index += 1
            hour = verifyParam('hour', int(args[index]), 0, 23)
            data.update({'hour': hour})
            index += 1

            if index < args_length:
                arg = args[index]
            else:
                arg = '-d'

            index += 1

            if arg == '-d' or arg == '--daily':
                data.update({'frequency': 'daily'})

            elif arg == '-w' or arg == '--weekly':
                day = verifyParam('day of the week', args[index], 1, 7)
                data.update({'frequency': 'weekly', 'day': day})

            elif arg == '-m' or arg == '--monthly':
                day = verifyParam('day', (args[index]), 1, 31)
                data.update({'frequency': 'monthly', 'day': day})

            elif arg == '-y' or arg == '--yearly':
                month = verifyParam('month', int(args[index]), 1, 12)
                index += 1
                day = verifyParam('day', int(args[index]), 1, 31)
                data.update({'frequency': 'yearly', 'day': day, 'month': month})

            else:
                printUsage()

            content = writeToFBatch(**data)
            if os.stat(FBATCH).st_size != 0:
                content = '\n' + content
            file.write(content)
            file.flush()
            logInfo(
                '[PGCYCL]: Added command "{command}" will be executed at : {hour}:{minute} on a {frequency} basis'.format(
                    **data), True)

        except IndexError:
            logError('[PGCYCL]: Error : No value behind parameter : {}'.format(arg), True, True)
            exit(2)

        except ValueError:
            logError('[PGCYCL]: Parameter {} needs integer value, given {}'.format(arg, args[index]), True, True)
            exit(2)

        finally:
            file.close()


def listAllTasks(withIndex):
    file = open(FBATCH, 'r')
    lines = file.readlines()
    output = []
    if withIndex:
        output = 'Id\tMinute\tHour\tDay\tMonth\tFrequency\tCommand\n'

    index = 0
    for line in lines:
        index += 1
        if withIndex:
            output += '{}\t{}'.format(index, line)
        else:
            output.append(line)

    file.close()

    return output


def deleteTask():
    tasks = listAllTasks(True)
    lines = listAllTasks(False)
    tasks_count = len(lines)

    if tasks_count == 0:
        logError('[PGCYCL]: No tasks in fbatch file for the moment, add some first', True, False)
        exit(0)

    print(tasks)
    print('Give id of the tasks you which to delete (q to exit) ')
    index = getinput()

    if index == 'q' or index == '' or index == 'exit':
        logInfo('[PGCYCL]: User aborted deletion', True)
        exit(0)

    try:
        index = int(index)

    except ValueError:
        logError('[PGCYCL]: Id invalid, given "{}"'.format(index), True, True)
        exit(1)

    if index > tasks_count:
        logError('[PGCYCL]: Id not found, "{}" given, only {} tasks'.format(index, tasks_count), True, True)
        exit(1)

    elif 0 < index <= tasks_count:
        line = lines[index - 1]
        output = 'Deleting tasks {} :\n'.format(index)
        output += 'Minute\tHour\tDay\tMonth\tFrequency\tCommand\n'
        output += line
        output += '\nAre you sure ? (y/N) '

        try:
            print(output)
            answer = getinput()

            if not answer or answer == 'n':
                logInfo("User aborted deletion", True)
                exit(0)

            elif answer == 'y':
                lines.pop(index - 1)
                last = len(lines) - 1
                lines[last] = lines[last].rstrip()

                # Resets file content
                open(FBATCH, 'w').close()

                fbatch_file = open(FBATCH, 'a')
                lines = ''.join(lines)
                fbatch_file.write(lines)
                fbatch_file.close()
                logInfo('[PGCYCL]: Recurrent task deleted successfully', True)

        except SyntaxError:
            logError('[PGCYCL]: Error : Answer invalid', True, True)
            exit(1)

    else:
        logError('[PGCYCL]: Id not valid', True, True)
        exit(1)


def P():
    semaphore = pos.Semaphore('/FBatch_Semaphore', pos.O_CREAT)
    try:
        logInfo('[PGCYCL]: Acquiring semaphore', False)
        semaphore.acquire()
        logInfo('[PGCYCL]: Semaphore acquired', False)

    except:
        semaphore.release()


def V():
    semaphore = pos.Semaphore('/FBatch_Semaphore', pos.O_CREAT)
    try:
        logInfo('[PGCYCL]: Releasing semaphore', False)
        semaphore.release()
        logInfo('[PGCYCL]: Semaphore released', False)

    except:
        semaphore.release()


def useSemaphore(func, args, update_required):
    res = None
    try:
        P()  # semaphore.acquire()
        if args is None:
            res = func()
        else:
            res = func(args)

    finally:
        V()  # semaphore.release()
        if update_required:
            try:
                logInfo('[GOBATCH]: Releasing semaphore', False)
                pos.Semaphore('/FBatch_Updated', pos.O_CREAT).release()
                logInfo('[GOBATCH]: Semaphore released', False)

            finally:
                pos.Semaphore('/FBatch_Updated', pos.O_CREAT).release()
    return res


def createSemaphore():
    try:
        # Creating semaphore
        logInfo('[PGCYCL]: Creating semaphore', False)
        pos.Semaphore('/FBatch_Semaphore', pos.O_CREAT | pos.O_EXCL, initial_value=1)
        logInfo('[PGCYCL]: Created semaphore', False)

    except pos.ExistentialError:
        # Semaphore already created
        logInfo('[PGCYCL]: Semaphore already created', False)
        pos.Semaphore('/FBatch_Semaphore', pos.O_CREAT)
        logInfo('[PGCYCL]: Using existing semaphore', False)


#####
# Main execution
#####

argv = sys.argv

if len(argv) >= 2:

    param = argv[1]

    if param == 'help' or param == '-h' or param == '?':
        printUsage()

    if param == 'list':
        print(useSemaphore(listAllTasks, True, False))

    elif param == 'add':
        useSemaphore(addNewTask, argv[2:], True)

    elif param == 'del':
        useSemaphore(deleteTask, None, True)

    else:
        logError('[PGCYCL]: Command not found', True, True)
        printUsage()

'''
deleteTask()
addNewTask(['command', 5, 39, '-d'])
addNewTask(['echo test', 7, 42, '-w', 3])
addNewTask(['error', 12, 1, '-m', 21])
addNewTask(['exit(1)', 3, 34, '-y', 9, 5])
addNewTask(['drop database', 23, 6])
'''
