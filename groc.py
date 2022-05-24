#!/usr/bin/python3
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
#                           Move initialization code into main
#   TDORSEY     2022-05-03  Move load/save to World class
#                           Move pipe definition to World class 
#   TDORSEY     2022-05-04  New groc file format, remove birthdatetime
#                           Add birthTick. Render gender.
#   TDORSEY     2022-05-04  Blank Line fix
#   TDORSEY     2022-05-06  observe,decide,act
#                           Added log level arg
#   TDORSEY     2022-05-07  grocfile.dat contains Groc constructor calls
#   TDORSEY     2022-05-12  Enabling CROWDED; establishing moodSince
#                           Added patience factor, stillness limit
#   TDORSEY     2022-05-14  Improved target finding for choosing a less
#                           crowded space 
#   TDORSEY     2022-05-15  visible moods
#   TDORSEY     2022-05-17  Added world stats
#   TDORSEY     2022-05-20  Combine groc.py and run.py
#                           Eliminate numpy
#   TDORSEY     2022-05-21  Support external renderers via a standard
#                           class and set of methods
#   TDORSEY     2022-05-22  Pass the world to the renderer for reference
#   

import datetime 
import logging
import math
import os
import random
# choose which renderer here
import grr_pyg as render
#import grr_pipe as render
import sys

# default limits
K_STILL_LIMIT = 10
K_GROC_LIMIT = 2
K_ITER_LIMIT = 1000
K_LOG_LEVEL = 20
# 50 CRITICAL
# 40 ERROR
# 30 WARNING
# 20 INFO
# 10 DEBUG
# 0  NOTSET

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
    GROCFILE = "grocfile.dat"
    WORLDFILE = ".world.dat"
    LOGFILE = "groc.log"

    currentTick = 0    

    # COLORS
    BLACK = (0, 0, 0)
    BLUE = (0, 0, 255)
    RED = (128, 0, 0)
    WHITE = (255, 255, 255)
 
    def __init__(self, x, y):
        
        super(World, self).__init__()
         
        self.MAXX = x
        self.MAXY = y
        self.happy = 0
        self.lonely = 0
        self.crowded = 0
        self.logger = None
        self.render = render.Renderer(self)
        if os.path.exists(self.WORLDFILE):
          self.worldFile = open(self.WORLDFILE, "r")
          line = self.worldFile.readline()
          World.currentTick = int(line)
        else:
          World.currentTick = 0

# world.bindX
    def bindX(self, x):
        boundx = x
        if x < 1:
          boundx = 1 
        if x > self.MAXX:
          boundx = self.MAXX
        return boundx

# world.bindY
    def bindY(self, y):
        boundy = y 
        if y < 1:
          boundy = 1
        if y > self.MAXY:
          boundy = self.MAXY
        return boundy

 
# world.close
    def close(self):
        self.render.close()  

# world.elapsedTicks
    def elapsedTicks(self, sinceTick):
        return abs(self.currentTick - sinceTick)
        

# world.findDistance
    def findDistance(self, firstx, firsty, secondx, secondy):
        xDiff = abs(firstx - secondx) 
        yDiff = abs(firsty - secondy)
        return (((xDiff ** 2) + (yDiff ** 2)) ** .5)

# world.findNearbyGroc
    def findNearbyGroc(self, x, y):
        leastDist = self.findDistance(0, 0, self.MAXX, self.MAXY)
        nearestGroc = None
        for thisGroc in self.grocList:
          zDist = self.findDistance(x, y, thisGroc.x, thisGroc.y)
          if zDist < leastDist:
            leastDist = zDist
            nearestGroc = thisGroc
        return nearestGroc

# world.getGrocs
    def getGrocs(self, numGrocs, grocFile):
        builtList = []
        if os.path.exists(grocFile):
          savedFile = open(grocFile, "r")
          grocsRead = 0 
          line = savedFile.readline()
          while line: 
            grocsRead += 1
            newGroc = eval(line)
            newGroc.identify()
            self.render.drawStatic(newGroc, self.bindX(newGroc.x), 
                                   self.bindY(newGroc.y))
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
            self.render.drawStatic(newGroc, newX, newY)
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
        newX = random.randint(1, self.MAXX)  
        newY = random.randint(1, self.MAXY)
        self.logger.debug("randomx, randomy = " + 
                         str(newX) + "," + str(newY))
        return (newX, newY)

