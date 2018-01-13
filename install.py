#! /usr/bin/python3
# -*- coding: utf8 -*-

import os
import time

# Title
print('---------- ProcessManager install ----------\n\n')

# get processManager directory
time.sleep(1)
print('Get the ProcessManager directory path .....')
processManagerPath = os.getcwd()

# Copy fbatch file to ~/.fbatch
time.sleep(1)
print('Create .fbatch to /home/user/ .....')
os.system('cp ' + processManagerPath + '/fbatch ~/.fbatch')

# Create log files
time.sleep(1)
print('Create log files into ~/.processManager_stdout.log and ~/.processManager_stderr.log .....')
os.system('touch ~/.processManager_stdout.log')
os.system('touch ~/.processManager_stderr.log \n\n')

print('---------- Installation done ---------')
