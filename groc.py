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
#   TDORSEY  2022-06-27  Grocs can dance
#   TDORSEY  2022-07-03  Better cold behavior
#   TDORSEY  2022-07-07  Hunger and loneliness create urgency
#   TDORSEY  2022-07-10  More grockish dancing

import random

class Groc():
    'Base class for the groc'
    MALE = "M"
    FEMALE = "F"
    # MOODS
    COLD = "Cold"
    CROWDED = "Crowded"
    DANCING = "Dancing"
    EATING = "Eating"
    HAPPY = "Happy"
    LONELY = "Lonely"
    HUNGRY = "Hungry"
    DEAD = "Dead"
    SLEEPING = "Sleeping"

    
    def __init__(self, world, mood, x, y, 
                 id=None, birthTick=None, 
                 gender=None, 
                 fp=80, 
                 sp=100):
        
        #super(Groc, self).__init__()

        self.world = world
        self.world.population += 1
        #the world around the groc (from observations)
        self.nearestGroc = None
        self.nearestFood = None
        self.nearestHungryGroc = None
        self.targetX = None
        self.targetY = None
        self.urgency = 1
        self.targetComment = None
        self.orbitalAnchor = None
        self.orbitalIndex = None
        self.orbitalPoints = None
        self.communityCount = 0
        self.personalCount = 0
        #personal variables (the result of decisions and actions)
        self.fp = fp
        self.sp = sp
        self.mood = mood
        self.moodComment = "Initial mood"
        self.moodSince = self.world.currentTick
        self.x = int(x)
        self.y = int(y)
        # constants 
        self.maxfp = 100
        self.hungerThreshold = 66 + self.world.d6(3)
        self.sleepThreshold = 30
        self.metabolism = .01
        self.bite = self.metabolism * 1000
        self.impatience = self.world.d6(1)
        self.id = self.world.population
        # variables with getters (environment affects these)
        self.defaultPersonalSpace = 20
        self.defaultComfortZone = 22
        self.defaultCommunitySpace = 50
        self.defaultEarshot = 100
        self.defaultVisualRange = 2000
        self.defaultPreferredCommunitySize = 4
        # generate if missing
        if birthTick is None:
          self.birthTick = self.world.currentTick
        else:
          self.birthTick = birthTick
        self.touchedTick = None
        if gender is None:
          self.gender = self.geneticAttributes() 
        else:
          self.gender = gender
        if self.world.percentage() < 50:
          self.faceTowards = -1
        else:
          self.faceTowards = 1
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
      elif self.x == self.targetX and self.y == self.targetY:
        moving = False
      else:
        moving = True

      'determine eating'
      if self.nearestFood == None:
        pass
      elif (self.world.findDistance(self, self.nearestFood) < 
              self.getPersonalSpace() and 
            self.fp < self.maxfp):
        calories = self.nearestFood.bite(self.bite)
        self.fp = self.fp + calories


      'move, or sit still; expend energy accordingly'
      if moving == True:
        self.moveTowardTarget(self.urgency)
        if self.mood == Groc.DANCING:
          self.fp = self.fp - self.metabolism
        else:
          self.fp = self.fp - (2 * self.metabolism * self.urgency)
        self.sp = self.sp - (self.urgency * 2)
      elif self.mood == Groc.SLEEPING:
        self.world.render.maybeDraw(self, self.x, self.y)
      else:
        'moving = False'
        self.sp = self.sp - self.urgency
        if self.world.lightLevel == 0:
          self.fp = self.fp - (self.metabolism/2)
        else:
          self.fp = self.fp - self.metabolism
        self.sp = self.sp - self.urgency
        if (self.world.ifNone(
             self.world.findDistance(self, self.nearestGroc), 
             self.world.maxDistance) < self.getPersonalSpace()):
           self.world.render.drawGrocStatic(self, self.x, self.y)
        else:
           self.world.render.maybeDraw(self, self.x, self.y)

