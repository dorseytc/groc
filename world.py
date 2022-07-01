#!/usr/bin/python3
#
#   world.py
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
#   TDORSEY  2022-04-29  Pipe location to world.py 
#   TDORSEY  2022-04-30  Generate grocs up to limit when reading a file
#   TDORSEY  2022-05-01  Refactor groc into groc.py class file
#   TDORSEY  2022-05-02  World owns constants now
#                        Add currentTick and tick to World
#   TDORSEY  2022-05-03  Move load/save to World class
#                        Move pipe definition to World class 
#   TDORSEY  2022-05-04  New groc file format, remove birthdatetime
#   TDORSEY  2022-05-06  Added log level arg
#   TDORSEY  2022-05-07  grocfile.dat contains Groc constructor calls
#   TDORSEY  2022-05-17  Added world stats
#   TDORSEY  2022-05-21  Support external renderers via a standard
#                        class and set of methods
#   TDORSEY  2022-05-22  Pass the world to the renderer for reference
#   TDORSEY  2022-06-08  Split from groc.py
#   TDORSEY  2022-06-15  Air and Ground Temperature
#   TDORSEY  2022-06-16  Compute "24-hour" GrocTime
#   TDORSEY  2022-06-20  Sleep animations



import logging
import math
import os
import random
import time

import groc
import food
import grr_pygame as render
#import grr_pipe as render
import settings
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
    # FILE UTILS
    FIELDSEP = '|'
    NEWLINE = '\n'
    GROCFILE = "grocfile.dat"
    WORLDFILE = "world.dat"
    LOGFILE = "groc.log"
    DEGREESIGN = u'\N{DEGREE SIGN}'

    currentTick = 0    
    currentTime = time.time()
    defaultTick = .1

    # COLORS
    BLACK = (0, 0, 0)
    BLUE = (0, 0, 255)
    GRAY = (159, 159, 159)
    GREEN = (0, 255, 0)
    PALEBLUE = (0, 0, 128)
    RED = (128, 0, 0)
    WHITE = (255, 255, 255)
    YELLOW = (255,233,0) 
    
   

    def __init__(self, x, y):
        self.MAXX = x
        self.MAXY = y
        #population counts
        self.happy = 0
        self.lonely = 0
        self.crowded = 0
        self.hungry = 0
        self.dead = 0
        self.cold = 0
        self.sleeping = 0
        self.eating = 0
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
        self.previousLightLevel = self.lightLevel + .01
        self.airTemperature = .7
        self.groundTemperature = .7
        self.maxDistance = self.findDistanceXY(0, 0, x, y)
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
        newFood = food.Food(self, calories, x, y)
        self.foodList.append(newFood)
        self.render.soundFood()

# world.currentGrocTime
    def currentGrocTime(self):
        curr = (6+(24*((self.currentTick % 10000)/10000))) % 24
        hour = int(curr)
        minute = int((curr-hour)*60)
        if hour > 12:
          hour = hour - 12
          tag = " pm "
        elif hour == 12:
          tag = " pm "
        else:
          tag = " am "
        return (str(hour) + ":" + str(minute).zfill(2) + tag)
        

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
    def findDistance(self, object1, object2):
        'measure the distance between two objects'
        if None in (object1, object2):
          result = None
        else:
          x1, y1 = object1.x, object1.y
          x2, y2 = object2.x, object2.y
          result = self.findDistanceXY(x1, y1, x2, y2)
        return result
        
# world.findDistanceXY
    def findDistanceXY(self, x1, y1, x2, y2):
        'measure the distance between two sets of coordinates'
        if None in (x1, x2, y1, y2):
          result = None
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
        leastDist = self.maxDistance
        nearestItem = None
        for thisItem in itemList:
          zDist = self.findDistanceXY(x, y, thisItem.x, thisItem.y)
          if zDist < leastDist:
            leastDist = zDist
            nearestItem = thisItem
        return nearestItem

# world.findGrocNearXY
    def findGrocNearXY(self, x, y):
        'supply coordinates, find nearest Groc'
        return self.findItemNearXY(self.grocList, x, y)

# world.getAirTemperature
    def getAirTemperature(self):
        return ((self.airTemperature * .999) + 
                (self.lightLevel * .0003) + 
                (self.groundTemperature * .0007)
               )

# world.getGroundTemperature
    def getGroundTemperature(self):
        coreTemp = .60
        return ((self.groundTemperature * .9999) + 
                (self.lightLevel * .00005) + 
                (coreTemp * .00005)
               )

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
            self.render.drawGrocStatic(newGroc, 
                                   self.bindX(newGroc.x), 
                                   self.bindY(newGroc.y))
            builtList.append(newGroc)
            line = savedFile.readline()
          savedFile.close()      
        else:
          grocsRead = 0
        if grocsRead < numGrocs:
          for count in range(0, (numGrocs - grocsRead)):
            newX, newY = self.randomLocation()
            newGroc = groc.Groc(self, groc.Groc.HAPPY, newX, newY)
            newGroc.identify()
            self.render.drawGrocStatic(newGroc, newX, newY)
            builtList.append(newGroc)
        self.grocList = builtList

