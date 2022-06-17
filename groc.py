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
#   TDORSEY  2022-04-29  Brownian motion.  Ability to iterate forever
#   TDORSEY  2022-04-30  Grocs seek nearest groc
#                        Generate grocs up to limit when reading a file
#                        Exit when nobody is moving 
#   TDORSEY  2022-05-01  Refactor groc into groc.py class file
#   TDORSEY  2022-05-02  Add movement methods to Groc
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
#   TDORSEY  2022-05-20  Eliminate numpy
#   TDORSEY  2022-05-24  Add HUNGRY and DEAD moods
#   TDORSEY  2022-05-25  Fix HUNGRY actions
#   TDORSEY  2022-05-26  Food has calories; Groc have foodpoints
#   TDORSEY  2022-06-01  variable bite and metabolism
#   TDORSEY  2022-06-03  Day and night
#   TDORSEY  2022-06-05  Limited vision at night
#   TDORSEY  2022-06-06  Reduce resting metabolism
#   TDORSEY  2022-06-07  Fear of the dark
#   TDORSEY  2022-06-08  Huddle for warmth at night
#   TDORSEY  2022-06-09  Split apart into separate files again
#   TDORSEY  2022-06-11  Update save file constructor syntax
#   TDORSEY  2022-06-15  Grocs respond to air temperature

import random

class Groc():
    'Base class for the groc'
    MALE = "M"
    FEMALE = "F"
    # MOODS
    COLD = "Cold"
    CROWDED = "Crowded"
    HAPPY = "Happy"
    LONELY = "Lonely"
    HUNGRY = "Hungry"
    DEAD = "Dead"
    SLEEPING = "Sleeping"

    
    def __init__(self, world, mood, x, y, 
                 id=None, birthTick=None, 
                 gender=None, 
                 fp=80):
        
        #super(Groc, self).__init__()

        self.world = world
        self.world.population += 1
        self.mood = mood
        self.x = int(x)
        self.y = int(y)
        self.nearestGroc = None
        self.nearestFood = None
        self.targetX = None
        self.targetY = None
        self.fp = fp
        # constants 
        self.maxfp = 100
        #self.hungerThreshold = 75
        self.hungerThreshold = 66 + self.world.d6(3)
        #self.communityRadius = 22
        #self.personalRadius = 20
        self.preferredCommunitySize = 4
        self.communityCount = 0
        self.personalCount = 0
        self.metabolism = .01
        #self.metabolism = (91 + self.world.d6(3))/20000
        self.bite = self.metabolism * 1000
        self.impatience = self.world.d6(1)
        self.id = self.world.population
        if birthTick is None:
          self.birthTick = self.world.currentTick
        else:
          self.birthTick = birthTick
        self.touchedTick = None
        if gender is None:
          self.gender = self.geneticAttributes() 
        else:
          self.gender = gender
        self.vision = 2000
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
      'determine motion'
      if self.mood == self.DEAD:  
        moving = False
      elif None in (self.targetX, self.targetY):
        moving = False
      else:
        moving = True

      'determine eating'
      if self.nearestFood == None:
        pass
      elif (self.distToFood < self.getPersonalRadius() and 
            self.fp < self.maxfp):
        calories = self.nearestFood.bite(self.bite)
        self.fp = self.fp + calories


      'move, or sit still; expend energy accordingly'
      if moving == True:
        self.moveTowardTarget()
        self.fp = self.fp - (2 * self.metabolism)
      else:
        'moving == False'
        if self.world.lightLevel == 0:
          self.fp = self.fp - (self.metabolism/2)
        else:
          self.fp = self.fp - self.metabolism
        if self.world.ifNone(self.distToGroc, self.world.maxDistance) < self.getPersonalRadius():
           self.world.render.drawStatic(self, self.x, self.y)
        else:
           self.world.render.maybeDraw(self, self.x, self.y)



