#!/usr/bin/python3
#
#   run.py
#
#     python class for an experiment in object-oriented ai
#     
#
#   TDORSEY  2016-10-16  Created
#   TDORSEY  2016-10-16  Saving the world
#   TDORSEY  2016-10-16  Retrieving saved world
#   TDORSEY  2016-10-16  Improved class and function structure
#   TDORSEY  2016-10-17  Rendering via pygame
#   TDORSEY  2016-10-22  Some form of pygame hell
#   TDORSEY  2022-05-01  Refactor groc into groc.py class file
#   TDORSEY  2022-05-02  Move initialization code into main
#   TDORSEY  2022-05-20  Combine groc.py and run.py
#   TDORSEY  2022-05-26  Main loop simplified
#   TDORSEY  2022-06-08  Split from groc.py

import sys
import world

def main():   
  thisWorld = world.World(1920,930)
  thisWorld.start(sys.argv)
  while thisWorld.keepRunning():
    thisWorld.tick()
  thisWorld.end()
            
if __name__ == '__main__':
    main()
