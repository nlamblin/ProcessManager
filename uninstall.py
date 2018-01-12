#! /usr/bin/python
# -*- coding: utf8 -*-

import os
import time

print('---------- Uninstallation start ----------\n\n')

# remove log file
time.sleep(1)
print('Remove log files .....')
os.system('rm ~/.processManager_stdout.log')
os.system('rm ~/.processManager_stderr.log')
os.system('rm ~/.fbatch')

# Clear semaphore
os.system('python ' + os.getcwd() + '/cleanSemaphore.py')

print('\n\n ---------- Uninstallation done ----------')