# groc.chooseLessCrowdedSpace
    def chooseLessCrowdedSpace(self, radius, invert=False):
      quadrantNames = ['NW', 'NE', 'SW', 'SE']
      quadrantInfo = {"NW":(-1,-1), "NE":(1,-1), "SW":(-1,1), "SE":(1,1)}
      bestPopulation = 100000
      if self.gender == Groc.MALE:
        direction = -1
      else:
        direction = 1
      for quadrantName in quadrantNames[::direction]:   
        xfactor, yfactor = quadrantInfo[quadrantName]
        population = self.countNearbyGrocs(radius, 
          self.world.bindX(self.x + (xfactor * radius)), 
          self.world.bindY(self.y + (yfactor * radius)))
        if invert == False:
          if population < bestPopulation:
            bestPopulation = population
            targetQuadrant = quadrantName
        else:
          if population < bestPopulation:
            bestPopulation = population
            targetQuadrant = quadrantName
        
      self.world.logger.debug ("Target quadrant is " + 
          targetQuadrant + " " + 
          " population " +  str(bestPopulation))
      xfactor, yfactor = quadrantInfo[targetQuadrant]
      newX = self.world.bindX(self.x + (xfactor * radius))
      newY = self.world.bindY(self.y + (yfactor * radius))
      self.world.logger.debug("newx, newy " + str(newX) + "," + str(newY))
      return newX, newY

# groc.chooseMoreCrowdedSpace
    def chooseMoreCrowdedSpace(self, radius):
      return self.chooseLessCrowdedSpace(radius, True)
 
# groc.countNearbyGrocs
    def countNearbyGrocs(self, searchRadius, x, y):
      'count within a given radius'
      count = 0
      for anotherGroc in self.world.grocList:
        if not (anotherGroc.id == self.id):
          zdist = self.world.findDistanceXY(x, y, 
                                          anotherGroc.x, anotherGroc.y)
          if zdist <= searchRadius:
            count += 1
      return count     
       
# groc.decide
    def decide(self):
      'decide what to do'
      'set mood'
      maxDistance = self.world.maxDistance
      if self.fp < 0:
        self.setMood(Groc.DEAD)
      elif (self.fp < self.hungerThreshold and 
            not self.nearestFood is None):
        'HUNGRY if I can find food'
        self.setMood(Groc.HUNGRY)
      elif (self.fp < self.maxfp and 
            self.world.ifNone(self.distToFood, maxDistance) < self.getPersonalRadius()):
        'HUNGRY since there is food right here'
        self.setMood(Groc.HUNGRY)
      elif self.world.ifNone(self.distToGroc, maxDistance) < self.getPersonalRadius():
        self.setMood(Groc.CROWDED)
      elif self.world.ifNone(self.distToGroc, maxDistance) > self.getCommunityRadius():
        self.setMood(Groc.LONELY)
      elif self.fp < self.hungerThreshold:
        'HUNGRY even if there is no food since I am not crowded or lonely'
        self.setMood(Groc.HUNGRY)
      else:
        self.setMood(Groc.HAPPY)

      'set target'
      if self.mood == self.DEAD:
        pass
      elif self.targetX == self.x and self.targetY == self.y:
        #arrived
        self.targetX, self.targetY = None, None
      elif self.mood == Groc.HAPPY:
        #stay put when you're happy
        self.targetX, self.targetY = None, None
      elif self.mood == Groc.HUNGRY:
        if self.nearestFood is None:
          if None == self.nearestHungryGroc:
            self.targetX, self.targetY = None, None
          elif self.distToHungryGroc > self.getPersonalRadius():
            self.targetX = self.nearestHungryGroc.targetX
            self.targetY = self.nearestHungryGroc.targetY
        elif self.nearestGroc is None:
          'do not venture out for food alone'
          self.targetX, self.targetY = None, None
        else:  
          self.targetX = self.nearestFood.x
          self.targetY = self.nearestFood.y
      elif self.mood in (Groc.LONELY, Groc.COLD):
        #continually retarget nearest groc when lonely and cold
        if self.nearestGroc == None:
          if self.mood == Groc.COLD:
            if None in (self.targetX, self.targetY):
              if self.nearestFood == None:
                if self.nearestHungryGroc == None:
                  self.targetX, self.targetY = self.world.randomLocation()
                else:
                  self.targetX, self.targetY = (self.nearestHungryGroc.x, 
                                                self.nearestHungryGroc.y)
              else:
                self.targetX, self.targetY = (self.nearestFood.x, 
                                              self.nearestFood.y)
          else:
            self.targetX, self.targetY = None, None
        else:  
          self.targetX = self.nearestGroc.x
          self.targetY = self.nearestGroc.y
      elif self.mood == Groc.CROWDED:
        #pick a target one time when crowded
        if self.targetX is None and self.targetY is None:
          pct = self.world.percentage()
          if pct <= (100-self.impatience):
            self.targetX, self.targetY = self.getAwayFrom(
                                               self.nearestGroc.x, 
                                               self.nearestGroc.y)
            if self.targetX == self.x and self.targetY == self.y:
              self.targetX, self.targetY = self.chooseLessCrowdedSpace(
                                               self.getCommunityRadius())
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

