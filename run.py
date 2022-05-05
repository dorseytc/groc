#!/usr/bin/python3
#
#   run
#
#      wrapper for groc, an object-oriented experiment in ai
#
#   TDORSEY     2022-05-01  Created run.py by refactoring
#                           groc.py into "class-specific" file 
#                           for groc.py, remainder becomes run.py
#   TDORSEY     2022-05-02  Move constants to World class
#                           Move initialization code into main
#   TDORSEY     2022-05-03  Move load/save to World class
#                           Move pipe definition to World class 
#   TDORSEY     2022-05-04  Render gender
#   TDORSEY     2022-05-05  Blank line fix

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
  print ("Start render to continue")
  thisWorld = groc.World(1800,800)
  renderPipe = thisWorld.renderPipe
  logger = thisWorld.logger
  #Command Line Arguments
  numArgs = len(sys.argv)
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
  print("p_numgrocs: ", p_numGrocs) 
  print("p_iterations: ", p_iterations)
  print("p_grocfile: ", p_grocFile)
  logger.info("Started run with p_numgrocs=" + str(p_numGrocs) + 
              ", p_iterations=" + str(p_iterations) + 
              ", p_grocfile=" + str(p_grocFile))
  # 
  #Reading the world
  #
  grocList = thisWorld.getGrocs(p_numGrocs, p_grocFile)
  running = True
  counter = 0 
  while running:
    counter += 1
    movingCount = 0 
    for thisGroc in grocList:   
       nearestGroc = thisGroc.findNearestGroc(grocList)
       # I still think moods and decisions belong in Groc
       targetX, targetY, newMood = thisGroc.decideMovement(nearestGroc)
       if newMood in (thisGroc.LONELY, thisGroc.CROWDED): 
         newX, newY = thisGroc.moveToward(targetX, targetY) 
       else:
         newX, newY = (thisGroc.x, thisGroc.y) 
       thisGroc.setMood(newMood)

       if thisGroc.didMove(newX, newY):
         movingCount += 1
         thisWorld.render(thisGroc.id, thisGroc.x, thisGroc.y, 
                          newX, newY, thisGroc.gender)
         thisGroc.x = newX
         thisGroc.y = newY
       else: 
         logger.debug("Groc " + str(thisGroc.id) + 
                      " did not move")

    if movingCount == 0:
      running = False
      logger.info("Nobody is moving")
    elif p_iterations == 0:
      running = True
    elif counter >= p_iterations:
      running = False
      logger.info("Iteration count exceeded")
    if counter % 100 == 0 or running == False:
      # write every 100 moves or when iteration limit reached
      thisWorld.saveGrocs(grocList, p_grocFile)
      thisWorld.saveWorld()

    thisWorld.tick()

  #
  # Saving The World
  #
  thisWorld.close() 
  logger.info("World closed")
            
if __name__ == '__main__':
    main()
