#   Groc
#
#   Version Author  Date        Comment
#   001     tcd     10/16/16    Created
#   002     tcd     10/16/16    Saving the world
#   003     tcd     10/16/16    Retrieving saved world
#   004     tcd     10/16/16    Improved class and function structure
#   005     tcd     10/17/16    Rendering via pygame

import datetime, numpy
import matplotlib.pyplot as plt
import os, pygame
from pygame.locals import *
from pygame.compat import geterror


class Groc(pygame.sprite.Sprite):
    'Base class for the groc'
    grocCount = 0    
    datafile = "/home/ted/py/groc/grocfile.dat"
    fieldsep = '|'
    newline = "\n"
    
    def __init__(self, name, mood, color, x=None, y=None, id=None, birthdatetime=None):
        
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
            self.x = numpy.random.random_integers((-1*(1+Groc.grocCount)), (1+Groc.grocCount))
        else:
            self.x = int(x)
        if y == None:
            self.y = numpy.random.random_integers((-1*(1+Groc.grocCount)), (1+Groc.grocCount))
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
        if self.x < 0: 
            self.x = self.x + 500
        if self.y < 0: 
            self.y = self.y + 300
        self.rect.move_ip(self.x, self.y)
        
    def introduce(self):
        print "My name is " + self.name + ".  I am " + self.color + " and I am feeling " + self.mood
        
    def identify(self):
        print "My ID is " + str(self.id) + " and I was born " + self.birthdatetime.strftime("%Y-%m-%d %H:%M")
        
    def locate(self):
        print self.name + " is at " + str(self.y) + ", " + str(self.x)
        
    def census(self):
        print "Total Groc Population is ", Groc.grocCount        

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
        birthdatetime = datetime.datetime.strptime(list[6].rstrip('\n'), "%Y-%m-%d %H:%M")
        newGroc = Groc(list[0],list[1], list[2], list[3], list[4], list[5], birthdatetime)
        newGroc.identify()
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
        print 'Spawned grocs'
    else:
        print 'Retrieved saved grocs'
    grocList[1].census()
    
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    running = True
    while running:
        for event in pygame.event.get():
        #
        # Plotting the world
        #
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == QUIT:
                running = False
        
        for thisGroc in grocList:            
            screen.blit(thisGroc.surf, thisGroc.rect)
            pygame.display.flip()
        
        density = 0
        for anotherGroc in grocList:
            if anotherGroc.x == thisGroc.x:
                if anotherGroc.y == thisGroc.y:
                    density += 1
                    
    
    #
    # Saving The World
    #
    
    grocFile = open(Groc.datafile, "w")
    nl = Groc.newline
    for thisGroc in grocList:
        grocText = thisGroc.dump()
        grocFile.write(grocText+nl)
        print thisGroc.id, 'saved'
    grocFile.close()

            
if __name__ == '__main__':
    main()