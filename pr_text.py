#!/usr/bin/python
#
# pr_text
#
# Pipe Reader for groc using Text output
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
# TDORSEY 2022-05-16  removed unused imports
# TDORSEY 2022-05-22  Converted to work with grr_pipe framework
#           
#
import groc
import grr_pipe

def main():
  pipe = grr_pipe.Renderer.PIPENAME
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