# groc.askAboutNearbyFood
    def askAboutNearbyFood(self):
      nearbyGrocs = self.listNearbyGrocs(self.getVisualRange())
      zdist = self.world.maxDistance
      nearestFood = None
      for otherGroc in nearbyGrocs:
        if otherGroc.nearestFood is None:
          pass
        elif otherGroc.mood in (Groc.SLEEPING, Groc.DEAD):
          pass
        else: 
          thisDist = self.world.findDistance(self, otherGroc.nearestFood) 
          if thisDist < zdist:
            nearestFood = otherGroc.nearestFood
            zdist = thisDist
          else:
            pass
      return nearestFood 
   

# groc.canSmell
    def canSmell(self, other):
      return True

# groc.canSee
    def canSee(self, other):
      if other == None:
        result = False
      elif (self.getVisualRange() >= 
            self.world.ifNone(self.world.findDistance(self, other),0)):
        result = True
      else:
        result = False
      return result

# groc.chooseLessCrowdedSpace
    def chooseLessCrowdedSpace(self, radius, invert=False):
      quadrantNames = ['NW', 'NE', 'SW', 'SE']
      quadrantInfo = {"NW":(-1,-1), "NE":(1,-1), "SW":(-1,1), "SE":(1,1)}
      targetQuadrant = None
      if invert:
        bestPopulation = 0
      else:
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
        if targetQuadrant == None:
           bestPopulation = population
           targetQuadrant = quadrantName
        elif invert == False:
          if population < bestPopulation:
            bestPopulation = population
            targetQuadrant = quadrantName
        else:
          if population > bestPopulation:
            bestPopulation = population
            targetQuadrant = quadrantName
        
      self.world.logger.debug ("Target quadrant is " + 
          self.world.ifNone(targetQuadrant, "none") + " " + 
          " population " +  str(self.world.ifNone(bestPopulation, 0)))
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
        if (anotherGroc.id == self.id):
          pass
        elif (anotherGroc.mood == Groc.DEAD):
          pass
        else:
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
      #self.urgency = 1
      if (self.world.isEnabled(Groc.DEAD) 
          and self.fp < 0):
        self.setMood(Groc.DEAD, str(self.fp)+" food points")
      elif (self.world.isEnabled(Groc.EATING) and
            self.fp < self.maxfp and 
            self.world.ifNone(
              self.world.findDistance(self, self.nearestFood), 
              maxDistance) < self.getPersonalSpace()):
        self.setMood(Groc.EATING, "There is food right here")
      elif (self.world.isEnabled(Groc.DANCING) 
            and not self.world.ifNone(self.orbitalAnchor, self.nearestFood) 
                    == None
            and self.fp >= self.hungerThreshold 
            and self.sp >= self.sleepThreshold
            and (self.world.currentTick - self.moodSince) < 1000
            and (self.world.lightLevel < self.world.previousLightLevel
                 or
                 self.world.lightLevel == 0)): 
        self.setMood(Groc.DANCING, "Time to dance")
      elif (self.world.isEnabled(Groc.COLD) and 
            self.world.airTemperature < .45 and
            self.communityCount < self.getPreferredCommunitySize()):
        self.setMood(Groc.COLD, "Cold with no shelter")
      elif (self.world.isEnabled(Groc.HUNGRY) and
            self.fp < self.hungerThreshold and 
            not self.nearestFood is None):
        self.setMood(Groc.HUNGRY, "I can find food")
      elif (self.world.isEnabled(Groc.CROWDED) 
            and self.world.ifNone(
              self.world.findDistance(self, self.nearestGroc), 
              maxDistance) < self.getPersonalSpace()):
        self.setMood(Groc.CROWDED, "Grocs in my space")
      elif (self.world.isEnabled(Groc.HUNGRY) and 
            self.fp < self.hungerThreshold):
        self.setMood(Groc.HUNGRY, "Can't find food")
      elif (self.world.isEnabled(Groc.LONELY) and 
            self.world.ifNone(
              self.world.findDistance(self, self.nearestGroc), 
              maxDistance) > self.getComfortZone()):
        self.setMood(Groc.LONELY, "Grocs too far away")
      elif (self.world.isEnabled(Groc.SLEEPING) and 
            self.mood == Groc.SLEEPING):
        self.setMood(Groc.SLEEPING, "Still asleep")
      else:
        self.setMood(Groc.HAPPY, "Feeling groovy")
  
      if (self.world.isEnabled(Groc.SLEEPING) and 
            self.mood == Groc.HAPPY and 
            (self.world.currentTick - self.moodSince) > 100 and
            (self.world.getLightLevel() == 0 
             or
             self.sp < 0)):
         self.setMood(Groc.SLEEPING, "Catching some Zs")

      'set target'
      if self.mood == Groc.DEAD:
        pass
      elif self.mood == Groc.DANCING:
        if self.orbitalAnchor == None: 
          self.doDance(self.nearestFood, 100)
        else:
          self.doDance(self.orbitalAnchor, 100)
      elif self.targetX == self.x and self.targetY == self.y:
        self.setTarget(None, None, "Arrived")
      elif self.mood == Groc.HAPPY:
        self.setTarget(None, None, "Stay put when you're happy")
      elif self.mood == Groc.HUNGRY:
        if self.nearestFood is None:
          if self.rumoredFood is None:
            self.setTarget(None, None, "Nobody knows where food is")
          else:
            self.setTarget(self.rumoredFood.x, 
                           self.rumoredFood.y,
                           "A friend told me where food is")
            if (self.fp < (self.hungerThreshold/2) and
              self.countFoodCompetitors(self.rumoredFood) > 0): 
                self.urgency = 2
        elif self.nearestGroc is None:
          self.setTarget(None, None, "Do not venture out for food alone")
        else:  
          self.setTarget(self.nearestFood.x, self.nearestFood.y, 
                         "I detected some food nearby")
          if (self.fp < (self.hungerThreshold/2) and
            self.countFoodCompetitors(self.nearestFood) > 0): 
              self.urgency = 2
      elif self.mood == Groc.EATING:
          self.setTarget(None, None, "Nom nom")
      elif self.mood == Groc.LONELY:
        if self.nearestGroc == None:
          self.setTarget(None, None, "I ain't got nobody")
        else:  
          self.setTarget(self.nearestGroc.x, self.nearestGroc.y, 
                         "I detect a friend nearby")
          if (self.world.currentTick - self.moodSince) > 100: 
            self.urgency = 2
      elif self.mood == Groc.COLD:
        if not (self.nearestFood == None):
          self.setTarget(self.nearestFood.x, self.nearestFood.y,
                         "Cold and headed to food")
        elif not (self.rumoredFood == None):
          self.setTarget(self.rumoredFood.x, self.rumoredFood.y,
                         "I heard there was food nearby")
        elif (self.world.ifNone(
                self.world.findDistance(self, self.nearestGroc), 
                maxDistance) < self.getPersonalSpace()):
          self.setTarget(*self.moveAwayFrom(self.nearestGroc.x, 
                                          self.nearestGroc.y), 
                         "Cold and crowded")
        elif not (self.nearestGroc == None):
          self.setTarget(self.nearestGroc.x, self.nearestGroc.y, 
                         "Cold and headed to nearest friend")
        elif (self.getPersonalSpace() <= self.world.ifNone(
                self.world.findDistance(self, self.nearestGroc), 
                maxDistance) <= self.getComfortZone()):
          self.setTarget(None, None, "Cold next to a friend")
      elif self.mood == Groc.CROWDED:
        if self.targetX is None and self.targetY is None:
          pct = self.world.percentage()
          if pct <= (100-self.impatience):
            self.setTarget(*self.moveAwayFrom(self.nearestGroc.x, 
                                            self.nearestGroc.y), 
                           "Getting away from this other groc")
            if self.targetX == self.x and self.targetY == self.y:
              self.setTarget(*self.chooseLessCrowdedSpace(
                               self.getCommunitySpace()), 
                             "Picking a less crowded space")
          else:
            self.setTarget(*self.world.randomLocation(), 
                           "Hiking to get away from the crowd")
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
                "self.bindX(" + str(self.x) + "), " + 
                "self.bindY(" + str(self.y) + "), " + 
                str(self.id) + ", " + 
                str(self.birthTick) + ", '" + 
                self.gender +  "'," + 
                str(round(self.fp, 3)) + ", " + 
                str(round(self.sp, 3)) + ")" + 
                self.world.NEWLINE)

