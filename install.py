#! /usr/bin/python3
# -*- coding: utf8 -*-

import os
import time

# Check if script is start with root rights
if os.geteuid() != 0:
    exit('You need to have root privileges to run this script. Use \'sudo ./install.py\'.')

# Title
print('---------- ProcessManager install ----------\n\n')

# get processManager directory
time.sleep(1)
print('Get the ProcessManager directory path.....\n')
processManagerPath = os.getcwd()

# Copy ProcessManager directory into /usr/local/bin/
time.sleep(1)
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

# Reload daemons list
time.sleep(1)
print('Reload the daemons list..... \n\n\n')
os.system('systemctl daemon-reload')

manual = '---------- Installation done ----------\n\n' \
         'Some infos: \n\n' \
         '       - To start the daemon use:                  systemctl start processManager.service \n' \
         '       - To kill the daemon use:                   systemctl kill processManager.service \n' \
         '       - To restart the daemon use:                systemctl restart processManager.service \n' \
         '       - To check is the daemon is active use:     systemctl is-active processManager.service \n' \
         '       - To check ths status of the daemon use:    systemctl status processManager.service \n' \
         '       - To enable the daemon at the startup use:  systemctl enable processManager.service \n' \
         '       - To disable the daemon at the startup use: systemctl disable processManager.service \n' \

print(manual)
