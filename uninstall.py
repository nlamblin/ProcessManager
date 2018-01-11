#! /usr/bin/python
# -*- coding: utf8 -*-

import os

# kill the service
os.system('systemctl kill processManager.service')

# remove the service file to /etc/systemd/system/
os.system('rm /etc/systemd/system/processManager.service')

# remove ProcessManager to /usr/local/bin
os.system('rm -r /usr/local/bin/ProcessManager')
