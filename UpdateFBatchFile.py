# -*- coding: utf8 -*-

#####
# Imports
#####

import sys
import calendar

#####
# Global Constants declaration
#####
FBATCH = 'FBatch'

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
          '         Lists all recurent tasks added to FBatch')
    exit(2)

def verifyParam(name, value, inf_bound, sup_bound):
    if value < inf_bound or value > sup_bound:
        print('Error, {} must be in the range [{},{}], given : {}'.format(name, inf_bound, sup_bound, value))
        exit(2)
    else:
        return value

def add(args):
    #####
    # Var initialization
    #####

    index = 0               # Index of the first optional arg
    arg = 0                 # Current argument

    minute = 0              # Default minute of execution
    hour = 0                # Default hour of execution
    month = 0               # Default month of executing
    day_of_week = 0         # Default day of the week execution
    day = 0                 # Default day of execution

    rec_type = 1            # Period type 1 = day, 2 = week, 3 = month
    recurrency = 'day'      # Describer of the choosen period of time
    command = ''            # Command that will be periodically executed

    args_length = len(args)

    if args_length < 3:
        printUsage()

    else:
        command = args[index]
        try:
            index += 1
            hour = verifyParam('hour', int(args[index]), 0, 23)
            index += 1
            minute = verifyParam('minute', int(args[index]), 0, 59)

            if args_length > index:
                arg = args[index]

            # FIXME: Put out list(...) arround calendar
            if arg == '-d' or arg == '--daily' or args_length == index:
                rec_type = 1
                recurrency = 'day'

            elif arg == '-w' or arg == '--weekly':
                rec_type = 2
                index += 1
                day_of_week = verifyParam('day of the week', args[index], 1, 7)
                recurrency = list(calendar.day_name)[day_of_week - 1]

            elif arg == '-m' or arg == '--monthly':
                rec_type = 3
                index += 1
                day = verifyParam('day', (args[index]), 1, 31)
                month_name = list(calendar.month_name)[month - 1]
                recurrency = 'month on the {}'.format(day)

            elif arg == '-y' or arg == '--yearly':
                rec_type = 4
                index += 1
                month = verifyParam('month', int(args[index]), 1, 12)
                index += 1
                day = verifyParam('day', int(args[index]), 1, 31)
                month_name = list(calendar.month_name)[month - 1]
                recurrency = 'year on the {} of {}'.format(day, month_name)

            else:
                printUsage()

            print('Your command "{}" will be executed at : {}:{} each {}'.format(command, hour, minute, recurrency))


        except IndexError:
            print('Error : No value behind parameter : {}'.format(arg))

        except ValueError:
            print('Parameter {} needs integer value, given {}'.format(arg, args[index]))

'''
add(sys.argv)
add(['command', 5, 39, '-d'])
add(['echo test', 7, 42, '-w', 3])
add(['error', 12, 01, '-m', 21])
add(['exit(1)', 3, 34, '-y', 9, 5])
add(['drop database', 23, 54])
add(['drop database', 23, 61])'''


def list():
    file = open(FBATCH, 'r')
    lines = file.readlines()
    print('Batched   Command   Frequency   Minute   Hour   Day   Month')
    index = 0
    for line in lines:
        index += 1
        print ('{} : {}'.format(index, line))
    file.close()

def delete(args):
    print('del')


#####
# Main execution
#####

argv = sys.argv

if argv[1] == 'list':
    # TODO: Sémaphore
    list()

elif argv[1] == 'add':
    # TODO: Sémaphore
    add(argv[2, len(argv)])

elif argv[1] == 'del':
    # TODO: Sémaphore
    delete(argv[2, len(argv)])

else:
    printUsage()