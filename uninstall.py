#! /usr/bin/python
# -*- coding: utf8 -*-

import os
import time

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
