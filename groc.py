#!/usr/bin/python
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
#   TDORSEY     2022-04-28  Pipe location to world.py


import datetime, numpy, logging, os

# limiters

K_GROC_LIMIT = 2
K_ITER_LIMIT = 300

# world dimensions
K_MAXX = 80
K_MAXY = 24

# cardinal directions
K_NONE = 0 
K_NORTH = 1
K_EAST = 2
K_SOUTH = 3
K_WEST = 4

# Init Code
pipe = "/tmp/grocpipe"
print ("start world.py to continue")
if os.path.exists(pipe):
  os.unlink(pipe)
if not os.path.exists(pipe):
  os.mkfifo(pipe, 0o600)
  wpipe = open(pipe, 'w', newline='\n')

Log_Format = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename = "groclog.log", 
                    filemode = "w", 
                    format = Log_Format, 
                    level = logging.DEBUG)
logger = logging.getLogger()

class Groc():
    'Base class for the groc'
    grocCount = 0    
    grocfile = "/home/ted/git/groc/grocfile.dat"
    fieldsep = '|'
    newline = "\n"
    
    def __init__(self, name, mood, color, x=None, y=None, id=None, 
                 birthdatetime=None, isMoving=False, direction=0):
        
        super(Groc, self).__init__()

        Groc.grocCount += 1
        self.name = name
        self.mood = mood
        self.color = color
        if x == None:
            self.x = numpy.random.randint(1, K_MAXX)
        else:
            self.x = int(x)
        if y == None:
            self.y = numpy.random.randint(0,K_MAXY)
        else:
            self.y = int(y)
        if id == None:
            self.id = Groc.grocCount
        else:
            self.id = Groc.grocCount
            #self.id = id
        if birthdatetime == None:
            self.birthdatetime = datetime.datetime.now()
        else:
            self.birthdatetime = birthdatetime
        self.isMoving = isMoving
        logger.debug ("Groc " + str(self.id) + 
                      " X,Y:" + str(self.x) + "," + str(self.y))
        self.direction = direction
       
# move 
    def move(self, oldX, oldY, newX, newY):
        wpipe.write(str(self.id) + "," + str(oldX) + "," + str(oldY) + "," +
                    str(newX) + "," + str(newY) + "\n")
        
# setMotion
    def setMotion(self, isMoving):
        logger.debug ("setMotion Groc:" + str(self.id) + " isMoving: " + 
                      str(isMoving))
        self.isMoving = isMoving

# setDirection
    def setDirection(self, direction=0):
        self.direction = direction

# update        
    def update(self):
        logger.debug ("update Groc " + str(self.id) + " isMoving? " + 
                      str(self.isMoving) + " Direction? " + 
                      str(self.direction) + " " + str(self.x) + "," + 
                      str( self.y))
        oldX = self.x
        oldY = self.y
        if self.isMoving == True:
            if self.direction == K_NORTH:
                self.y += 1
            elif self.direction == K_SOUTH:
                self.y += -1
            elif self.direction == K_EAST:
                self.x += 1
            elif self.direction == K_WEST:
                self.x += -1
                
            if self.x < 0:
                self.x = 0
                if self.direction == K_WEST:
                    self.direction = K_NORTH
            elif self.y > K_MAXX:
                self.y = K_MAXX
                if self.direction == K_EAST:
                    self.direction = K_SOUTH
            elif self.y <= 0:
                self.y = 0
                if self.direction == K_NORTH:
                    self.direction = K_EAST
            elif self.y >= K_MAXY:
                self.y = K_MAXY   
                if self.direction == K_SOUTH:
                    self.direction = K_WEST
            self.move(oldX, oldY, self.x, self.y)
        else:
            logger.debug ("UPDATE Groc " + str(self.id) + " has nothing to do")
 
 
 
 
# introduce 
    def introduce(self):
        logger.debug ("My name is " + self.name + ".  I am " + self.color + 
                      " and I am feeling " + self.mood)
        
# identify
    def identify(self):
        logger.debug ("My ID is " + str(self.id) + " and I was born " + 
                      self.birthdatetime.strftime("%Y-%m-%d %H:%M"))
        
# locate
    def locate(self):
        logger.debug ("Groc " + self.name + " at " + str(self.y) + ", " + 
                      str(self.x) + ") Moving: " +str(self.isMoving) +  
                      " Direction: " + str(self.direction))
        
