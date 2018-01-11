#! /usr/bin/python3
# -*- coding: utf8 -*-

#####
# Imports
#####

import sys
import calendar
import posix_ipc as pos

from gobatch import updateString

#####
# Global Constants declaration
#####
FBATCH = 'FBatch'

#####
# Semaphore declaration
#####
try:
    # Creating semaphore
    print('Creating semaphore')
    semaphore = pos.Semaphore('/S1', pos.O_CREAT|pos.O_EXCL, initial_value=1)
    print('Created semaphore')

except pos.ExistentialError:
    # Semaphore already created
    print('Semaphore already created')
    semaphore = pos.Semaphore('/S1', pos.O_CREAT)

# semaphore.unlink()
# exit()

#####
# Functions definition
#####


# TODO: FIXME: Better man page
def printUsage():
    print('Usage : pgcycl man page\n'
          'PGCYCL\n'
          '     Used to manage programs launched by the daemon gobatch\n\n'
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
          '         Lists all recurrent tasks added to FBatch and allow\n'
          '         you to choose which one to delete\n'
          '     list\n'
          '         Lists all recurrent tasks added to FBatch'
          ''
          '     help\n'
          '         Display this man page')
    exit(2)


def verifyParam(name, value, inf_bound, sup_bound):
    if value < inf_bound or value > sup_bound:
        print('Error, {} must be in the range [{},{}], given : {}'.format(name, inf_bound, sup_bound, value))
        exit(2)
    else:
        return value


def writeToFBatch(**kwargs):
    return '{minute}\t{hour}\t{day}\t{month}\t{frequency}\t{command}\n'.format(**kwargs)


def addNewTask(args):
    #####
    # Var initialization
    #####

    index = 0               # Index of the first optional arg
    arg = 0                 # Current argument

    data = {'command':'', 'minute':0, 'hour':0, 'frequency':'0', 'day':'0', 'month':'0'}

    args_length = len(args)

    if args_length < 3:
        printUsage()

    else:
        data.update({'command': args[index]})
        file = open(FBATCH, 'a')
        try:
            index += 1
            hour = verifyParam('hour', int(args[index]), 0, 23)
            data.update({'hour':hour})
            index += 1
            minute = verifyParam('minute', int(args[index]), 0, 59)
            data.update({'minute': minute})
            index += 1

            if index < args_length:
                arg = args[index]
            else:
                arg = '-d'

            index += 1

            if arg == '-d' or arg == '--daily':
                frequency = 'day'
                data.update({'frequency':'daily'})

            elif arg == '-w' or arg == '--weekly':
                day = verifyParam('day of the week', args[index], 1, 7)
                frequency = list(calendar.day_name)[day - 1]
                data.update({'frequency':'weekly', 'day':day})

            elif arg == '-m' or arg == '--monthly':
                day = verifyParam('day', (args[index]), 1, 31)
                frequency = 'month on the {}'.format(day)
                data.update({'frequency':'monthly', 'day':day})

            elif arg == '-y' or arg == '--yearly':
                month = verifyParam('month', int(args[index]), 1, 12)
                index += 1
                day = verifyParam('day', int(args[index]), 1, 31)
                month_name = list(calendar.month_name)[month - 1]
                frequency = 'year on the {} of {}'.format(day, month_name)
                data.update({'frequency':'yearly', 'day':day, 'month':month})

            else:
                printUsage()

            file.write(writeToFBatch(**data))
            file.flush()
            updateString()
            print('Added command "{command}" executed at : {hour}:{minute} on a {frequency} basis'.format(**data))

        except IndexError:
            print('Error : No value behind parameter : {}'.format(arg))

        except ValueError:
            print('Parameter {} needs integer value, given {}'.format(arg, args[index]))

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
        print('No tasks in FBatfh file for the moment, add some first')
        exit(0)

    print(tasks)
    index = raw_input('Give id of the tasks you which to delete (q to exit)')

    if index == 'q' or index == '':
        print("User aborted deletion")
        exit(0)

    try:
        index = int(index)

    except ValueError:
        print('Id invalid, given "{}"'.format(index))
        exit(1)

    if index > tasks_count:
        print('Id not found, "{}" given, only {} tasks'.format(index, tasks_count))
        exit(1)

    elif 0 < index <= tasks_count:
        line = lines[index - 1]
        output = 'Deleting tasks {} :\n'.format(index)
        output += 'Minute\tHour\tDay\tMonth\tFrequency\tCommand\n'
        output += line
        output += '\nAre you sure ? (y/N)'
        print(output)

        try:
            answer = raw_input(output)

            if not answer or answer == 'n':
                print("User aborted deletion")
                exit(0)

            elif answer == 'y':
                lines.pop(index - 1)

                # Resets file content
                open(FBATCH, 'w').close()

                fbatch_file = open(FBATCH, 'a')
                lines = ''.join(lines)
                fbatch_file.write(lines)
                fbatch_file.close()
                updateString()
                print('record deleted successfully')

        except SyntaxError:
            print('Error : Answer invalid')

    else:
        print('Id not valid')
        exit(1)


def P():
    print('Acquiring semaphore')
    semaphore.acquire()
    print('Semaphore acquired')


def V():
    print('Releasing semaphore')
    semaphore.release()
    print('Semaphore released')


#####
# Main execution
#####

argv = sys.argv

if argv[1] == 'list':
    print(listAllTasks(True))

elif argv[1] == 'add':
    # semaphore.acquire()
    P()
    try:
        addNewTask(argv[2, len(argv) - 1])

    finally:
        V()
        #semaphore.release()

elif argv[1] == 'del':
    # semaphore.acquire()
    P()
    try:
        deleteTask()

    finally:
        V()
        # semaphore.release()

elif argv[1] == 'help':
    printUsage()

else:
    print('Command not found')
    printUsage()

'''
addNewTask(['drop database', 23, 54])
addNewTask(['command', 5, 39, '-d'])
addNewTask(['echo test', 7, 42, '-w', 3])
addNewTask(['error', 12, 1, '-m', 21])
addNewTask(['exit(1)', 3, 34, '-y', 9, 5])
addNewTask(['drop database', 23, 6])
'''