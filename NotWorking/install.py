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
print('Get the ProcessManager directory path .....')
processManagerPath = os.getcwd()

# Copy ProcessManager directory into /usr/local/bin/
time.sleep(1)
print('Copy sources into /usr/local/bin/ .....')
os.makedirs('/usr/local/bin/ProcessManager')
os.system('cp ' + processManagerPath + '/*.py /usr/local/bin/ProcessManager/')
os.system('cp ' + processManagerPath + '/fbatch ~/.fbatch')

# Create log files
time.sleep(1)
print('Create log files into ~/.processManager_stdout.log and ~/.processManager_stderr.log .....')
os.system('touch ~/.processManager_stdout.log')
os.system('touch ~/.processManager_stderr.log')

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

time.sleep(1)
print('Create the service file into /etc/systemd/system/ .....')
file = open('/etc/systemd/system/processManager.service', 'w')
file.write(fileContent)
file.close()

# Reload daemons list
time.sleep(1)
print('Reload the daemons list .....')
os.system('systemctl daemon-reload')

# Clear semaphore
os.system('python /usr/local/bin/ProcessManager/cleanSemaphore.py')

# Give rights
time.sleep(1)
print('Give rights to files ..... \n\n')
os.chmod('/usr/local/bin/ProcessManager', 0o777)
os.system('chmod 744 /usr/local/bin/ProcessManager/')
os.system('chmod 644 ~/.fbatch')
os.system('chmod 644 ~/.processManager_stdout.log')
os.system('chmod 644 ~/.processManager_stderr.log')
os.system('chmod 744 /etc/systemd/system/processManager.service')

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
