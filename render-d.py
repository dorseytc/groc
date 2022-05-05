#!/usr/bin/python
#
# render-d.py
#
# text based "render" of a groc world. 
# receives messages from world.py containing instructions on
# groc movement.  Other versions might render graphically, 
# this one, for debugging purposes, reveals the contents of the 
# messages piped between "world" and the renderer
#
# TDORSEY 2022-04-28  Created
# TDORSEY 2022-05-01  Renamed render-d to denote its roles as a
#                     debugging tool
# TDORSEY 2022-05-02  Show received line message even if '\n'
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
    print("Line: ", line)
    line = ""
    msgcount += 1
  else:
    line = line + msg
  if len(msg) != 1:
    print("Sender Terminated")
    break
print("Messages received: ", msgcount)
rpipe.close()
