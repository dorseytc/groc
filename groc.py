#!/usr/bin/python3
#
#   groc.py
#
#     python class for an experiment in object-oriented ai
#     
#
#   TDORSEY  2016-10-16  Created
#   TDORSEY  2016-10-16  Saving the world
#   TDORSEY  2016-10-16  Retrieving saved world
#   TDORSEY  2016-10-16  Improved class and function structure
#   TDORSEY  2016-10-17  Rendering via pygame
#   TDORSEY  2016-10-22  Some form of pygame hell
#   TDORSEY  2022-04-26  Removing pygame in favor of text based 
#   TDORSEY  2022-04-27  Adding logging
#                        Configurable loop lengths 
#   TDORSEY  2022-04-27  Log groc moves separately 
#   TDORSEY  2022-04-28  Groc position to stdout for now
#   TDORSEY  2022-04-29  Pipe location to world.py (later w-debug.py)
#                        Brownian motion
#                        Ability to iterate forever
#   TDORSEY  2022-04-30  Grocs seek nearest groc
#                        Generate grocs up to limit when reading a file
#                        Exit when nobody is moving 
#   TDORSEY  2022-05-01  Refactor groc into groc.py class file
#   TDORSEY  2022-05-02  World owns constants now
#                        Add movement methods to Groc
#                        Add currentTick and tick to World
#                        Move initialization code into main
#   TDORSEY  2022-05-03  Move load/save to World class
#                        Move pipe definition to World class 
#   TDORSEY  2022-05-04  New groc file format, remove birthdatetime
#                        Add birthTick. Render gender.
#   TDORSEY  2022-05-04  Blank Line fix
#   TDORSEY  2022-05-06  observe,decide,act
#                        Added log level arg
#   TDORSEY  2022-05-07  grocfile.dat contains Groc constructor calls
#   TDORSEY  2022-05-12  Enabling CROWDED; establishing moodSince
#                        Added patience factor, stillness limit
#   TDORSEY  2022-05-14  Improved target finding for choosing a less
#                        crowded space 
#   TDORSEY  2022-05-15  visible moods
#   TDORSEY  2022-05-17  Added world stats
#   TDORSEY  2022-05-20  Combine groc.py and run.py
#                        Eliminate numpy
#   TDORSEY  2022-05-21  Support external renderers via a standard
#                        class and set of methods
#   TDORSEY  2022-05-22  Pass the world to the renderer for reference
#   TDORSEY  2022-05-24  Add HUNGRY and DEAD moods
#   TDORSEY  2022-05-25  Fix HUNGRY actions
#   TDORSEY  2022-05-26  Food has calories; Groc have foodpoints
#                        main loop simplified
#   TDORSEY  2022-05-27  handleFood and handleGrocs to simplify
#                        tick
#   TDORSEY  2022-06-01  variable bite and metabolism
#   TDORSEY  2022-06-03  Day and night