# groc.distanceTo
    def distanceTo(self, object):
        return (self.world.findDistance(self, object))

# groc.dump
    def dump(self):
        return ("groc.Groc(self, '" + self.mood + "', " + 
                str(self.x) + ", " + str(self.y) + ", " + 
                str(self.id) + ", " + str(self.birthTick) + ", '" + 
                str(self.gender) +  "'," + str(round(self.fp, 3)) + ")" + 
                self.world.NEWLINE)

# groc.findNearestFood
    def findNearestFood(self):
        if self.gender == self.FEMALE:
          leastDist = self.world.maxDistance
          nearestFood = None
          for someFood in self.world.foodList:
            zDist = self.world.findDistance(self, someFood)
            if zDist < leastDist:
              leastDist = zDist
              nearestFood = someFood
          if leastDist > self.visualRange():
            nearestFood = None
          else:
            pass
        else:
          strongestOdor = 0
          nearestFood = None
          for someFood in self.world.foodList:
            zDist = self.world.findDistance(self, someFood)
            if zDist == 0:
              odor = 100
            else:
              odor = max(0,(100-self.fp)) + someFood.calories / (2*zDist)
            if odor > strongestOdor:
              strongestOdor = odor
              nearestFood = someFood
        return nearestFood

# groc.findNearestGroc
    def findNearestGroc(self, mood=None, mustHaveTarget=False):
        leastDist = self.world.maxDistance
        nearestGroc = None
        for anotherGroc in self.world.grocList:
          if (anotherGroc.id == self.id):
            pass
          elif (None in (anotherGroc.targetX, anotherGroc.targetY) and 
                mustHaveTarget == True):
            pass
          elif (anotherGroc.mood == mood or mood == None):
            zDist = self.world.findDistance(self, anotherGroc)
            if zDist < leastDist:
              leastDist = zDist
              nearestGroc = anotherGroc
          else:
            pass 
        if leastDist > self.visualRange():
          return None
        else:
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

# groc.getCommunityRadius
    def getCommunityRadius(self):
        #return 22 + (10 * self.world.lightLevel)
        return 22


# groc.getPersonalRadius
    def getPersonalRadius(self):
        #return 20 + (10 * self.world.lightLevel)
        return 20

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
                   " Nearest Groc " + str(self.nearestGroc) + 
                   " Nearest Food " + str(self.nearestFood) + 
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
        self.distToGroc = self.world.findDistance(self, 
                                              self.nearestGroc)
        self.nearestFood = self.findNearestFood()
        self.distToFood = self.world.findDistance(self, 
                                              self.nearestFood)
        self.nearestHungryGroc = self.findNearestGroc(Groc.HUNGRY, True)
        self.distToHungryGroc = self.world.findDistance(self, 
                                              self.nearestHungryGroc)
        self.communityCount = self.countNearbyGrocs(
                                   self.getCommunityRadius(), 
                                   self.x, self.y)
        self.personalCount = self.countNearbyGrocs(
                                   self.getPersonalRadius(), 
                                   self.x, self.y)
        
        #other observations eventually

# groc.setMood
    def setMood(self, newMood):
        if self.mood == newMood:
          pass
        else:
          if newMood == Groc.DEAD:
            self.identify()
            print("Groc died " + str(self.id))
          self.mood = newMood
          self.moodSince = self.world.currentTick
          self.world.render.drawStatic(self, self.x, self.y)

# groc.setTarget
    def setTarget(self, newx, newy):
        self.targetX = newx
        self.targetY = newy 

# groc.touch
    def touch(self):
        self.touchedTick = self.world.currentTick

# groc.visualRange
    def visualRange(self):
        return max(self.vision * self.world.lightLevel, 50)
