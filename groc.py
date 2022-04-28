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


import datetime, numpy, logging

# limiters

K_GROC_LIMIT = 2
K_ITER_LIMIT = 30

# world dimensions
K_MAXX = 80
K_MAXY = 24

# cardinal directions
K_NONE = 0 
K_NORTH = 1
K_EAST = 2
K_SOUTH = 3
K_WEST = 4

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
    worldfile = "/home/ted/git/groc/world.log"
    fieldsep = '|'
    newline = "\n"
    
    def __init__(self, name, mood, color, x=None, y=None, id=None, birthdatetime=None, isMoving=False, direction=0):
        
        super(Groc, self).__init__()

        Groc.grocCount += 1
        self.name = name
        self.mood = mood
        self.color = color
        if x == None:
            #self.x = numpy.random.random_integers(0,K_MAXX)            
            self.x = numpy.random.randint(1, K_MAXX)
        else:
            self.x = int(x)
        if y == None:
            #self.y = numpy.random.random_integers(0,K_MAXY)
            self.y = numpy.random.randint(0,K_MAXY)
        else:
            self.y = int(y)
        if id == None:
            self.id = Groc.grocCount
        else:
            #i think i want these to be uniquely assigned upon creation of the Groc
            self.id = Groc.grocCount
            #self.id = id
        if birthdatetime == None:
            self.birthdatetime = datetime.datetime.now()
        else:
            self.birthdatetime = birthdatetime
        self.isMoving = isMoving
        logger.debug ("Groc " + str(self.id) + " X,Y:" + str(self.x) + "," + str(self.y))
        self.direction = direction
        
        
        
# setMotion
    def setMotion(self, isMoving):
        logger.debug ("SETMOTION Groc:" + str(self.id) + " isMoving: " + str(isMoving))
        self.isMoving = isMoving

# setDirection
    def setDirection(self, direction=0):
        self.direction = direction

# update        
    def update(self):
        logger.debug ("UPDATE Groc " + str(self.id) + " isMoving? " + str(self.isMoving) + " Direction? " + str(self.direction) + " " + str(self.x) + "," + str( self.y))
        if self.isMoving == True:
            if self.direction == K_NORTH:
                self.y += 1
            elif self.direction == K_SOUTH:
                self.y += -1
            elif self.direction == K_EAST:
                #self.rect.move_ip(1, 0)
                self.x += 1
            elif self.direction == K_WEST:
                #self.rect.move_ip(-1,0)
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
        else:
            logger.debug ("UPDATE Groc " + str(self.id) + " has nothing to do")
 
 
 
 
# introduce 
    def introduce(self):
        logger.debug ("My name is " + self.name + ".  I am " + self.color + " and I am feeling " + self.mood)
        
# identify
    def identify(self):
        logger.debug ("My ID is " + str(self.id) + " and I was born " + self.birthdatetime.strftime("%Y-%m-%d %H:%M"))
        
# locate
    def locate(self):
        logger.debug ("Groc " + self.name + " is at " + str(self.y) + ", " + str(self.x))
        logger.debug ("Groc " + self.name + " isMoving: " +str(self.isMoving) +  " Direction: " + str(self.direction))
        
# census
    def census(self):
        logger.debug ("Total Groc Population is " + str(Groc.grocCount))

# getCount
    def getCount(self):
        return self.grocCount
    
# dump
    def dump(self):
        fs = Groc.fieldsep
        return self.name + fs + self.mood + fs + self.color + fs + str(self.x) + fs + str(self.y) + fs + str(self.id) + fs + self.birthdatetime.strftime("%Y-%m-%d %H:%M")






# main

