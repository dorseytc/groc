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
    LOGFILE = "groc.log"
    LOGLEVEL = logging.DEBUG
    
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


     
    def randomLocation(self):
        newX = numpy.random.randint(1, self.MAXX)  
        newY = numpy.random.randint(1, self.MAXY)
        return (newX, newY)


class Groc():
    'Base class for the groc'
    grocCount = 0    
    
    def __init__(self, world, name, mood, color, x, y, id=None, 
                 birthdatetime=None, isMoving=False, direction=0):
        
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
        self.isMoving = isMoving
        self.world.logger.debug ("Groc " + str(self.id) + 
                      " X,Y:" + str(self.x) + "," + str(self.y))
        self.direction = direction
       
# setMotion
    def setMotion(self, pisMoving):
        self.isMoving = pisMoving

# setDirection
    def setDirection(self, pdirection=0):
        self.direction = pdirection

# update        
    def move(self):
        self.world.logger.debug ("update Groc " + str(self.id) + " isMoving? " + 
                      str(self.isMoving) + " Direction? " + 
                      str(self.direction) + " " + str(self.x) + "," + 
                      str( self.y))
        newX = self.x
        newY = self.y
        if self.isMoving == True:
            if self.direction == self.world.NORTH:
                newY = self.y + 1
            elif self.direction == self.world.SOUTH:
                newY = self.y - 1
            elif self.direction == self.world.EAST:
                newX = self.x + 1
            else:  
                newX = self.x - 1
                
            if newX <= 0:
                newX = 0;
                if self.direction == self.world.WEST:
                    self.direction = self.world.NORTH
            elif newX > self.world.MAXX:
                newX = self.world.MAXX
                if self.direction == self.world.EAST:
                    self.direction = self.world.SOUTH
            elif newY <= 0:
                newY = 1
                if self.direction == self.world.NORTH:
                    self.direction = self.world.EAST
            elif newY >= self.world.MAXY:
                newY = self.world.MAXY   
                if self.direction == self.world.SOUTH:
                    self.direction = self.world.WEST
        else:
            self.world.logger.debug ("UPDATE Groc " + str(self.id) + 
                          " has nothing to do")
        return (newX, newY) 
 
 
 
# introduce 
    def introduce(self):
        self.world.logger.debug ("My name is " + self.name + ".  I am " + self.color + 
                      " and I am feeling " + self.mood)
        
# identify
    def identify(self):
        self.world.logger.debug ("My ID is " + str(self.id) + " and I was born " + 
                      self.birthdatetime.strftime("%Y-%m-%d %H:%M"))
        
# locate
    def locate(self):
        self.world.logger.debug ("locate Groc " + self.name + " at " + str(self.x) + 
                      ", " + str(self.y) + " Moving: " + 
                      str(self.isMoving) +  " Direction: " + 
                      str(self.direction))
        
# census
    def census(self):
        self.world.logger.debug ("Total Groc Population is " + str(Groc.grocCount))

# getCount
    def getCount(self):
        return self.grocCount
    
# dump
    def dump(self):
        fs = self.world.FIELDSEP
        return ( self.name + fs + self.mood + fs + self.color + fs + 
               str(self.x) + fs + str(self.y) + fs + str(self.id) + fs + 
               self.birthdatetime.strftime("%Y-%m-%d %H:%M"))


            

