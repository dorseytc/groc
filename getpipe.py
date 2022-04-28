#!/usr/bin/python
#
# putpipe.py
#
import os, sys

FIFO_PATH = '/tmp/pipe'

try:
  print("about to try")
  rpipe = open(FIFO_PATH, "r")
except Exception as e:
  print (e)
  sys.exit()
while True:
  msg = rpipe.read(1)
  if msg == '\n':
    print("newline")
  else:
    print(msg) 
  if len(msg) != 1:
    print("Sender Terminated")
    break
rpipe.close()
