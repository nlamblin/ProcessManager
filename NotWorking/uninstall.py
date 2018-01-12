#! /usr/bin/python
# -*- coding: utf8 -*-

import os
import time

print('---------- Uninstallation start ----------\n\n')


# Check if script is start with root rights
if os.geteuid() != 0:
    exit('You need to have root privileges to run this script. Use \'sudo ./uninstall.py\'.')

# kill the service
print('Kill ProcessManager service.....')
os.system('systemctl kill processManager.service')

# remove the service file to /etc/systemd/system/
time.sleep(1)
print('Remove the service file.....')
os.system('rm /etc/systemd/system/processManager.service')

# remove ProcessManager to /usr/local/bin
time.sleep(1)
print('Remove sources of ProcessManager.....')
os.system('rm -r /usr/local/bin/ProcessManager')

# remove log and fbatch files
time.sleep(1)
print('Remove log files .....')
os.system('rm ~/.processManager_stdout.log')
os.system('rm ~/.processManager_stderr.log')
os.system('rm ~/.fbatch')

print('\n\n ---------- Uninstallation done ----------')