# census
    def census(self):
        logger.debug ("Total Groc Population is " + str(Groc.grocCount))

# getCount
    def getCount(self):
        return self.grocCount
    
# dump
    def dump(self):
        fs = Groc.fieldsep
        return ( self.name + fs + self.mood + fs + self.color + fs + 
               str(self.x) + fs + str(self.y) + fs + str(self.id) + fs + 
               self.birthdatetime.strftime("%Y-%m-%d %H:%M"))






# main

def main():   
  grocList = [] 
  #
  #Reading the world
  #
  savedFile = open(Groc.grocfile, "r")
  grocsRead = 0 
  line = savedFile.readline()
  while line: 
    grocsRead += 1
    list = line.split(Groc.fieldsep)
    birthdatetime = datetime.datetime.strptime(list[6].rstrip('\n'), 
                                               "%Y-%m-%d %H:%M")        
    newGroc = Groc(list[0],list[1], list[2], list[3], list[4], list[5], 
                   birthdatetime)
    newGroc.identify()
    newGroc.locate()
    grocList.append(newGroc)
    line = savedFile.readline()
  savedFile.close()      
  if grocsRead == 0: 
    for count in range(0, K_GROC_LIMIT):
      name = 'G'+str(count)
      newGroc = Groc(name, 'happy', 'green')
      newGroc.identify()
      newGroc.introduce()
      newGroc.locate()
      grocList.append(newGroc)
    
  running = True
  counter = 0 
  while running:
    counter += 1
    #
    # Plotting the world
    #
    movingCount = 0 
    for thisGroc in grocList:   
      thisGroc.locate()
      density = 0
      oldX = thisGroc.x
      oldY = thisGroc.y
      for anotherGroc in grocList:
        if anotherGroc.id == thisGroc.id:
          logger.debug ("Groc " + str(thisGroc.id) + 
                        " skip myself when evaluating density")
        elif abs(anotherGroc.x - thisGroc.x) < 20:
          if abs(anotherGroc.y - thisGroc.y) < 20:                        
            if anotherGroc.isMoving == True: 
              logger.debug ("Groc " + str(thisGroc.id) +  
                            " ignoring passers by")
            else:
              density += 1
              logger.debug ("Groc " + str(thisGroc.id) +  
                            " somebody already here, density " + str(density ))
          else:
            logger.debug ("Groc " + str(anotherGroc.id) +  " >20y away " + 
                          str(anotherGroc.x) + "," + str(anotherGroc.y) + 
                          " and I am at "  + str(thisGroc.x) + "," + 
                          str(thisGroc.y))
        else:
          logger.debug ("Groc " + str(anotherGroc.id) + " >20x away " + 
                        str(anotherGroc.x) + "," + str( anotherGroc.y) + 
                        " and I am at " + str(thisGroc.x) + "," + 
                        str(thisGroc.y))
                        
        if thisGroc.isMoving == True:
          if density > 0: 
            logger.debug ("Groc " + str(thisGroc.id) + 
                          " already moving. Density "  + str(density))
          else:
            logger.debug ("Groc " + str(thisGroc.id) +  
                          "stop moving.  Density " + str(density))
            thisGroc.setMotion(False)
        else:
          if density > 20:
            logger.debug ("Groc " + str(thisGroc.id) + 
                          " Crowded.  Start moving. Density "  + str(density))
            thisGroc.setMotion(True)
            thisGroc.setDirection(numpy.random.randint(1,4+1))
          elif density > 10:
            logger.debug ("Groc " + str(thisGroc.id) + 
                          " Comfortable.  Density "  + str(density))
          else:
            thisGroc.setMotion(True)
            thisGroc.setDirection(numpy.random.randint(1,4+1))
            logger.debug ("Groc " + str(thisGroc.id) + 
                          " Lonely, start moving.  Density "  + str(density))
                    
        if thisGroc.isMoving == True:
          movingCount += 1
                
        thisGroc.update()

    if counter > K_ITER_LIMIT:
      running = False
    #
    # Saving The World
    #
    
  grocFile = open(Groc.grocfile, "w")
  nl = Groc.newline
  for thisGroc in grocList:
    grocText = thisGroc.dump()
    grocFile.write(grocText+nl)
    logger.debug ("Groc " + str(thisGroc.id) + " saved")
  grocFile.close()
  
  wpipe.close()
  if os.path.exists(pipe):
    os.unlink(pipe)



            
if __name__ == '__main__':
    main()
