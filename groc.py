#!/usr/bin/python
#
#   TDORSEY     2016-10-16  Created
#   TDORSEY     2016-10-16  Saving the world
#   TDORSEY     2016-10-16  Retrieving saved world
#   TDORSEY     2016-10-16  Improved class and function structure
#   TDORSEY     2016-10-17  Rendering via pygame
#   TDORSEY     2016-10-22  Some form of pygame hell
#   TDORSEY     2022-04-26  Removing pygame in favor of text based 
#   TDORSEY     2022-04-27  Adding logging
#                           Configurable loop lengths 
#   TDORSEY     2022-04-27  Log groc moves separately 
#   TDORSEY     2022-04-28  Groc position to stdout for now
#   TDORSEY     2022-04-29  Pipe location to world.py
#                           Brownian motion
#                           Ability to iterate forever
#   TDORSEY     2022-04-30  Grocs seek nearest groc
#                           Generate grocs up to limit when reading a file
#                           Exit when nobody is moving 

import datetime 
import logging
import math
import numpy 
import os
import sys

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
print ("start world.py to continue")
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

class Groc():
    'Base class for the groc'
    grocCount = 0    
    
    def __init__(self, name, mood, color, x=None, y=None, id=None, 
                 birthdatetime=None, isMoving=False, direction=0):
        
        super(Groc, self).__init__()

        Groc.grocCount += 1
        self.name = name
        self.mood = mood
        self.color = color
        if x == None:
            self.x = numpy.random.randint(1, K_MAXX)
        else:
            self.x = int(x)
        if y == None:
            self.y = numpy.random.randint(1,K_MAXY)
        else:
            self.y = int(y)
        if id == None:
            self.id = Groc.grocCount
        else:
            self.id = Groc.grocCount
        if birthdatetime == None:
            self.birthdatetime = datetime.datetime.now()
        else:
            self.birthdatetime = birthdatetime
        self.isMoving = isMoving
        logger.debug ("Groc " + str(self.id) + 
                      " X,Y:" + str(self.x) + "," + str(self.y))
        self.direction = direction
       
# move 
    def move(self, oldX, oldY, newX, newY):
        wpipe.write(str(self.id) + "," + str(oldX) + "," + str(oldY) + "," +
                    str(newX) + "," + str(newY) + K_NEWLINE)
        
# setMotion
    def setMotion(self, pisMoving):
        self.isMoving = pisMoving

# setDirection
    def setDirection(self, pdirection=0):
        self.direction = pdirection

# update        
    def update(self):
        logger.debug ("update Groc " + str(self.id) + " isMoving? " + 
                      str(self.isMoving) + " Direction? " + 
                      str(self.direction) + " " + str(self.x) + "," + 
                      str( self.y))
        oldX = self.x
        oldY = self.y
        if self.isMoving == True:
            if self.direction == K_NORTH:
                self.y += 1
            elif self.direction == K_SOUTH:
                self.y += -1
            elif self.direction == K_EAST:
                self.x += 1
            else:  
                #elif self.direction == K_WEST:
                self.x += -1
                
            if self.x <= 0:
                self.x = 1
                if self.direction == K_WEST:
                    self.direction = K_NORTH
            elif self.x > K_MAXX:
                self.x = K_MAXX
                if self.direction == K_EAST:
                    self.direction = K_SOUTH
            elif self.y <= 0:
                self.y = 1
                if self.direction == K_NORTH:
                    self.direction = K_EAST
            elif self.y >= K_MAXY:
                self.y = K_MAXY   
                if self.direction == K_SOUTH:
                    self.direction = K_WEST
            self.move(oldX, oldY, self.x, self.y)
        else:
            logger.debug ("UPDATE Groc " + str(self.id) + " has nothing to do")
 
 
 
 
# introduce 
    def introduce(self):
        logger.debug ("My name is " + self.name + ".  I am " + self.color + 
                      " and I am feeling " + self.mood)
        
# identify
    def identify(self):
        logger.debug ("My ID is " + str(self.id) + " and I was born " + 
                      self.birthdatetime.strftime("%Y-%m-%d %H:%M"))
        
# locate
    def locate(self):
        self.move(0,0,self.x,self.y)
        logger.debug ("locate Groc " + self.name + " at " + str(self.x) + 
                      ", " + str(self.y) + " Moving: " + 
                      str(self.isMoving) +  " Direction: " + 
                      str(self.direction))
        
# census
    def census(self):
        logger.debug ("Total Groc Population is " + str(Groc.grocCount))

# getCount
    def getCount(self):
        return self.grocCount
    
# dump
    def dump(self):
        fs = K_FIELDSEP
        return ( self.name + fs + self.mood + fs + self.color + fs + 
               str(self.x) + fs + str(self.y) + fs + str(self.id) + fs + 
               self.birthdatetime.strftime("%Y-%m-%d %H:%M"))






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
      newGroc = Groc(list[0],list[1], list[2], list[3], list[4], list[5], 
                   birthdatetime)
      newGroc.identify()
      newGroc.locate()
      grocList.append(newGroc)
      line = savedFile.readline()
    savedFile.close()      
  else:
    grocsRead = 0
  if grocsRead < p_numGrocs:
    for count in range(0, (p_numGrocs - grocsRead)):
      name = 'G'+str(count)
      newGroc = Groc(name, 'happy', 'green')
      newGroc.identify()
      newGroc.introduce()
      newGroc.locate()
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

            thisGroc.update()            
              
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
