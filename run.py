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
#   TDORSEY     2022-05-06  Observe, decide, act

import datetime 
import logging
import math
import os
import sys
import groc

# default limits

K_GROC_LIMIT = 2
K_ITER_LIMIT = 1000
K_LOG_LEVEL = 20


# main

def main():   
  print ("Start render to continue")
  thisWorld = groc.World(1800,800)
  renderPipe = thisWorld.renderPipe
  #Command Line Arguments
  numArgs = len(sys.argv)
  if numArgs > 4:
    p_grocFile = sys.argv[4] 
  else:
    p_grocFile = thisWorld.GROCFILE
  if numArgs > 3:
    p_logLevel = int(sys.argv[3])
  else:
    p_logLevel = K_LOG_LEVEL
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
  print("p_logLevel: ", p_logLevel)
  print("p_grocFile: ", p_grocFile)
  logger = thisWorld.getLogger(p_logLevel)
  logger.info("Started run with p_numgrocs=" + str(p_numGrocs) + 
              ", p_iterations=" + str(p_iterations) + 
              ", p_grocfile=" + str(p_grocFile))
  # 
  #Reading the world
  #
  thisWorld.getGrocs(p_numGrocs, p_grocFile)
  running = True
  counter = 0 
  while running:
    counter += 1
    movingCount = 0 
    for thisGroc in thisWorld.grocList:   
       oldX = thisGroc.x
       oldY = thisGroc.y
       thisGroc.observe()
       thisGroc.decide()
       thisGroc.act()
       if thisGroc.didMove(oldX, oldY):
         movingCount += 1
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
      thisWorld.saveGrocs(p_grocFile)
      thisWorld.saveWorld()

    thisWorld.tick()

  #
  # Saving The World
  #
  thisWorld.close() 
  logger.info("World closed")
            
if __name__ == '__main__':
    main()