# groc.findBiggestFood
    def findBiggestFood(self, n=1):
      self.world.foodList.sort(key=lambda x: x.calories, reverse=True)
      return self.world.foodList[:n]
      
# groc.countFoodCompetitors
    def countFoodCompetitors(self, theFood):
        leastDist = self.world.maxDistance
        competitorCount = 0
        for anotherGroc in self.world.grocList:
          if (anotherGroc.id == self.id):
            pass
          elif not (anotherGroc.nearestFood == theFood):
            pass
          elif (anotherGroc.mood == Groc.DEAD):
            pass
          elif (self.world.findDistance(self, anotherGroc) > 
                self.getVisualRange()):
            pass
          elif (self.world.findDistance(theFood, anotherGroc) < 
                self.world.findDistance(self, theFood)):
            competitorCount += 1
        return competitorCount
    
      
# groc.findMostCrowdedGroc
    def findMostCrowdedGroc(self):
        biggestGroup = self.communityCount
        bestGroc = self
        bestDist = self.world.maxDistance
        for anotherGroc in self.world.grocList:
          if (anotherGroc.id == self.id):
            pass
          elif (anotherGroc.mood == Groc.DEAD):
            pass
          else:
            thisDist = self.world.findDistance(self, anotherGroc)
            if anotherGroc.communityCount > biggestGroup: 
              biggestGroup = anotherGroc.communityCount
              bestGroc = anotherGroc
              bestDist = thisDist
            elif (anotherGroc.communityCount == biggestGroup and
                  thisDist < bestDist): 
              biggestGroup = anotherGroc.communityCount
              bestGroc = anotherGroc
              bestDist = thisDist
        if bestGroc == self:
          bestGroc == None
        return bestGroc

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
          if self.canSee(nearestFood): 
            pass
          else:
            nearestFood = None
        else:
          strongestOdor = 0
          nearestFood = None
          for someFood in self.world.foodList:
            zDist = self.world.findDistance(self, someFood)
            if zDist == 0:
              odor = 100
            else:
              odor = (max(0,(100-self.fp)) * someFood.calories) / (2*zDist)
            if odor > strongestOdor:
              strongestOdor = odor
              nearestFood = someFood
          if self.canSmell(nearestFood):
            pass
          else:
            nearestFood = None 
        return nearestFood

