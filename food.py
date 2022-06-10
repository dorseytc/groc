#!/usr/bin/python3
#
#   food.py
#
#     python class for an experiment in object-oriented ai
#     
#
#   TDORSEY  2022-06-09  Split from groc.py


import datetime 
import logging
import math
import os
import random
import sys
import time
#
# choose a renderer here

class Food():
    'New class for food'
    def __init__(self, world, calories=None, x=None, y=None): 
        self.world = world
        self.value = 1
        if None in (x, y):
          x, y = world.randomLocation()
        if None == calories:
          self.calories = 500 + self.world.hungry 
        else:
          self.calories = calories
        self.x = x
        self.y = y
        self.color = (255, 0, 0)
        print(self.identify(), time.ctime())
         
         
# food.__str__
    def __str__(self):
      return self.dump()

# food.__repr__
    def __repr__(self):
      return self.dump()
     

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
                   " Value: " + str(self.value) + 
                   " Count: " + str(len(self.world.foodList)) + 
                   " Light: " + str(self.world.lightLevel) + 
                   " Hungry: " + str(self.world.hungry) + 
                   " Time: " + str(self.world.currentTick % 10000))
        return identity 
 
        
#food.dump
    def dump(self):
        return ("Food(self, '" + str(self.calories) + "', '" + 
                str(self.x) + ", " + str(self.y) + ")" + 
                self.world.NEWLINE)

