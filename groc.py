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
#                           Remainder becomes world.py

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
#    def move(self, oldX, oldY, newX, newY):
#        wpipe.write(str(self.id) + "," + str(oldX) + "," + str(oldY) + "," +
#                    str(newX) + "," + str(newY) + K_NEWLINE)
        
# setMotion
    def setMotion(self, pisMoving):
        self.isMoving = pisMoving

# setDirection
    def setDirection(self, pdirection=0):
        self.direction = pdirection

# update        
    def move(self):
        logger.debug ("update Groc " + str(self.id) + " isMoving? " + 
                      str(self.isMoving) + " Direction? " + 
                      str(self.direction) + " " + str(self.x) + "," + 
                      str( self.y))
        newX = self.x
        newY = self.y
        if self.isMoving == True:
            if self.direction == K_NORTH:
                #self.y += 1
                newY = self.y + 1
            elif self.direction == K_SOUTH:
                newY = self.y - 1
            elif self.direction == K_EAST:
                newX = self.x + 1
            else:  
                #elif self.direction == K_WEST:
                newX = self.x - 1
                
            if newX <= 0:
                newX = 0;
                if self.direction == K_WEST:
                    self.direction = K_NORTH
            elif newX > K_MAXX:
                newX = K_MAXX
                if self.direction == K_EAST:
                    self.direction = K_SOUTH
            elif newY <= 0:
                newY = 1
                if self.direction == K_NORTH:
                    self.direction = K_EAST
            elif newY >= K_MAXY:
                newY = K_MAXY   
                if self.direction == K_SOUTH:
                    self.direction = K_WEST
        else:
            logger.debug ("UPDATE Groc " + str(self.id) + " has nothing to do")
        return (newX, newY) 
 
 
 
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


            