# groc.listNearbyGrocs
    def listNearbyGrocs(self, radius):
      nearbyGrocs = []    
      for anotherGroc in self.world.grocList:
        if (anotherGroc.id == self.id):
          pass
        elif (anotherGroc.mood == Groc.DEAD):
          pass
        elif radius <= self.world.findDistance(self, anotherGroc):
          nearbyGrocs.append(anotherGroc)
        else:
          pass
      return nearbyGrocs 

# groc.findNearestGroc
    def findNearestGroc(self, 
                        mood=None, 
                        mustHaveTarget=False, 
                        grocList=None):
        if grocList == None:
          grocList = self.world.grocList
        leastDist = self.world.maxDistance
        nearestGroc = None
        for anotherGroc in self.world.grocList:
          if (anotherGroc.id == self.id):
            pass
          elif (anotherGroc.mood == Groc.DEAD):
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
        if leastDist > self.getVisualRange():
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

# groc.getComfortZone
    def getComfortZone(self):
        return self.defaultComfortZone

# groc.getCommunitySpace
    def getCommunitySpace(self):
        return self.defaultCommunitySpace

# groc.getEarshot
    def getEarshot(self):
        return self.defaultEarshot

# groc.getOlfactoryLimit
    def getOlfactoryLimit(self):
        return 0.005

