#!/usr/bin/python
#
# putpipe.py
#
from subprocess import *
import os

FIFO_PATH = '/tmp/pipe'

if os.path.exists(FIFO_PATH):
  os.unlink(FIFO_PATH)

if not os.path.exists(FIFO_PATH):
  os.mkfifo(FIFO_PATH, 0o600)
  wpipe = open(FIFO_PATH, 'w', newline='\n')
  for i in range(10):
    msg = "Hello " + str(i) + "\n"
    wpipe.write(msg)
    print(msg)
  wpipe.close()

if os.path.exists(FIFO_PATH):
  os.unlink(FIFO_PATH)

