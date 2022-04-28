#!/usr/bin/python
#
# putpipe.py
#
# TDORSEY 2022-04-28  Created
#
import os, sys, time

FIFO_PATH = '/tmp/pipe'

try:
  print("about to try")
  rpipe = open(FIFO_PATH, "r")
except Exception as e:
  print(e)
  exit()

line = ""
print ("Opened pipe")
while True:
  msg = rpipe.read(1)
  if msg == '\n':
    print("newline")
    print(line)
    line = ""
  else:
    line = line + msg
  if len(msg) != 1:
    print("Sender Terminated")
    break
rpipe.close()
