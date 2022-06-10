#!/usr/bin/python3
#
#   run.py
#
#     python class for an experiment in object-oriented ai
#     
#
#   TDORSEY  2022-06-08  Split from groc.py

import sys
import world

def main():   
  thisWorld = world.World(1800,800)
  thisWorld.start(sys.argv)
  while thisWorld.keepRunning():
    thisWorld.tick()
  thisWorld.end()
            
if __name__ == '__main__':
    main()