# world.getLightLevel
    def getLightLevel(self):
      relevantTick = self.currentTick % 10000
      if settings.fixedLightLevel == None:
        if 0 <= relevantTick < 1000:
          result = relevantTick/1000
        elif 1000 <= relevantTick < 5000:
          result = 1
        elif 5000 <= relevantTick < 6000:
          result = (6000-relevantTick)/1000
        elif 6000 <= relevantTick < 10000:
          result = 0 
      else:
        result = settings.fixedLightLevel 
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
      return self.interpolateColor(self.BLACK, self.WHITE, self.lightLevel) 
 
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
          allCalories = sum(foodItem.calories for foodItem 
                 in self.foodList)
          if (allCalories < 50 * self.population and
             len(self.foodList) < .1 * self.population):
              self.spawnFood()
        if len(self.foodList) == 0:
          for i in range(max(2,int(.05 * self.population))):
              self.createFood()
        if self.lightLevel == 0 and self.previousLightLevel > 0:
          self.createFood(1000, self.MAXX/2, self.MAXY/2)

# world.handleGrocs
    def handleGrocs(self):
        movingCount = 0
        happyCount = 0
        lonelyCount = 0
        crowdedCount = 0
        hungryCount = 0
        deadCount = 0
        coldCount = 0
        sleepingCount = 0
        eatingCount = 0
        dancingCount = 0
        i = 0
        while i < len(self.grocList):
          if self.grocList[i].fp <= -5:
            deadGroc = self.grocList.pop(i)
            deadGroc.identify()
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
          if thisGroc.mood == groc.Groc.HAPPY:
            happyCount += 1
          elif thisGroc.mood == groc.Groc.LONELY:
            lonelyCount += 1
          elif thisGroc.mood == groc.Groc.CROWDED:
            crowdedCount += 1
          elif thisGroc.mood == groc.Groc.HUNGRY:
            hungryCount += 1
          elif thisGroc.mood == groc.Groc.DEAD:
            deadCount += 1 
          elif thisGroc.mood == groc.Groc.COLD:
            coldCount += 1
          elif thisGroc.mood == groc.Groc.SLEEPING:
            sleepingCount += 1
          elif thisGroc.mood == groc.Groc.EATING:
            eatingCount += 1
          elif thisGroc.mood == groc.Groc.DANCING:
            dancingCount += 1
        self.setStats(happyCount, lonelyCount, crowdedCount, 
                      hungryCount, deadCount, coldCount, 
                      sleepingCount, eatingCount, dancingCount)

# world.ifNone
    def ifNone(self, thing, alternative):
      if thing == None:
        result = alternative
      else:
        result = thing
      return result

# world.interimSave
    def interimSave(self):
        if self.currentTick % 1000 == 0:
          self.saveGrocs()
          self.saveWorld()
 

# world.interpolateColor
    def interpolateColor(self, color1, color2, scale):
      def interpolateScalar(v1, v2, scale):
        return (scale*v2) + (1-scale)*v1
      result = [None,None,None]
      for i in range(3):
        result[i] = interpolateScalar(color1[i], color2[i], scale)
      return tuple(result)
 
# world.intNone
    def intNone(self, parm):
        if parm == None:
          return None
        else:
          return int(parm)
         
# world.isEnabled
    def isEnabled(self, state):
      if state in settings.enabledStates:
        result = True  
      else:
        result = False
      return result

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

# world.pointsOnACircle
    def pointsOnACircle(self, r, n=100): 
      pi = math.pi
      return [(math.cos(2*pi/n*x)*r, math.sin(2*pi/n*x)*r) for x in range(0,n+1)] 


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
    def setStats(self, happy, lonely, crowded, hungry, 
                 dead, cold, sleeping, eating, dancing):
        self.happy = happy 
        self.lonely = lonely
        self.crowded = crowded
        self.hungry = hungry
        self.cold = cold
        self.sleeping = sleeping
        self.eating = eating
        self.dead = dead
        self.dancing = dancing
        self.population = (happy + lonely + crowded + dancing + 
                           hungry + cold + eating + sleeping)

# world.spawnFood
    def spawnFood(self, calories=None, x=None, y=None):
        if calories == None:
          foodCalories = 500 + (10 * self.hungry)
          foodCalories = foodCalories * self.lightLevel
        else:
          foodCalories = calories * self.lightLevel
        if foodCalories > 0:
          newFood = food.Food(self, foodCalories, x, y)
          self.foodList.append(newFood)
          self.render.soundFood()

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
        self.previousLightLevel = self.lightLevel
        self.lightLevel = self.getLightLevel()
        self.airTemperature = self.getAirTemperature()
        self.groundTemperature = self.getGroundTemperature()
        self.handleGrocs()
        self.handleFood()
        self.interimSave()
        self.render.tick()
        if waitSeconds > 0:
          print("Slow tick ", waitSeconds, " seconds")
        nowTime = time.time()
        if nowTime < self.currentTime + self.defaultTick + waitSeconds:
          time.sleep(self.currentTime + self.defaultTick + 
                     waitSeconds - nowTime)
        if self.currentTick % 1000 == 0:
          print("Light:", self.lightLevel, 
                "Air Temp:", int(self.airTemperature*100), 
                "Ground Temp:", int(self.groundTemperature*100), 
                "Time:", self.currentGrocTime(),
                "Date:", self.currentTick)
        self.currentTime = time.time()
        

        
        
# world.percentage
    def percentage(self):
        return(random.randint(1,100))
