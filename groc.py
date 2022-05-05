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
#                           Add currentTick and tick() to World
#   TDORSEY     2022-05-03  Move load/save to World class
#   TDORSEY     2022-05-04  New groc file format, remove birthdatetime
#                           Add birthTick and gender.
#   TDORSEY     2022-05-04  Blank Line fix

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
    LOGLEVEL = logging.INFO
    #LOGLEVEL = logging.ERROR
    #LOGLEVEL = logging.DEBUG
    currentTick = 0    
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)
    RED = (128, 0, 0)

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
          self.worldFile = open(self.WORLDFILE, "r")
          line = self.worldFile.readline()
          World.currentTick = int(line)
        else:
          World.currentTick = 0
        if os.path.exists(self.PIPENAME):
          os.unlink(self.PIPENAME)
        if not os.path.exists(self.PIPENAME):
          os.mkfifo(self.PIPENAME, 0o600)
          self.renderPipe = open(self.PIPENAME, 'w', 
                                 newline=self.NEWLINE)
# world.close
    def close(self):
        self.renderPipe.close()
        if os.path.exists(self.PIPENAME):
          os.unlink(self.PIPENAME) 

# world.findDistance
    def findDistance(self, firstx, firsty, secondx, secondy):
        xDiff = abs(firstx - secondx) 
        yDiff = abs(firsty - secondy)
        #return (math.sqrt((xDiff ** 2) + (yDiff ** 2)))
        return (((xDiff ** 2) + (yDiff ** 2)) ** .5)

# world.getGrocs
    def getGrocs(self, numGrocs, grocFile):
        grocList = []
        if os.path.exists(grocFile):
          savedFile = open(grocFile, "r")
          grocsRead = 0 
          line = savedFile.readline()
          while line: 
            grocsRead += 1
            list = line.split(self.FIELDSEP)
            newGroc = Groc(self, list[0],list[1], list[2], 
                          list[3], list[4], list[5], 
                          list[6], list[7].rstrip(self.NEWLINE))
            newGroc.identify()
            self.render(newGroc.id, 0, 0, newGroc.x, newGroc.y, 
                        newGroc.gender)
            grocList.append(newGroc)
            line = savedFile.readline()
          savedFile.close()      
        else:
          grocsRead = 0
        if grocsRead < numGrocs:
          for count in range(0, (numGrocs - grocsRead)):
            name = 'G' + str(count)
            newX, newY = self.randomLocation()
            newGroc = Groc(self, name, 'happy', 'green', newX, newY)
            newGroc.identify()
            self.render(newGroc.id, 0, 0, newGroc.x, newGroc.y, 
                        newGroc.gender)
            grocList.append(newGroc)
        return grocList

# world.randomLocation
    def randomLocation(self):
        newX = numpy.random.randint(1, self.MAXX)  
        newY = numpy.random.randint(1, self.MAXY)
        return (newX, newY)

# world.render
    def render(self, grocId, oldx, oldy, newx, newy, gender):
        fs = World.FIELDSEP
        nl = World.NEWLINE
        self.renderPipe.write(str(grocId) + fs + str(oldx) + fs + 
                              str(oldy) + fs + str(newx) + fs + 
                              str(newy) + fs + gender + nl)

# world.saveGrocs
    def saveGrocs(self, grocList, grocFile):
      saveFile = open(grocFile, "w")
      for thisGroc in grocList:
        grocText = thisGroc.dump()
        saveFile.write(grocText)
        self.logger.debug ("Groc " + str(thisGroc.id) + " saved")
      saveFile.close()

# world.saveWorld
    def saveWorld(self):
        self.worldFile = open(World.WORLDFILE, "w")
        self.worldFile.write(str(self.currentTick) + self.NEWLINE)
        self.worldFile.close()

# world.tick
    def tick(self):
        self.currentTick += 1

class Groc():
    'Base class for the groc'
    grocCount = 0    
    MALE = "M"
    FEMALE = "F"
    
    def __init__(self, world, name, mood, color, x, y, 
                 id=None, birthTick=None, 
                 gender=None):
        
        super(Groc, self).__init__()

        Groc.grocCount += 1
        self.world = world
        self.name = name
        self.mood = mood
        self.color = color
        self.x = int(x)
        self.y = int(y)
        if id is None:
          self.id = Groc.grocCount
        else:
          self.id = Groc.grocCount
        if birthTick is None:
          self.birthTick = self.world.currentTick
        else:
          self.birthTick = birthTick
        if gender is None:
          self.gender = self.geneticAttributes() 
        else:
          self.gender = gender
        self.world.logger.debug ("Groc " + str(self.id) + 
                      " X,Y:" + str(self.x) + "," + str(self.y))
       
# groc.findNearestGroc
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
    
# groc.geneticAttributes
    def geneticAttributes(self):
        seed = numpy.random.randint(1, self.world.MAXX) 
        if seed % 2 == 0:
          gender = Groc.FEMALE
        else:
          gender = Groc.MALE
        # additional attributes added later
        return gender


      

# groc.setMood
    def setMood(self, newMood):
        self.mood = newMood
  
# groc.didMove
    def didMove(self, x, y):
        if self.x == x and self.y == y:
          result = False
        else:
          result = True
        return (result)

# groc.moveToward
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
 
# groc.identify
    def identify(self):
        self.world.logger.debug ("My ID is " + str(self.id) + 
                      " and I was born " + str(self.birthTick))
        
# groc.dump
    def dump(self):
        fs = self.world.FIELDSEP
        return ( self.name + fs + self.mood + fs + self.color + fs + 
               str(self.x) + fs + str(self.y) + fs + str(self.id) + fs + 
               str(self.birthTick) + fs + self.gender + self.world.NEWLINE)


            

