#!/usr/bin/python
#
#  world.py
#    
#    python class for world object
#    in an experiment in object oriented ai
#
#
import numpy

print("Loading world")
class World():
    'Base class for the world'
    NORTH = 1
    EAST = 2
    SOUTH = 3
    WEST = 4
    FIELDSEP = '|'
    
    def __init__(self, x, y):
        
        super(World, self).__init__()
         
        self.MAXX = x
        self.MAXY = y
     
    def randomLocation(self):
        newX = numpy.random.randint(1, self.MAXX)  
        newY = numpy.random.randint(1, self.MAXY)
        return (newX, newY)

