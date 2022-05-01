#!/usr/bin/python
#
#   world
#
#      world class for groc, an object-oriented experiment in ai
#
#   TDORSEY     2022-05-01  Created world.py by refactoring
#                           groc.py into "class-specific" groc.py
#                           Remainder becomes world.py

import datetime 
import logging
import math
import numpy 
import os
import sys
import groc

# limiters

K_GROC_LIMIT = 2
K_ITER_LIMIT = 1000

# world dimensions
K_MAXX = 1800
K_MAXY = 800

# cardinal directions
K_NONE = 0 
K_NORTH = 1
K_EAST = 2
K_SOUTH = 3
K_WEST = 4

# Init Code
K_PIPE_NAME = "/tmp/grocpipe"
K_GROCFILE = "grocfile.dat"
K_GROCLOG = "groclog.log"
K_FIELDSEP = '|'
K_NEWLINE = "\n"
print ("start render to continue")
if os.path.exists(K_PIPE_NAME):
  os.unlink(K_PIPE_NAME)
if not os.path.exists(K_PIPE_NAME):
  os.mkfifo(K_PIPE_NAME, 0o600)
  wpipe = open(K_PIPE_NAME, 'w', newline=K_NEWLINE)
#Command Line Arguments
numArgs = len(sys.argv)
print(sys.argv)
if numArgs > 3:
  p_grocFile = sys.argv[3] 
else:
  p_grocFile = K_GROCFILE
  
if numArgs > 2:
  p_iterations = int(sys.argv[2])
else:
  p_iterations = K_ITER_LIMIT

if numArgs > 1:
  p_numGrocs = int(sys.argv[1])
else:
  p_numGrocs = K_GROC_LIMIT
  
print("p_numGrocs: ", p_numGrocs) 
print("p_iterations: ", p_iterations)
print("p_grocFile: ", p_grocFile)

Log_Format = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename = K_GROCLOG, 
                    filemode = "w", 
                    format = Log_Format, 
                    level = logging.DEBUG)
logger = logging.getLogger()

# main

def main():   
  grocList = [] 
  # 
 
  #Reading the world
  #
  if os.path.exists(p_grocFile):
    savedFile = open(p_grocFile, "r")
    grocsRead = 0 
    line = savedFile.readline()
    while line: 
      grocsRead += 1
      list = line.split(K_FIELDSEP)
      birthdatetime = datetime.datetime.strptime(list[6].rstrip(K_NEWLINE), 
                                               "%Y-%m-%d %H:%M")        
      newGroc = groc.Groc(list[0],list[1], list[2], 
                          list[3], list[4], list[5], 
                          birthdatetime)
      newGroc.identify()
      newGroc.locate()
      wpipe.write(str(newGroc.id) + "," + 
                          str(0) + "," + str(0) + "," + 
                          str(newGroc.x) + "," + str(newGroc.y) + K_NEWLINE)
      grocList.append(newGroc)
      line = savedFile.readline()
    savedFile.close()      
  else:
    grocsRead = 0
  if grocsRead < p_numGrocs:
    for count in range(0, (p_numGrocs - grocsRead)):
      name = 'G' + str(count)
      newGroc = groc.Groc(name, 'happy', 'green')
      newGroc.identify()
      newGroc.introduce()
      newGroc.locate()
      wpipe.write(str(newGroc.id) + "," + 
                  str(0) + "," + str(0) + "," + 
                  str(newGroc.x) + "," + str(newGroc.y) + K_NEWLINE)
      grocList.append(newGroc)
    
  running = True
  counter = 0 
  while running:
    counter += 1
    movingCount = 0 
    for thisGroc in grocList:   
            logger.debug ("*** GROC: " + str(thisGroc.id) + " IsMoving? " + 
                          str(thisGroc.isMoving) + " Direction? " + 
                          str(thisGroc.direction) + " " + str(thisGroc.x) + 
                          "," + str( thisGroc.y))
        
            least_zdist = K_MAXX + K_MAXY
            nearestx = K_MAXX
            nearesty = K_MAXY 
            for anotherGroc in grocList:
                if anotherGroc.id == thisGroc.id:
                    logger.debug ("Groc " + str(thisGroc.id) + 
                                  " skip myself when evaluating density")
                else: 
                    xdiff = abs(thisGroc.x - anotherGroc.x) 
                    ydiff = abs(thisGroc.y - anotherGroc.y)
                    zdist = math.sqrt((xdiff ** 2) + (ydiff ** 2))
                    logger.debug("Groc " + str(anotherGroc.id) + 
                       " is " + str(zdist) + " away")
                    if zdist < least_zdist:
                      least_zdist = zdist
                      nearestx = anotherGroc.x
                      nearesty = anotherGroc.y
            if least_zdist < 20:  
              logger.debug("Groc " + str(thisGroc.id) + 
                           " is happy to have friends")
              thisGroc.isMoving = False
            else:
              thisGroc.isMoving = True
              movingCount += 1
              if nearestx == thisGroc.x:
                if nearesty > thisGroc.y:
                  thisGroc.setDirection(K_NORTH)
                else:
                  thisGroc.setDirection(K_SOUTH)
              elif nearesty == thisGroc.y:
                if nearestx > thisGroc.x:
                  thisGroc.setDirection(K_EAST)
                else:
                  thisGroc.setDirection(K_WEST)
              elif abs(nearestx) > abs(nearesty):
                if nearestx > thisGroc.x:
                  thisGroc.setDirection(K_EAST)
                else:
                  thisGroc.setDirection(K_WEST)
              else:
                if nearesty > thisGroc.y:
                  thisGroc.setDirection(K_NORTH) 
                else: 
                  thisGroc.setDirection(K_SOUTH)

            newX, newY = thisGroc.move()            
            if newX == thisGroc.x and newY == thisGroc.y:
              logger.debug("Groc " + str(thisGroc.id) + 
                           " was unable to move") 
            else:
              #world.move
              wpipe.write(str(thisGroc.id) + "," + 
                          str(thisGroc.x) + "," + str(thisGroc.y) + "," + 
                          str(newX) + "," + str(newY) + K_NEWLINE)
              thisGroc.x = newX
              thisGroc.y = newY

              
              
    if movingCount == 0:
      running = False
      logger.debug("Nobody is moving")
    elif p_iterations == 0:
      running = True
    elif counter > p_iterations:
      running = False
      logger.debug("Iteration count exceeded")
    if counter % 100 == 0 or running == False:
      # write every 100 moves or when iteration limit reached
      grocFile = open(p_grocFile, "w")
      for thisGroc in grocList:
        grocText = thisGroc.dump()
        grocFile.write(grocText+K_NEWLINE)
        logger.debug ("Groc " + str(thisGroc.id) + " saved")
      grocFile.close()

    #
    # Saving The World
    #
    
  
  wpipe.close()
  if os.path.exists(K_PIPE_NAME):
    os.unlink(K_PIPE_NAME)



            
if __name__ == '__main__':
    main()