# groc.getPersonalSpace
    def getPersonalSpace(self):
        if self.world.airTemperature < .45: 
          result = 16
        elif self.world.airTemperature > .80:
          result = 22
        else:
          result = 20
        return result

# groc.getPreferredCommunitySize
    def getPreferredCommunitySize(self):
        return self.defaultPreferredCommunitySize

# groc.getVisualRange
    def getVisualRange(self):
        return max(self.defaultVisualRange * self.world.lightLevel, 105)

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
        nl = self.world.NEWLINE
        identity = (
          "Id: " + str(self.id) + " Gender: " + self.gender + 
          nl + 
          "Location " + str(self.x) + "," + str(self.y) + 
          nl + 
          "Target " + str(self.targetX) + "," + str(self.targetY) + 
          " Urgency " + str(self.urgency) + 
          nl + 
          self.world.ifNone(self.targetComment, "") + 
          nl + 
          "Mood: " + self.mood + 
          " Duration: " + str(self.world.currentTick - self.moodSince) +
          nl + 
          self.world.ifNone(self.moodComment, "") + 
          nl + 
          "Food Points: " + str(int(self.fp)) + 
          " Hunger " + str(int(self.hungerThreshold)) + 
          nl + 
          "Sleep Points: " + str(int(self.sp)) + 
          nl + 
          "Nearest Groc " + str(self.world.intNone(
            self.world.findDistance(self, self.nearestGroc))) + 
          nl + 
          "Nearest Food " + str(self.world.intNone(
            self.world.findDistance(self, self.nearestFood))) + 
          nl + 
          "Community Size: " + str(self.communityCount) +
          nl) 
        if not None == self.orbitalAnchor:
          identity = (identity + 
            "Orbiting: " + str(self.orbitalAnchor) + 
            nl + 
            "OrbitalIndex: " + str(self.orbitalIndex) + 
            nl )
        return identity 
 
# groc.moveAwayFrom
    def moveAwayFrom(self, x, y):
        if None in (x,y):
          newX = self.x 
          newY = self.y
        else:
          diffX = self.x - x
          diffY = self.y - y
          newX = self.x + diffX
          newY = self.y + diffY
        return newX, newY

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
          self.world.render.drawGrocMoving(self, self.x, self.y, newX, newY)
          self.x = newX
          self.y = newY

# groc.observe
    def observe(self):
        self.nearestGroc = self.findNearestGroc()
        self.nearestFood = self.findNearestFood()
        if self.nearestFood is None:
          self.rumoredFood = self.askAboutNearbyFood()   
        else:
          self.rumoredFood = None
        
        self.nearestHungryGroc = self.findNearestGroc(Groc.HUNGRY, True)
        self.communityCount = self.countNearbyGrocs(
                                   self.getCommunitySpace(), 
                                   self.x, self.y) + 1
        self.personalCount = self.countNearbyGrocs(
                                   self.getPersonalSpace(), 
                                   self.x, self.y)
        self.mostCrowdedGroc = self.findMostCrowdedGroc()         
        if self.orbitalAnchor == None:
          pass
        elif self.world.foodIsGone(self.orbitalAnchor.x, 
                                  self.orbitalAnchor.y):
          self.orbitalAnchor = None
        #other observations eventually

