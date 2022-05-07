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
# TDORSEY 2022-05-05  Debug missing messages, use world constants
# TDORSEY 2022-05-07  import and pydoc enabled, __main__ protected
#           
#
import groc
import os
import sys

def main():
  pipe = groc.World.PIPENAME
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
    if msg == groc.World.NEWLINE:
      msgcount += 1
      print("Msg ", msgcount, line)
      line = ""
    else:
      line = line + msg
    if len(msg) != 1:
      print("Sender Terminated")
      break
  print("Messages received: ", msgcount)
  rpipe.close()


if __name__ == '__main__':
  main()
