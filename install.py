#! /usr/bin/python3
# -*- coding: utf8 -*-

import os
import time

# Check if script is start with root rights
if os.geteuid() != 0:
    exit('You need to have root privileges to run this script. Use \'sudo ./install.py\'.')

# Title
print('----- ProcessManager install ----- \n')

time.sleep(1)

# Get path of gobatch file
processManagerPath = input("Please enter the path (absolute) where the ProcessManager folder is located "
                           "(like /home/user/ProcessManager) : ")

# Check is directory exists
directoryExists = os.path.isdir(processManagerPath)

if not directoryExists:
    exit('Error : directory does not exists.')

# Copy ProcessManager directory into /usr/local/bin/
print('Copy sources into /usr/local/bin..... \n')
os.system('cp -r ' + processManagerPath + ' /usr/local/bin')

fileContent = '[Unit] \n' \
              'Description=ProcessManager \n' \
              'After=tlp-init.service \n\n' \
              '' \
              '[Service] \n' \
              'Type=oneshot \n' \
              'RemainAfterExit=no \n' \
              'ExecStart=/usr/bin/python /usr/local/bin/ProcessManager/gobatch.py \n\n' \
              '' \
              '[Install] \n' \
              'WantedBy=multi-user.target'

print('Create the service file..... \n')
file = open('/etc/systemd/system/processManager.service', 'w')
file.write(fileContent)
file.close()

# reload daemons list
print('Reload the daemons list..... \n')
os.system('sudo systemctl daemon-reload')

print('- To start the daemon use : systemctl start processManager.service')
print('- To enable the daemon at the startup use : systemctl enable processManager.service')