# world.saveGrocs
    def saveGrocs(self, grocFile):
      saveFile = open(grocFile, "w")
      for thisGroc in self.grocList:
        saveFile.write(str(thisGroc))
        self.logger.debug ("Groc " + str(thisGroc.id) + " saved")
      saveFile.close()

# world.saveWorld
    def saveWorld(self):
        self.worldFile = open(World.WORLDFILE, "w")
        self.worldFile.write(str(self.currentTick) + self.NEWLINE)
        self.worldFile.close()

# world.setStats
    def setStats(self, happy, lonely, crowded):
        self.happy = happy 
        self.lonely = lonely
        self.crowded = crowded

# world.tick
    def tick(self):
        self.currentTick += 1
        self.render.tick()

# world.percentage
    def percentage(self):
        return(random.randint(1,100))
        

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
        self.moodSince = self.world.currentTick
        self.color = color
        self.x = int(x)
        self.y = int(y)
        self.nearestGroc = None
        self.targetX = None
        self.targetY = None
        self.communityRadius = 22
        self.personalRadius = 20
        self.preferredCommunitySize = 4
        self.patience=5
        self.communityCount = 0
        self.personalCount = 0
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
       
# groc.__str__
    def __str__(self):
      return self.dump()

# groc.__repr__
    def __repr__(self):
      return self.dump()
     
# groc.act
    def act(self):
      'take action'
      if self.targetX is None or self.targetY is None:
        pass
      else:
        self.moveTowardTarget()


# groc.chooseLessCrowdedSpace
    def chooseLessCrowdedSpace(self, radius):
      quadrantNames = ['NW', 'NE', 'SW', 'SE']
      quadrantInfo = {"NW":(-1,-1), "NE":(1,-1), "SW":(-1,1), "SE":(1,1)}
      leastPopulation = 100000
      if self.gender == Groc.MALE:
        direction = -1
      else:
        direction = 1
      for quadrantName in quadrantNames[::direction]:   
        xfactor, yfactor = quadrantInfo[quadrantName]
        population = self.countNearbyGrocs(radius, 
          self.world.bindX(self.x + (xfactor * radius)), 
          self.world.bindY(self.y + (yfactor * radius)))
        if population < leastPopulation:
          leastPopulation = population
          targetQuadrant = quadrantName
      self.world.logger.debug ("Target quadrant is " + 
          targetQuadrant + " " + 
          " population " +  str(leastPopulation))
      xfactor, yfactor = quadrantInfo[targetQuadrant]
      newX = self.world.bindX(self.x + (xfactor * radius))
      newY = self.world.bindY(self.y + (yfactor * radius))
      self.world.logger.debug("newx, newy " + str(newX) + "," + str(newY))
      return newX, newY
 
# groc.countNearbyGrocs
    def countNearbyGrocs(self, searchRadius, x, y):
      'count within a given radius'
      count = 0
      for anotherGroc in self.world.grocList:
        if not (anotherGroc.id == self.id):
          zdist = self.world.findDistance(x, y, 
                                          anotherGroc.x, anotherGroc.y)
          if zdist <= searchRadius:
            count += 1
      return count     
       
