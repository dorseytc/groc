#
#   TDORSEY     10/16/16    Created
#   TDORSEY     10/16/16    Saving the world
#   TDORSEY     10/16/16    Retrieving saved world
#   TDORSEY     10/16/16    Improved class and function structure
#   TDORSEY     10/17/16    Rendering via pygame
#   TDORSEY     10/22/16    Some form of pygame hell
#   TDORSEY     04/26/22    Reducing to text based for now
#   

import datetime, numpy


K_NONE = 0 
K_NORTH = 1
K_EAST = 2
K_SOUTH = 3
K_WEST = 4
K_MAXX = 1000
K_MAXY = 600

class Groc():
    'Base class for the groc'
    grocCount = 0    
    datafile = "/home/ted/git/groc/grocfile.dat"
    fieldsep = '|'
    newline = "\n"

    
    def __init__(self, name, mood, color, x=None, y=None, id=None, birthdatetime=None, isMoving=False, direction=0):
        
        super(Groc, self).__init__()
        
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
        
    def setMotion(self, isMoving):
        print ("SETMOTION", self.id, "isMoving", isMoving)
        
        self.isMoving = isMoving
 
    def setDirection(self, direction=0):
        self.direction = direction
        
    def update(self):
        print ("UPDATE", self.id, self.isMoving, self.direction, self.x, self.y)
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
    print ("Done reading saved grocs")
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
    
    running = True
    counter = 0 
    movingCount = 0 
    while running:
        counter += 1
        #
        # Plotting the world
        #
        for thisGroc in grocList:   
            print ("***")
            print ("***")
            print ("*** GROC:", thisGroc.id, thisGroc.isMoving, thisGroc.direction, thisGroc.x, thisGroc.y)
            print ("***")
            print ("***")
        
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
                    else:
                            print (anotherGroc.id, "Groc is more than 20y away ", anotherGroc.x, anotherGroc.y, ", whereas I am at ", thisGroc.x, thisGroc.y)
                else:
                     print (anotherGroc.id, "groc is more than 20x away ", anotherGroc.x, anotherGroc.y, ", whereas I am at ", thisGroc.x, thisGroc.y)
                        
            if thisGroc.isMoving == True:
                if density > 0: 
                    print (thisGroc.id, "already moving", density)
                else:
                    print (thisGroc.id, "stop moving", density)
                    thisGroc.setMotion(False)
            else:
                if density > 20:
                    print (thisGroc.id, "Crowded start moving", density)
                    thisGroc.setMotion(True)
                    thisGroc.setDirection(numpy.random.random_integers(1,4))
                elif density > 10:
                    print (thisGroc.id, "already stopped", density)
                else:
                    thisGroc.setMotion(True)
                    thisGroc.setDirection(numpy.random.random_integers(1,4))
                    print (thisGroc.id, "Lonely start moving", density)
                    
            if thisGroc.isMoving == "True":
                movingCount += 1
                
                
                    
            thisGroc.update()            
              
            print ("***")
            print ("***")
            print ("*** GROC: id, isMoving, direction, x, y ***")
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
