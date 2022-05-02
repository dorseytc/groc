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

       nearestX, nearestY = thisGroc.findNearestGroc(grocList)
       zdist = thisWorld.findDistance(thisGroc.x, thisGroc.y, 
                                      nearestX, nearestY)
       if zdist < 20: 
         thisGroc.setMood('Happy')
         newX, newY = (thisGroc.x, thisGroc.y)
       else:
         thisGroc.setMood('Lonely')
         newX, newY = thisGroc.moveToward(nearestX, nearestY)

       if thisGroc.didMove(newX, newY): 
         movingCount += 1
         #world.move
         wpipe.write(str(thisGroc.id) + "," + 
                     str(thisGroc.x) + "," + str(thisGroc.y) + "," + 
                     str(newX) + "," + str(newY) + 
                          thisWorld.NEWLINE)
         thisGroc.x = newX
         thisGroc.y = newY
       else: 
         logger.debug("Groc " + str(thisGroc.id) + 
                      " did not move")

              
              
    if movingCount == 0:
      running = False
      logger.debug("Nobody is moving")
    elif p_iterations == 0:
      running = True
    elif counter >= p_iterations:
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
      thisWorld.saveWorld()

    thisWorld.tick()

  #
  # Saving The World
  #
  wpipe.close()
  if os.path.exists(thisWorld.PIPENAME):
    os.unlink(thisWorld.PIPENAME)



            
if __name__ == '__main__':
    main()
