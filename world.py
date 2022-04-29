#!/usr/bin/python
#
# world.py
#
# TDORSEY 2022-04-28  Created
#
import os, sys, time

pipe = "/tmp/grocpipe"
try:
  print("Looking for the pipe")
  rpipe = open(pipe, "r")
except Exception as e:
  print(e)
  print("Start groc.py first")
  exit()

line = ""
msgcount = 0
print ("Opened pipe")
while True:
  msg = rpipe.read(1)
  if msg == '\n':
    print(line)
    line = ""
    msgcount += 1
  else:
    line = line + msg
  if len(msg) != 1:
    print("Sender Terminated")
    break
print("Messages received: ", msgcount)
rpipe.close()
