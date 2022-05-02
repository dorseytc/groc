#!/usr/bin/python
#
#   run
#
#      world class for groc, an object-oriented experiment in ai
#
#   TDORSEY     2022-05-01  Created run.py by refactoring
#                           groc.py into "class-specific" files 
#                           for world.py and groc.py
#                           Remainder becomes run.py
#   TDORSEY     2022-05-02  Move constants to World class
#                           Move initial code into main
#   

import datetime 
import logging
import math
import os
import sys
import groc

# default limits

K_GROC_LIMIT = 2
K_ITER_LIMIT = 1000


# main

def main():   
  thisWorld = groc.World(1800,800)
  print ("start render to continue")
  if os.path.exists(thisWorld.PIPENAME):
    os.unlink(thisWorld.PIPENAME)
  if not os.path.exists(thisWorld.PIPENAME):
    os.mkfifo(thisWorld.PIPENAME, 0o600)
    wpipe = open(thisWorld.PIPENAME, 'w', newline=thisWorld.NEWLINE)
  #Command Line Arguments
  numArgs = len(sys.argv)
  print(sys.argv)
  if numArgs > 3:
    p_grocFile = sys.argv[3] 
  else:
    p_grocFile = thisWorld.GROCFILE
  
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

  logger = thisWorld.logger
  # 
  #Reading the world
  #
  grocList = [] 
  if os.path.exists(p_grocFile):
    savedFile = open(p_grocFile, "r")
    grocsRead = 0 
    line = savedFile.readline()
    while line: 
      grocsRead += 1
      list = line.split(thisWorld.FIELDSEP)
      birthdatetime = datetime.datetime.strptime(
                      list[6].rstrip(thisWorld.NEWLINE), "%Y-%m-%d %H:%M")        
      newGroc = groc.Groc(thisWorld, list[0],list[1], list[2], 
                          list[3], list[4], list[5], 
                          birthdatetime)
      newGroc.identify()
      newGroc.locate()
      wpipe.write(str(newGroc.id) + "," + 
                          str(0) + "," + str(0) + "," + 
                          str(newGroc.x) + "," + str(newGroc.y) + 
                          thisWorld.NEWLINE)
      grocList.append(newGroc)
      line = savedFile.readline()
    savedFile.close()      
  else:
    grocsRead = 0
  if grocsRead < p_numGrocs:
    for count in range(0, (p_numGrocs - grocsRead)):
      name = 'G' + str(count)
      newX, newY = thisWorld.randomLocation()
      newGroc = groc.Groc(thisWorld, name, 'happy', 'green', newX, newY)
      newGroc.identify()
      newGroc.introduce()
      newGroc.locate()
      wpipe.write(str(newGroc.id) + "," + 
                  str(0) + "," + str(0) + "," + 
                  str(newGroc.x) + "," + str(newGroc.y) + thisWorld.NEWLINE)
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
        
            least_zdist = thisWorld.MAXX + thisWorld.MAXY
            nearestx = thisWorld.MAXX
            nearesty = thisWorld.MAXY 
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
                  thisGroc.setDirection(thisWorld.NORTH)
                else:
                  thisGroc.setDirection(thisWorld.SOUTH)
              elif nearesty == thisGroc.y:
                if nearestx > thisGroc.x:
                  thisGroc.setDirection(thisWorld.EAST)
                else:
                  thisGroc.setDirection(thisWorld.WEST)
              elif abs(nearestx) > abs(nearesty):
                if nearestx > thisGroc.x:
                  thisGroc.setDirection(thisWorld.EAST)
                else:
                  thisGroc.setDirection(thisWorld.WEST)
              else:
                if nearesty > thisGroc.y:
                  thisGroc.setDirection(thisWorld.NORTH) 
                else: 
                  thisGroc.setDirection(thisWorld.SOUTH)

            newX, newY = thisGroc.move()            
            if newX == thisGroc.x and newY == thisGroc.y:
              logger.debug("Groc " + str(thisGroc.id) + 
                           " was unable to move") 
            else:
              #world.move
              wpipe.write(str(thisGroc.id) + "," + 
                          str(thisGroc.x) + "," + str(thisGroc.y) + "," + 
                          str(newX) + "," + str(newY) + 
                          thisWorld.NEWLINE)
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
        grocFile.write(grocText+thisWorld.NEWLINE)
        logger.debug ("Groc " + str(thisGroc.id) + " saved")
      grocFile.close()

    #
    # Saving The World
    #
    
  
  wpipe.close()
  if os.path.exists(thisWorld.PIPENAME):
    os.unlink(thisWorld.PIPENAME)



            
if __name__ == '__main__':
    main()
