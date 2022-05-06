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
#   TDORSEY     2022-05-06  observe,decide,act

import datetime 
import logging
import math
import numpy
import os
import sys

print("Loading groc")

class World():
    'Base class for the world'
    # DIRECTIONS
    NORTH = 1
    EAST = 2
    SOUTH = 3
    WEST = 4
    
    # FILE UTILS
    FIELDSEP = '|'
    NEWLINE = '\n'
    PIPENAME = "/tmp/grocpipe"
    GROCFILE = "grocfile.dat"
    WORLDFILE = ".world.dat"
    LOGFILE = "groc.log"

    currentTick = 0    

    # COLORS
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)
    RED = (128, 0, 0)
  
    def __init__(self, x, y):
        
        super(World, self).__init__()
         
        self.MAXX = x
        self.MAXY = y
        self.logger = None
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
        builtList = []
        if os.path.exists(grocFile):
          savedFile = open(grocFile, "r")
          grocsRead = 0 
          line = savedFile.readline()
          while line: 
            grocsRead += 1
            list = line.split(self.FIELDSEP)
            newGroc = Groc(self, list[0],list[1], list[2], 
                          list[3], list[4], list[5], 
                          list[6].rstrip(self.NEWLINE))
            newGroc.identify()
            self.render(newGroc.id, 0, 0, newGroc.x, newGroc.y, 
                        newGroc.gender)
            builtList.append(newGroc)
            line = savedFile.readline()
          savedFile.close()      
        else:
          grocsRead = 0
        if grocsRead < numGrocs:
          for count in range(0, (numGrocs - grocsRead)):
            newX, newY = self.randomLocation()
            newGroc = Groc(self, Groc.HAPPY, "green", newX, newY)
            newGroc.identify()
            self.render(newGroc.id, 0, 0, newGroc.x, newGroc.y, 
                        newGroc.gender)
            builtList.append(newGroc)
        #return grocList
        self.grocList = builtList

# world.getLogger
    def getLogger(self, debugLevel):    
      if self.logger is None:
        Log_Format = "%(levelname)s %(asctime)s - %(message)s"
        logging.basicConfig(filename = self.LOGFILE,
                            filemode = "w", 
                            format = Log_Format, 
                            level = debugLevel)
        self.logger = logging.getLogger()
      return self.logger 

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
    def saveGrocs(self, grocFile):
      saveFile = open(grocFile, "w")
      for thisGroc in self.grocList:
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
    # MOODS
    CROWDED = "Crowded"
    HAPPY = "Happy"
    LONELY = "Lonely"

    
    def __init__(self, world, mood, color, x, y, 
                 id=None, birthTick=None, 
                 gender=None):
        
        super(Groc, self).__init__()

        Groc.grocCount += 1
        self.world = world
        self.mood = mood
        self.color = color
        self.x = int(x)
        self.y = int(y)
        self.nearestGroc = None
        self.targetX = None
        self.targetY = None
        self.communityRadius = 100
        self.personalRadius = 20
        self.preferredCommunitySize = 4
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
        self.world.logger.debug ("(init)Groc " + str(self.id) + 
                      " X,Y:" + str(self.x) + "," + str(self.y))
       
# groc.act
    def act(self):
      if self.mood == self.HAPPY:
        self.targetX = None
        self.targetY = None
      elif self.mood == self.LONELY:
        self.targetX = self.nearestGroc.x
        self.targetY = self.nearestGroc.y
      elif self.mood == self.CROWDED:
        if self.targetX is None or self.targetY is None:
          self.targetX, self.targetY = self.world.randomLocation()
      else:
        self.world.logger.debug("act:" + str(self.id) + " Unknown mood " + 
                                self.mood)
      if self.targetX is None or self.targetY is None:
        self.world.logger.debug("act: " + str(self.id) + " is " + 
                                self.mood + " no movement")
      else:
        self.moveTowardTarget()

# groc.countNearbyGrocs
    def countNearbyGrocs(self, searchRadius):
      count = 0
      for anotherGroc in self.world.grocList:
        if not (anotherGroc.id == self.id):
          zdist = self.world.findDistance(self.x, self.y, 
                                          anotherGroc.x, anotherGroc.y)
          if zdist <= searchRadius:
            count += 1
      return count     
       
# groc.decide
    def decide(self):
      zdist = self.world.findDistance(self.x, self.y, self.nearestGroc.x, 
                                      self.nearestGroc.y)
      communityCount = self.countNearbyGrocs(self.communityRadius)
      personalCount = self.countNearbyGrocs(self.personalRadius)
      if zdist <= self.personalRadius:  
        newMood = self.HAPPY
      elif zdist > self.personalRadius:
        newMood = self.LONELY
      else:
        newMood = self.HAPPY
      if self.mood == newMood:
        self.world.logger.debug("decide: " + str(self.id) + 
                                " mood is stable at " + 
                                self.mood)
      else:
        self.world.logger.debug("decide: " + str(self.id) + 
                                " changed mood from " + 
                                self.mood + " to " + newMood )
        self.mood = newMood

# groc.didMove
    def didMove(self, x, y):
        if self.x == x and self.y == y:
          result = False
        else:
          result = True
        return (result)

# groc.dump
    def dump(self):
        fs = self.world.FIELDSEP
        return ( self.mood + fs + self.color + fs + 
               str(self.x) + fs + str(self.y) + fs + str(self.id) + fs + 
               str(self.birthTick) + fs + self.gender + self.world.NEWLINE)

# groc.findNearestGroc
    def findNearestGroc(self):
        nearestx = self.world.MAXX
        nearesty = self.world.MAXY 
        leastDist = nearestx + nearesty
        nearestGroc = None
        for anotherGroc in self.world.grocList:
          if not (anotherGroc.id == self.id):
            zDist = self.world.findDistance(self.x, self.y, 
                               anotherGroc.x, anotherGroc.y)
            if zDist < leastDist:
              leastDist = zDist
              nearestGroc = anotherGroc
        return nearestGroc
    
# groc.geneticAttributes
    def geneticAttributes(self):
        seed = numpy.random.randint(1, self.world.MAXX) 
        if seed % 2 == 0:
          gender = Groc.FEMALE
        else:
          gender = Groc.MALE
        # additional attributes added later
        return gender

# groc.hasTarget
    def hasTarget(self):
        if self.targetX is None or self.targetY is None:
          answer = False
        elif self.targetX == self.x and self.targetY == self.y:
          targetX = None
          targetY = None
          answer = False
        else:
          answer = True
        return answer
          

# groc.identify
    def identify(self):
        self.world.logger.debug ("Identify " + str(self.id) + 
                      " was born at " + str(self.birthTick))

# groc.moveTowardTarget
    def moveTowardTarget(self, speed=1):
        if self.targetX is None or self.targetY is None:
          self.world.logger.debug("moveTowardTarget: " + str(self.id) + 
                                  " has no target")
        else:
          newX = self.x
          newY = self.y
          for step in range(speed):
            if newX < self.targetX:
              newX = newX + 1
            elif newX > self.targetX:
              newX = newX - 1
            elif newY < self.targetY:
              newY = newY + 1
            elif newY > self.targetY:
              newY = newY - 1
          self.world.render(self.id, self.x, self.y, newX, newY, 
                            self.gender)
          self.x = newX
          self.y = newY

# groc.observe
    def observe(self):
        self.nearestGroc = self.findNearestGroc()
        #other observations eventually

# groc.setMood
    def setMood(self, newMood):
        self.mood = newMood

# groc.setTarget(self, newx, newy)
    def setTarget(self, newx, newy):
        self.targetX = newx
        self.targetY = newy 