import datetime 
import logging
import math
import os
import random
import sys
import time
#
# choose a renderer here
#
import grr_pygame as render
#import grr_pipe as render
#
#
#
K_LOG_LEVEL = 50
K_MUTE = True
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
    WORLDFILE = "world.dat"
    LOGFILE = "groc.log"

    currentTick = 0    
    currentTime = time.time()
    defaultTick = .1
    #defaultTick = 0

    # COLORS
    BLACK = (0, 0, 0)
    BLUE = (0, 0, 255)
    RED = (128, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (159, 159, 159)

    def __init__(self, x, y):
        
        #super(World, self).__init__()
         
        self.MAXX = x
        self.MAXY = y
        #population counts
        self.happy = 0
        self.lonely = 0
        self.crowded = 0
        self.hungry = 0
        self.dead = 0
        self.population = 0
        self.foodList = []
        #technical pointers
        self.logger = None
        self.render = render.Renderer(self)
        self.mute = K_MUTE
        if os.path.exists(self.WORLDFILE):
          self.worldFile = open(self.WORLDFILE, "r")
          line = self.worldFile.readline()
          World.currentTick = int(line)
        else:
          World.currentTick = 0
        self.lightLevel = self.getLightLevel()
        World.startTick = World.currentTick

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

 
        
# world.createFood
    def createFood(self, calories=None, x=None, y=None):
        newFood = Food(self, calories, x, y)
        self.foodList.append(newFood)
        self.render.soundFood()

# world.d6
    def d6(self, n):
        result = 0
        for i in range(n):
          result = result + random.randint(1,6)
        return result

# world.elapsedTicks
    def elapsedTicks(self, sinceTick):
        'measure elapsed ticks subtracting sinceTicks from current value'
        return abs(self.currentTick - sinceTick)
        
# world.end
    def end(self):
        self.saveGrocs()
        self.saveWorld()
        self.endTimeSeconds = time.time()
        self.endTick = self.currentTick
        print("Elapsed seconds: " + 
              str(int(self.endTimeSeconds - self.startTimeSeconds)))
        print("Elapsed ticks: " + 
              str(self.endTick - self.startTick))
        self.render.close()  

# world.findDistance
    def findDistance(self, x1, y1, x2, y2):
        'measure the distance between a two pairs of coordinates'
        if None in (x1, x2, y1, y2):
          result = 0
        else:
          xDiff = abs(x1 - x2) 
          yDiff = abs(y1 - y2)
          result = (((xDiff ** 2) + (yDiff ** 2)) ** .5)
        return result

# world.findFoodNearXY
    def findFoodNearXY(self, x, y):
        'supply coordinates, find nearest Food'
        return self.findItemNearXY(self.foodList, x, y) 

# world.findItemNearXY
    def findItemNearXY(self, itemList, x, y):
        leastDist = self.findDistance(0, 0, self.MAXX, self.MAXY)
        nearestItem = None
        for thisItem in itemList:
          zDist = self.findDistance(x, y, thisItem.x, thisItem.y)
          if zDist < leastDist:
            leastDist = zDist
            nearestItem = thisItem
        return nearestItem

# world.findGrocNearXY
    def findGrocNearXY(self, x, y):
        'supply coordinates, find nearest Groc'
        return self.findItemNearXY(self.grocList, x, y)

# world.getGrocs
    def getGrocs(self, numGrocs):
        builtList = []
        if os.path.exists(World.GROCFILE):
          savedFile = open(World.GROCFILE, "r")
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
        self.grocList = builtList

# world.getLightLevel
    def getLightLevel(self):
        relevantTick = self.currentTick % 10000
        if 0 <= relevantTick < 1000:
          result = relevantTick/1000
          print(relevantTick, result)
        elif 1000 <= relevantTick < 5000:
          result = 1
        elif 5000 <= relevantTick < 6000:
          result = (6000-relevantTick)/1000
          print(relevantTick, result)
        elif 6000 <= relevantTick < 10000:
          result = 0 
        return result

# world.getLogger
    def getLogger(self, debugLevel):    
      if self.logger is None:
        Log_Format = "%(levelname)s %(asctime)s - %(message)s"
        logging.basicConfig(filename = self.LOGFILE,
                            filemode = "w", 
                            format = Log_Format, 
                            level = debugLevel)
        self.logger = logging.getLogger()

# world.getWorldColor
    def getWorldColor(self):
      def interpolateScalar(v1, v2, scale):
        return (scale*v2) + (1-scale)*v1
      def interpolateColor(color1, color2, scale):
        result = [None,None,None]
        for i in range(3):
          result[i] = interpolateScalar(color1[i], color2[i], scale)
        return tuple(result)
      return interpolateColor(self.BLACK, self.WHITE, self.lightLevel) 
 
# world.handleFood
    def handleFood(self):
        'handle Food items' 
        i = 0
        while i < len(self.foodList):
          if self.foodList[i].calories <= 0:
            deadFood = self.foodList.pop(i)
            self.render.drawFood(deadFood) 
          else:
            self.render.drawFood(self.foodList[i])
            i += 1
        if self.currentTick % 100 == 0:
          if len(self.foodList) < .05 * self.population:
            self.createFood()
        if len(self.foodList) == 0:
          for i in range(int(.05 * self.population)):
            self.createFood()

# world.handleGrocs
    def handleGrocs(self):
        movingCount = 0
        happyCount = 0
        lonelyCount = 0
        crowdedCount = 0
        hungryCount = 0
        deadCount = 0
        i = 0
        while i < len(self.grocList):
          if self.grocList[i].fp <= -5:
            deadGroc = self.grocList.pop(i)
            self.createFood(500, deadGroc.x, deadGroc.y)
          else:
            i += 1
        for thisGroc in self.grocList: 
          oldX = thisGroc.x
          oldY = thisGroc.y
          thisGroc.observe() 
          thisGroc.decide()
          thisGroc.act()
          if thisGroc.didMove(oldX, oldY):
            movingCount += 1
          if thisGroc.mood == Groc.HAPPY:
            happyCount += 1
          elif thisGroc.mood == Groc.LONELY:
            lonelyCount += 1
          elif thisGroc.mood == Groc.CROWDED:
            crowdedCount += 1
          elif thisGroc.mood == Groc.HUNGRY:
            hungryCount += 1
          elif thisGroc.mood == Groc.DEAD:
            deadCount += 1 
        self.setStats(happyCount, lonelyCount, crowdedCount, 
                      hungryCount, deadCount)

# world.interimSave
    def interimSave(self):
        if self.currentTick % 1000 == 0:
          self.saveGrocs()
          self.saveWorld()

# world.keepRunning
    def keepRunning(self): 
        result = True
        tickCount = self.currentTick - self.startTick
        if self.loopMode == "LIFE" and self.population <= 0:
          print("No life remaining")
          result = False
        elif self.loopMode == "MOTION" and self.motionCount <= 0:
          print("No motion remaining")
          result = False
        elif self.iterationLimit > 0 and tickCount > self.iterationLimit:
          print("Iteration limit " + str(self.iterationLimit) + 
                " exceeded")
          result = False
        return result

# world.randomLocation
    def randomLocation(self):
        newX = random.randint(1, self.MAXX)  
        newY = random.randint(1, self.MAXY)
        self.logger.debug("randomx, randomy = " + 
                         str(newX) + "," + str(newY))
        return (newX, newY)

# world.saveGrocs
    def saveGrocs(self):
      saveFile = open(World.GROCFILE, "w")
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
    def setStats(self, happy, lonely, crowded, hungry, dead):
        self.happy = happy 
        self.lonely = lonely
        self.crowded = crowded
        self.hungry = hungry
        self.dead = dead
        self.population = happy + lonely + crowded + hungry

# world.start
    def start(self, argv):
      numArgs = len(argv)
      if numArgs > 4:
        p_logLevel = int(argv[4])
      else:
        p_logLevel = 50
      assert 10 <= p_logLevel <= 50, "Invalid Log Level"
      if numArgs > 3:
        p_loopMode = argv[3]
      else:
        p_loopMode = "LIFE"
      assert p_loopMode in ("LIFE", "MOTION"), "Mode must be 'LIFE' or 'MOTION'"
      if numArgs > 2:
        p_iterationLimit = int(argv[2])
      else:
        p_iterationLimit = 0
      assert type(p_iterationLimit) is int, "Iterations must be an integer"
      if numArgs > 1:
        p_numGrocs = int(argv[1])
      else:
        p_numGrocs = 2
      assert type(p_numGrocs) is int, "Number of Grocs must be an integer"
      self.iterationLimit = p_iterationLimit
      self.numGrocs = p_numGrocs
      self.loopMode = p_loopMode
      self.startTimeSeconds = time.time()
      self.startTick = self.currentTick
      self.getLogger(p_logLevel)
      self.getGrocs(self.numGrocs)

# world.tick
    def tick(self, waitSeconds=0):
        self.currentTick += 1
        self.lightLevel = self.getLightLevel()
        self.handleGrocs()
        self.handleFood()
        self.interimSave()
        self.render.tick()
        if waitSeconds > 0:
          print("Slow tick ", waitSeconds, " seconds")
        nowTime = time.time()
        if nowTime < self.currentTime + self.defaultTick + waitSeconds:
          time.sleep(self.currentTime + self.defaultTick + waitSeconds - nowTime)
        self.currentTime = time.time()
        

        
        
# world.percentage
    def percentage(self):
        return(random.randint(1,100))
        

class Food():
    'New class for food'
    def __init__(self, world, calories=None, x=None, y=None): 
        self.world = world
        self.value = 1
        if None in (x, y):
          x, y = world.randomLocation()
        if None == calories:
          #self.calories = self.world.d6(10) * 10
          self.calories = 500 + self.world.hungry
        else:
          self.calories = calories
        self.x = x
        self.y = y
        self.color = (255, 0, 0)
        print(self.identify(), time.ctime())
         
         

#food.bite
    def bite(self, biteSize=1):
        'food returns calories to the consumer'
        biteCalories = biteSize * self.value
        if self.calories < biteCalories:
          biteCalories = max(self.calories, 0)
        self.calories = self.calories - biteCalories
        self.world.render.soundEat()
        return biteCalories
 
    def identify(self):
        identity = ("Calories: " + str(self.calories) + 
                   " X,Y: " + str(self.x) + "," + str(self.y) + 
                   " Value: " + str(self.value))
        return identity 
 
        
 
        

class Groc():
    'Base class for the groc'
    MALE = "M"
    FEMALE = "F"
    # MOODS
    CROWDED = "Crowded"
    HAPPY = "Happy"
    LONELY = "Lonely"
    HUNGRY = "Hungry"
    DEAD = "Dead"

    
    def __init__(self, world, mood, color, x, y, 
                 id=None, birthTick=None, 
                 gender=None, 
                 fp=80):
        
        #super(Groc, self).__init__()

        self.world = world
        self.world.population += 1
        self.mood = mood
        self.color = color
        self.x = int(x)
        self.y = int(y)
        self.nearestGroc = None
        self.targetX = None
        self.targetY = None
        self.fp = fp
        # constants 
        self.maxfp = 100
        #self.hungerThreshold = 75
        self.hungerThreshold = 66 + self.world.d6(3)
        self.communityRadius = 22
        self.personalRadius = 20
        self.preferredCommunitySize = 4
        self.communityCount = 0
        self.personalCount = 0
        #self.metabolism = .01
        self.metabolism = (91 + self.world.d6(3))/10000
        self.bite = self.metabolism * 100
        self.impatience = self.world.d6(1)
        self.id = self.world.population
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
      distToGroc = self.world.findDistance(self.x, self.y, 
                                           self.nearestGroc.x, 
                                           self.nearestGroc.y)
       
      'determine motion'
      if self.mood == self.DEAD:  
        moving = False
      elif None in (self.targetX, self.targetY):
        moving = False
      else:
        moving = True

      'determine eating'
      if self.mood == self.HUNGRY and not (self.nearestFood is None):
         distToFood = self.world.findDistance(self.x, self.y, 
                                           self.nearestFood.x, 
                                           self.nearestFood.y)
      else:
         distToFood = self.world.findDistance(0, 0, 
                                           self.world.MAXX,
                                           self.world.MAXY)

      if distToFood < self.personalRadius and self.fp < self.maxfp:
        calories = self.nearestFood.bite(self.bite)
        self.fp = self.fp + calories


      'move, or sit still; expend energy accordingly'
      if moving == True:
        self.moveTowardTarget()
        self.fp = self.fp - (2 * self.metabolism)
      else:
        'moving == False'
        self.fp = self.fp - self.metabolism
        zdist = self.world.findDistance(self.x, self.y, 
                                        self.nearestGroc.x, 
                                        self.nearestGroc.y) 
        if zdist < self.personalRadius:
           self.world.render.drawStatic(self, self.x, self.y)
        else:
           self.world.render.maybeDraw(self, self.x, self.y)



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
      distToGroc = self.world.findDistance(self.x, self.y, 
                                           self.nearestGroc.x, 
                                           self.nearestGroc.y)
      if self.nearestFood == None:
        distToFood = self.world.findDistance(self.x, self.y, 
                                           self.world.MAXX, 
                                           self.world.MAXY)
      else:
        distToFood = self.world.findDistance(self.x, self.y, 
                                           self.nearestFood.x, 
                                           self.nearestFood.y)
      if self.fp < 0:
        self.setMood(Groc.DEAD)
      elif self.fp < self.hungerThreshold:
        self.setMood(Groc.HUNGRY)
      elif self.fp < self.maxfp and distToFood < self.personalRadius:
        self.setMood(Groc.HUNGRY)
      elif distToGroc < self.personalRadius:  
        self.setMood(Groc.CROWDED)
      elif distToGroc > self.communityRadius:
        self.setMood(Groc.LONELY)
      else:
        self.setMood(Groc.HAPPY)

      if self.mood == self.DEAD:
        pass
      elif self.targetX == self.x and self.targetY == self.y:
        #arrived
        self.targetX = None
        self.targetY = None
      elif self.mood == Groc.HAPPY:
        #stay put when you're happy
        self.targetX = None
        self.targetY = None
      elif self.mood == Groc.HUNGRY:
        if self.nearestFood is None:
          self.targetX = None
          self.targetY = None
        else:  
          self.targetX = self.nearestFood.x
          self.targetY = self.nearestFood.y
      elif self.mood == Groc.LONELY:
        #continually retarget nearest groc when lonely
        self.targetX = self.nearestGroc.x
        self.targetY = self.nearestGroc.y
      elif self.mood == Groc.CROWDED:
        #pick a target one time when crowded
        if self.targetX is None and self.targetY is None:
          pct = self.world.percentage()
          if pct <= (100-self.impatience):
            self.targetX, self.targetY = self.getAwayFrom(self.nearestGroc.x, self.nearestGroc.y)
            if self.targetX == self.x and self.targetY == self.y:
              self.targetX, self.targetY = self.chooseLessCrowdedSpace(
                                               self.communityRadius)
          else:
            self.targetX, self.targetY = self.world.randomLocation()
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
                str(self.birthTick) + ", '" + str(self.gender) +  "'," + 
                str(round(self.fp, 3)) + ")" + self.world.NEWLINE)