# groc.decide
    def decide(self):
      'decide what to do'
      zdist = self.world.findDistance(self.x, self.y, self.nearestGroc.x, 
                                      self.nearestGroc.y)
      if zdist < self.personalRadius:  
        self.setMood(Groc.CROWDED)
      elif zdist > self.communityRadius:
      #elif zdist > self.personalRadius:
        self.setMood(Groc.LONELY)
      else:
        self.setMood(Groc.HAPPY)

      if self.targetX == self.x and self.targetY == self.y:
        #arrived
        self.targetX = None
        self.targetY = None
      elif self.mood == Groc.HAPPY:
        #stay put when you're happy
        self.targetX = None
        self.targetY = None
      elif self.mood == Groc.LONELY:
        #continually retarget nearest groc when lonely
        self.targetX = self.nearestGroc.x
        self.targetY = self.nearestGroc.y
      elif self.mood == Groc.CROWDED:
        #pick a target one time when crowded
        if self.targetX is None and self.targetY is None:
          pct = self.world.percentage()
          if pct <= 50:
            self.targetX, self.targetY = self.world.randomLocation()
          else:
            self.targetX, self.targetY = self.chooseLessCrowdedSpace(
                                               self.communityRadius)
        else:
          pass
     
       

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
        return ("Groc(self, '" + self.mood + "', '" + 
                self.color + "', " + str(self.x) + ", " + 
                str(self.y) + ", " + str(self.id) + ", " + 
                str(self.birthTick) + ", '" + 
                str(self.gender) + "')" + self.world.NEWLINE)

# groc.findNearestGroc
    def findNearestGroc(self):
        nearestx = self.world.MAXX
        nearesty = self.world.MAXY 
        leastDist = self.world.findDistance(0, 0, nearestx, nearesty)
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
        seed = random.randint(1, self.world.MAXX) 
        if seed % 2 == 0:
          gender = Groc.FEMALE
        else:
          gender = Groc.MALE
        # additional attributes added later
        return gender

# groc.isMoving
    def isMoving(self, theGroc):
        if theGroc.targetX is None or theGroc.targetY is None:
          answer = False
        elif theGroc.targetX == theGroc.x and theGroc.targetY == theGroc.y:
          answer = False
        else:
          answer = True
        return answer
          

# groc.identify
    def identify(self):
        self.world.logger.debug ("Identify " + str(self.id) + 
                      " was born at " + str(self.birthTick))
        identity = ("Id: " + str(self.id) + 
                   " Current X,Y: " + str(self.x) + "," + str(self.y) + 
                   " Target X,Y: " + str(self.targetX) + "," + 
                                     str(self.targetY) + 
                   " Mood: " + self.mood + 
                   " Gender: " + self.gender + 
                   " Birthtick: " + str(self.birthTick))
        return identity 
 

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
          self.world.render.drawMoving(self, self.x, self.y, newX, newY)
          self.x = newX
          self.y = newY

# groc.observe
    def observe(self):
        self.nearestGroc = self.findNearestGroc()
        self.communityCount = self.countNearbyGrocs(self.communityRadius, 
                                                   self.x, self.y)
        self.personalCount = self.countNearbyGrocs(self.personalRadius, 
                                                   self.x, self.y)
        #other observations eventually

# groc.setMood
    def setMood(self, newMood):
        if self.mood == newMood:
          pass
        else:
          self.mood = newMood
          self.moodSince = self.world.currentTick
          self.world.render.drawStatic(self, self.x, self.y)

# groc.setTarget(self, newx, newy)
    def setTarget(self, newx, newy):
        self.targetX = newx
        self.targetY = newy 


# main

def main():   
  thisWorld = World(1800,800)
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
  stillTimer = 0
  while running:
    counter += 1
    movingCount = 0 
    happyCount = 0
    lonelyCount = 0
    crowdedCount = 0
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
       if thisGroc.mood == Groc.HAPPY:
         happyCount += 1
       elif thisGroc.mood == Groc.LONELY:
         lonelyCount += 1
       elif thisGroc.mood == Groc.CROWDED:
         crowdedCount += 1

    thisWorld.setStats(happyCount, lonelyCount, crowdedCount)

    if movingCount > 0:
      stillTimer = 0
    else:
      stillTimer += 1

    if stillTimer > K_STILL_LIMIT:
      running = False
      logger.info("Nobody has moved in " + str(K_STILL_LIMIT) + " ticks")
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
  print("Nothing is moving")
  thisWorld.close() 
  logger.info("World closed")
            
if __name__ == '__main__':
    main()