# groc.findNearestOrbitalIndex
    def findNearestOrbitalIndex(self):
      assert None not in (self.orbitalAnchor, 
        self.orbitalPoints), "invalid parms"
      closestDist = self.world.maxDistance
      for i in range(len(self.orbitalPoints)):
        pos = self.orbitalPoints[i]
        zdist = self.world.findDistanceXY(self.x, self.y, 
                  pos[0] + self.orbitalAnchor.x, 
                  pos[1] + self.orbitalAnchor.y)
        if zdist < closestDist:
          closestDist = zdist
          closestIndex = i 
      return closestIndex



# groc.doDance
    def doDance(self, anchor, radius, points=100):
      assert None not in (anchor, radius, points), "invalid parms"
      def getNthStation(currentStation, n):
        return (currentStation + n) % points
      if not (self.orbitalAnchor == anchor):
        self.orbitalAnchor = anchor
        self.orbitalPoints = self.world.pointsOnACircle(radius, points)
        self.orbitalIndex = self.findNearestOrbitalIndex()
        newX, newY = self.orbitalPoints[self.orbitalIndex]
        self.setTarget(round(newX) + anchor.x, round(newY) + anchor.y, 
                     "Orbital index "  + str(self.orbitalIndex))
      if self.x == self.targetX and self.y == self.targetY:
        aheadIndex = getNthStation(self.orbitalIndex, 9)
        behindIndex = getNthStation(self.orbitalIndex, -9)
        if self.nearestGroc == None:
          self.urgency = 1
        else:
          distAhead = self.world.findDistanceXY(self.nearestGroc.x, 
                        self.nearestGroc.y, 
                        self.orbitalPoints[aheadIndex][0] + anchor.x, 
                        self.orbitalPoints[aheadIndex][1] + anchor.y) 
          distBehind = self.world.findDistanceXY(self.nearestGroc.x, 
                        self.nearestGroc.y, 
                        self.orbitalPoints[behindIndex][0] + anchor.x, 
                        self.orbitalPoints[behindIndex][1] + anchor.y) 
          if distAhead < distBehind:
            self.urgency = 1
          else:
            self.urgency = 2
        self.orbitalIndex = getNthStation(self.orbitalIndex, 1)
        newX, newY = self.orbitalPoints[self.orbitalIndex]
        self.setTarget(round(newX) + anchor.x, round(newY) + anchor.y,
                     "Orbital index "  + str(self.orbitalIndex))
      #self.moveTowardTarget()
        
# groc.exitOrbit
    def exitOrbit(self):
      self.orbitalAnchor = None
      self.orbitalIndex = None
      self.orbitalPoints = None

# groc.isInSameOrbit
    def isInSameOrbit(self, other):
      if other == None:
        result = False
      elif self.orbitalAnchor == other.orbitalAnchor:
        result = True
      else:
        result = False
      return result
          
             
# groc.setMood
    def setMood(self, newMood, comment):
        if self.mood == newMood:
          pass
        else:
          self.urgency = 1
          if newMood == Groc.DEAD:
            self.identify()
            print("Groc died (" + str(self.id) + 
              ") " + str(self.world.currentGrocTime()))
            self.world.render.drawDeath(self)
          elif self.mood == Groc.DANCING:
            self.exitOrbit()
          elif self.mood == Groc.SLEEPING:
            sleepTicks = self.world.currentTick - self.moodSince
            self.sp = self.sp + ((sleepTicks ** 2)/1000)
          self.mood = newMood
          self.moodSince = self.world.currentTick
          self.world.render.drawGrocStatic(self, self.x, self.y)
        self.moodComment = comment

# groc.setTarget
    def setTarget(self, newx, newy, comment):
        self.targetX = newx
        self.targetY = newy 
        self.targetComment = comment
        if newx == None:
          pass 
        elif self.x < newx:
          self.faceTowards = 1
        else:
          self.faceTowards = -1

# groc.touch
    def touch(self):
        self.touchedTick = self.world.currentTick