def main():   
    grocList = [] 
    world = []
    worldline = " " * K_MAXX 

    for i in range(K_MAXY):
      world.append(str(i).zfill(3) + ":" + worldline) 
    
    #
    #Reading the world
    #
    
    savedFile = open(Groc.grocfile, "r")
    grocsRead = 0 
    line = savedFile.readline()
    while line: 
        grocsRead += 1
        list = line.split(Groc.fieldsep)
        birthdatetime = datetime.datetime.strptime(list[6].rstrip('\n'), "%Y-%m-%d %H:%M")        
        newGroc = Groc(list[0],list[1], list[2], list[3], list[4], list[5], birthdatetime)
        newGroc.identify()
        newGroc.locate()
        grocList.append(newGroc)
        line = savedFile.readline()
    savedFile.close()      
    logger.debug ("Done reading saved grocs")
    if grocsRead == 0: 
        for count in range(0, K_GROC_LIMIT):
            name = 'G'+str(count)
            newGroc = Groc(name, 'happy', 'green')
            newGroc.identify()
            newGroc.introduce()
            newGroc.locate()
            grocList.append(newGroc)
        logger.debug ('Spawned grocs')
    else:
        logger.debug ('Retrieved saved grocs')
    
    running = True
    counter = 0 
    while running:
        counter += 1
        #
        # Plotting the world
        #
        movingCount = 0 
        for thisGroc in grocList:   
            logger.debug ("***")
            logger.debug ("***")
            logger.debug ("*** GROC: " + str(thisGroc.id) + " IsMoving? " + str(thisGroc.isMoving) + " Direction? " + str(thisGroc.direction) + " " + str(thisGroc.x) + "," + str( thisGroc.y))
            logger.debug ("***")
            logger.debug ("***")
        
            density = 0
            for anotherGroc in grocList:
                if anotherGroc.id == thisGroc.id:
                    logger.debug ("Groc " + str(thisGroc.id) + " skip myself when evaluating density")
                elif abs(anotherGroc.x - thisGroc.x) < 20:
                    if abs(anotherGroc.y - thisGroc.y) < 20:                        
                        if anotherGroc.isMoving == True: 
                            logger.debug ("Groc " + str(thisGroc.id) +  " ignoring passers by")
                        else:
                            density += 1
                            logger.debug ("Groc " + str(thisGroc.id) +  " somebody already here, density " + str(density ))
                    else:
                            logger.debug ("Groc " + str(anotherGroc.id) +  " is more than 20y away " + str(anotherGroc.x) + "," + str( anotherGroc.y) + " whereas I am at "  + str(thisGroc.x) + "," + str(thisGroc.y))
                else:
                     logger.debug ("Groc " + str(anotherGroc.id) +  " is more than 20x away " + str(anotherGroc.x) + "," + str( anotherGroc.y) + " whereas I am at "  + str(thisGroc.x) + "," + str(thisGroc.y))
                        
            if thisGroc.isMoving == True:
                if density > 0: 
                    logger.debug ("Groc " + str(thisGroc.id) +  " already moving. Density "  + str(density))
                else:
                    logger.debug ("Groc " + str(thisGroc.id) +  "stop moving.  Density " + str(density))
                    thisGroc.setMotion(False)
            else:
                if density > 20:
                    logger.debug ("Groc " + str(thisGroc.id) +  " Crowded.  Start moving. Density "  + str(density))
                    thisGroc.setMotion(True)
                    #thisGroc.setDirection(numpy.random.random_integers(1,4))
                    thisGroc.setDirection(numpy.random.randint(1,4+1))
                elif density > 10:
                    logger.debug ("Groc " + str(thisGroc.id) +  " Comfortable.  Density "  + str(density))
                else:
                    thisGroc.setMotion(True)
                    #thisGroc.setDirection(numpy.random.random_integers(1,4))
                    thisGroc.setDirection(numpy.random.randint(1,4+1))
                    logger.debug ("Groc " + str(thisGroc.id) +  " Lonely, start moving.  Density "  + str(density))
                    
            logger.debug("Groc " + str(thisGroc.id) + " isMoving:" + str(thisGroc.isMoving))
            if thisGroc.isMoving == True:
                movingCount += 1
                
                
                    
            thisGroc.update()            
              
            logger.debug ("***")
            logger.debug ("***")
            logger.debug ("*** GROC: " + str(thisGroc.id) + " IsMoving? " + str(thisGroc.isMoving) + " Direction? " + str(thisGroc.direction) + " " + str(thisGroc.x) + "," + str( thisGroc.y))
            logger.debug ("***")
            logger.debug ("***")
            logger.debug ("****************************************************************************")
            
        logger.debug("Counter: " + str(counter) + " Moving count: " + str(movingCount))
        #if movingCount == 0:
        if counter > K_ITER_LIMIT:
            running = False
    
    #
    # Saving The World
    #
    
    grocFile = open(Groc.grocfile, "w")
    nl = Groc.newline
    for thisGroc in grocList:
        worldline = world[thisGroc.y]
        world[thisGroc.y] = worldline[0:thisGroc.x-1] + "X" + worldline[thisGroc.x:K_MAXX]
        grocText = thisGroc.dump()
        grocFile.write(grocText+nl)
        logger.debug ("Groc " + str(thisGroc.id) + " saved")
    grocFile.close()

    for i in range(K_MAXY):
       print(world[i])


            
if __name__ == '__main__':
    main()
