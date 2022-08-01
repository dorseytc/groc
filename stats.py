#!/usr/bin/python3
import os
import sys
import time
import groc
import world

def main():
    self = world.World(1920,930, False)
    self.getLogger(50)
    builtList = []
    if os.path.exists(world.World.GROCFILE):
      savedFile = open(world.World.GROCFILE, "r")
      grocsRead = 0 
      line = savedFile.readline()
      while line: 
        grocsRead += 1
        newGroc = eval(line)
        newGroc.identify()
        builtList.append(newGroc)
        line = savedFile.readline()
    savedFile.close()      
    self.moodCounts = dict()
    print(groc.Groc.Mood)
    for item in groc.Groc.Mood:
      print("Item", item, "Value", item.value)
    for thisGroc in builtList:
      if thisGroc.mood in self.moodCounts:
        self.moodCounts[thisGroc.mood] += 1
      else:
        self.moodCounts[thisGroc.mood] = 1
    self.population = sum(self.moodCounts.values())
    print(sorted(self.moodCounts.items()))
    print(sorted(self.moodCounts.items(), key=lambda val:-val[1]))
    print("grocs ", len(builtList)) 
    for key, value in self.moodCounts.items():
      print(key.rjust(12), str(value))


if __name__ == '__main__':
   main()
