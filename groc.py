#!/usr/bin/python
#
#   groc.py
#
#     python class for an experiment in object-oriented ai
#     
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
#   TDORSEY     2022-04-29  Pipe location to world.py (later w-debug.py)
#                           Brownian motion
#                           Ability to iterate forever
#   TDORSEY     2022-04-30  Grocs seek nearest groc
#                           Generate grocs up to limit when reading a file
#                           Exit when nobody is moving 
#   TDORSEY     2022-05-01  Refactor groc into groc.py class file
#   TDORSEY     2022-05-02  World owns constants now
#                           Add movement methods to Groc
#                           Add elapsedTicks and tick() to World

import datetime 
import logging
import math
import numpy
import os
import sys

print("Loading groc")

class World():
    'Base class for the world'
    NORTH = 1
    EAST = 2
    SOUTH = 3
    WEST = 4
    FIELDSEP = '|'
    NEWLINE = '\n'
    PIPENAME = "/tmp/grocpipe"
    GROCFILE = "grocfile.dat"
    WORLDFILE = ".world.dat"
    LOGFILE = "groc.log"
    LOGLEVEL = logging.ERROR
    elapsedTicks = 0
    
    def __init__(self, x, y):
        
        super(World, self).__init__()
         
        self.MAXX = x
        self.MAXY = y
        Log_Format = "%(levelname)s %(asctime)s - %(message)s"
        logging.basicConfig(filename = self.LOGFILE,
                            filemode = "w", 
                            format = Log_Format, 
                            level = self.LOGLEVEL)
        self.logger = logging.getLogger()
        if os.path.exists(self.WORLDFILE):
          worldFile = open(self.WORLDFILE, "r")
          line = worldFile.readline()
          World.elapsedTicks = int(line)
        else:
          World.elapsedTicks = 0

    def findDistance(self, firstx, firsty, secondx, secondy):
        xDiff = abs(firstx - secondx) 
        yDiff = abs(firsty - secondy)
        #return (math.sqrt((xDiff ** 2) + (yDiff ** 2)))
        return (((xDiff ** 2) + (yDiff ** 2)) ** .5)

     
    def randomLocation(self):
        newX = numpy.random.randint(1, self.MAXX)  
        newY = numpy.random.randint(1, self.MAXY)
        return (newX, newY)

    def saveWorld(self):
        worldFile = open(World.WORLDFILE, "w")
        worldFile.write(str(self.elapsedTicks) + self.NEWLINE)
        worldFile.close()

    def tick(self):
        self.elapsedTicks += 1

class Groc():
    'Base class for the groc'
    grocCount = 0    
    
    def __init__(self, world, name, mood, color, x, y, id=None, 
                 birthdatetime=None):
        
        super(Groc, self).__init__()

        Groc.grocCount += 1
        self.world = world
        self.name = name
        self.mood = mood
        self.color = color
        self.x = int(x)
        self.y = int(y)
        if id == None:
            self.id = Groc.grocCount
        else:
            self.id = Groc.grocCount
        if birthdatetime == None:
            self.birthdatetime = datetime.datetime.now()
        else:
            self.birthdatetime = birthdatetime
        self.world.logger.debug ("Groc " + str(self.id) + 
                      " X,Y:" + str(self.x) + "," + str(self.y))
       
    def findNearestGroc(self, listOfGrocs):
        nearestx = self.world.MAXX
        nearesty = self.world.MAXY 
        leastDist = nearestx + nearesty
        for anotherGroc in listOfGrocs:
          if anotherGroc.id == self.id:
            self.world.logger.debug("Groc " + str(self.id) + 
                          " skip myself")
          else: 
            zDist = self.world.findDistance(self.x, self.y, 
                               anotherGroc.x, anotherGroc.y)
            self.world.logger.debug("Groc " + str(anotherGroc.id) + 
                       " is " + str(zDist) + " away")
            if zDist < leastDist:
              leastDist = zDist
              nearestx = anotherGroc.x
              nearesty = anotherGroc.y
        return (nearestx, nearesty)


    def setMood(self, newMood):
        self.mood = newMood
  
    def didMove(self, x, y):
        if self.x == x and self.y == y:
          result = False
        else:
          result = True
        return (result)

    def moveToward(self, x, y, speed=1):
        newX = self.x
        newY = self.y
        for step in range(speed):
          self.world.logger.debug("Step " + str(step))
          if newX < x:
            newX = newX + 1
          elif newX > x:
            newX = newX - 1
          elif newY < y:
            newY = newY + 1
          elif newY > y:
            newY = newY - 1
        return (newX, newY)
 
# identify
    def identify(self):
        self.world.logger.debug ("My ID is " + str(self.id) + 
                      " and I was born " + 
                      self.birthdatetime.strftime("%Y-%m-%d %H:%M"))
        
# dump
    def dump(self):
        fs = self.world.FIELDSEP
        return ( self.name + fs + self.mood + fs + self.color + fs + 
               str(self.x) + fs + str(self.y) + fs + str(self.id) + fs + 
               self.birthdatetime.strftime("%Y-%m-%d %H:%M"))


            

