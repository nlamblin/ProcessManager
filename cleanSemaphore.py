#! /usr/bin/python3
# -*- coding: utf8 -*-

import posix_ipc as pos

pos.Semaphore('/Info_Logger', pos.O_CREAT).unlink()
pos.Semaphore('/Error_Logger', pos.O_CREAT).unlink()
semaphore = pos.Semaphore('/FBatch_Semaphore', pos.O_CREAT).unlink()
exit()