# groc.findNearestFood
    def findNearestFood(self):
        if self.gender == self.FEMALE:
          nearestx = self.world.MAXX
          nearesty = self.world.MAXY 
          leastDist = self.world.findDistance(0, 0, nearestx, nearesty)
          nearestFood = None
          for someFood in self.world.foodList:
            zDist = self.world.findDistance(self.x, self.y, 
                               someFood.x, someFood.y)
            if zDist < leastDist:
              leastDist = zDist
              nearestFood = someFood
        else:
          strongestOdor = 0
          nearestFood = None
          for someFood in self.world.foodList:
            zDist = self.world.findDistance(self.x, self.y, 
                               someFood.x, someFood.y)
            if zDist == 0:
              odor = 100
            else:
              odor = max(0,(100-self.fp)) + someFood.calories / (2*zDist)
            if odor > strongestOdor:
              strongestOdor = odor
              nearestFood = someFood
        return nearestFood

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

# groc.getAwayFrom
    def getAwayFrom(self, x, y):
        if None in (x,y):
          newX = self.x 
          newY = self.y
        else:
          diffX = self.x - x
          diffY = self.y - y
          newX = self.x + diffX
          newY = self.y + diffY
        return newX, newY

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
                   " Birthtick: " + str(self.birthTick) + 
                   " Food Points: " + str(self.fp) + 
                   " Hunger Treshold " + str(self.hungerThreshold) + 
                   " Metabolism " + str(self.metabolism))
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
            xdiff = abs(self.targetX - newX)
            ydiff = abs(self.targetY - newY)
            if xdiff > ydiff:
              if newX < self.targetX:
                newX = newX + 1
              elif newX > self.targetX:
                newX = newX - 1
            else:
              if newY < self.targetY:
                newY = newY + 1
              elif newY > self.targetY:
                newY = newY - 1
          self.world.render.drawMoving(self, self.x, self.y, newX, newY)
          self.x = newX
          self.y = newY

# groc.observe
    def observe(self):
        self.nearestGroc = self.findNearestGroc()
        self.nearestFood = self.findNearestFood()
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
  thisWorld.start(sys.argv)
  while thisWorld.keepRunning():
    thisWorld.tick()
  thisWorld.end()
            
if __name__ == '__main__':
    main()
