#   Groc
#
#   Version Author  Date        Comment
#   001     tcd     10/16/16    Created
#   002     tcd     10/16/16    Saving the world
#   003     tcd     10/16/16    Retrieving saved world
#   004     tcd     10/16/16    Improved class and function structure
#   005     tcd     10/17/16    Rendering via pygame
#   006     tcd     10/22/16    Some form of pygame hell

import datetime, numpy
import matplotlib.pyplot as plt
import os, pygame
from pygame.locals import *
from pygame.compat import geterror


K_NONE = 0 
K_NORTH = 1
K_EAST = 2
K_SOUTH = 3
K_WEST = 4
K_MAXX = 1000
K_MAXY = 600

class Groc(pygame.sprite.Sprite):
    'Base class for the groc'
    grocCount = 0    
    datafile = "/home/ted/py/groc/grocfile.dat"
    fieldsep = '|'
    newline = "\n"
    blank = pygame.Surface((4,4))
    blank.fill((0,0,0))
    blankrect = blank.get_rect()

    
    def __init__(self, name, mood, color, x=None, y=None, id=None, birthdatetime=None, isMoving=False, direction=0):
        
        # i dont understand this
        super(Groc, self).__init__()
        self.surf = pygame.Surface((4,4))
        self.surf.fill((255,255,255))
        self.rect = self.surf.get_rect()
        
        
        
        Groc.grocCount += 1
        self.name = name
        self.mood = mood
        self.color = color
        if x == None:
            self.x = numpy.random.random_integers(0,K_MAXX)            
        else:
            self.x = int(x)
        if y == None:
            self.y = numpy.random.random_integers(0,K_MAXY)
        else:
            self.y = int(y)
        print ("X,Y:", self.x, self.y)
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
        print ("X,Y:", self.x, self.y)
        self.isMoving = isMoving
        self.direction = direction
        self.rect.move_ip(self.x, self.y)
        
    def setMotion(self, isMoving):
        print ("SETMOTION", self.id, "isMoving", isMoving)
        
        self.isMoving = isMoving
 
    def setDirection(self, direction=0):
        self.direction = direction
        
    def update(self):
        print ("UPDATE", self.id, self.isMoving, self.direction, self.x, self.y, self.rect.left, self.rect.top)
        if self.isMoving == True:
            if self.direction == K_NORTH:
                self.rect.move_ip(0, -1)
            elif self.direction == K_SOUTH:
                self.rect.move_ip(0, 1)
            elif self.direction == K_EAST:
                self.rect.move_ip(1, 0)
            elif self.direction == K_WEST:
                self.rect.move_ip(-1,0)
                
            if self.rect.left < 0:
                self.rect.left = 0
                if self.direction == K_WEST:
                    self.direction = K_NORTH
            elif self.rect.right > K_MAXX:
                self.rect.right = K_MAXX
                if self.direction == K_EAST:
                    self.direction = K_SOUTH
            if self.rect.top <= 0:
                self.rect.top = 0
                if self.direction == K_NORTH:
                    self.direction = K_EAST
            elif self.rect.bottom >= K_MAXY:
                self.rect.bottom = K_MAXY   
                if self.direction == K_SOUTH:
                    self.direction = K_WEST
        
            self.x = self.rect.left
            self.y = self.rect.top     
            self.rect.move(self.x, self.y)
            
        else:
            print ("UPDATE", self.id, "nothing to do")
 
    def introduce(self):
        print ("My name is " + self.name + ".  I am " + self.color + " and I am feeling " + self.mood)
        
    def identify(self):
        print ("My ID is " + str(self.id) + " and I was born " + self.birthdatetime.strftime("%Y-%m-%d %H:%M"))
        
    def locate(self):
        print (self.name + " is at " + str(self.y) + ", " + str(self.x))
        print (self.name, "isMoving: ", self.isMoving, "Direction: ", self.direction)
        
    def census(self):
        print ("Total Groc Population is ", Groc.grocCount        )

    def getCount(self):
        return self.grocCount
    
    def dump(self):
        fs = Groc.fieldsep
        return self.name + fs + self.mood + fs + self.color + fs + str(self.x) + fs + str(self.y) + fs + str(self.id) + fs + self.birthdatetime.strftime("%Y-%m-%d %H:%M")



def main():   
    grocList = [] 
    
    
    #
    #Reading the world
    #
    
    savedFile = open(Groc.datafile, "r")
    grocsRead = 0 
    line = savedFile.readline()
    while line: 
        grocsRead += 1
        list = line.split(Groc.fieldsep)
        print (list)
        birthdatetime = datetime.datetime.strptime(list[6].rstrip('\n'), "%Y-%m-%d %H:%M")        
        newGroc = Groc(list[0],list[1], list[2], list[3], list[4], list[5], birthdatetime)
        newGroc.identify()
        newGroc.locate()
        grocList.append(newGroc)
        line = savedFile.readline()
    savedFile.close()      
    if grocsRead == 0: 
        for count in range(0, 10):
            name = 'G'+str(count)
            newGroc = Groc(name, 'happy', 'green')
            newGroc.identify()
            newGroc.introduce()
            newGroc.locate()
            grocList.append(newGroc)
        print ('Spawned grocs')
    else:
        print ('Retrieved saved grocs')
    grocList[1].census()
    
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    running = True
    counter = 0 
    while running:
        counter += 1
        for event in pygame.event.get():
        #
        # Plotting the world
        #
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == QUIT:
                running = False

        screen.fill((0, 0, 0))
        
        movingCount = 0
        for thisGroc in grocList:   
            print ("***")
            print ("***")
            print ("*** GROC:", thisGroc.id, thisGroc.isMoving, thisGroc.direction, thisGroc.x, thisGroc.y)
            print ("***")
            print ("***")
            screen.blit(thisGroc.surf, thisGroc.rect)
            pygame.display.flip()
        
            density = 0
            for anotherGroc in grocList:
                if anotherGroc.id == thisGroc.id:
                    print (thisGroc.id, "skip myself when evaluating density")
                elif abs(anotherGroc.x - thisGroc.x) < 20:
                    if abs(anotherGroc.y - thisGroc.y) < 20:                        
                        if anotherGroc.isMoving == True: 
                            print (thisGroc.id, "ignoring passers by")
                        else:
                            print (thisGroc.id, "somebody already here = density")
                            density += 1
                        
            if thisGroc.isMoving == True:
                if density > 0: 
                    print (thisGroc.id, "already moving", density)
                else:
                    print (thisGroc.id, "stop moving", density)
                    thisGroc.setMotion(False)
            else:
                if density > 0:
                    print (thisGroc.id, "start moving", density)
                    thisGroc.setMotion(True)
                    thisGroc.setDirection(numpy.random.random_integers(1,4))
                else:
                    print (thisGroc.id, "already stopped", density)
                    
            if thisGroc.isMoving == "True":
                movingCount += 1
                
                
                    
            thisGroc.update()            
            screen.blit(thisGroc.surf, thisGroc.rect)
              
            print ("***")
            print ("***")
            print ("*** GROC:", thisGroc.id, thisGroc.isMoving, thisGroc.direction, thisGroc.x, thisGroc.y)
            print ("***")
            print ("***")
            print ("****************************************************************************")
            
        if movingCount == 0:
            if counter > 30:
                running = False
    
    #
    # Saving The World
    #
    
    grocFile = open(Groc.datafile, "w")
    nl = Groc.newline
    for thisGroc in grocList:
        grocText = thisGroc.dump()
        grocFile.write(grocText+nl)
        print (thisGroc.id, 'saved')
    grocFile.close()

            
if __name__ == '__main__':
    main()
