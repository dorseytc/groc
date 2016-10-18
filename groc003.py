#   Groc
#
#   Version Author  Date        Comment
#   001     tcd     10/16/16    Created
#   002     tcd     10/16/16    Saving the world
#   003     tcd     10/16/16    Retrieving saved world

import datetime, numpy
import matplotlib.pyplot as plt

class Groc:
    'Base class for the groc'
    grocCount = 0    
    datafile = "/home/ted/py/groc/grocfile.dat"
    fieldsep = '|'
    
    def __init__(self, name, mood, color, x=None, y=None, id=None, birthdatetime=None):
        Groc.grocCount += 1
        self.name = name
        self.mood = mood
        self.color = color
        if x == None:
            self.x = numpy.random.random_integers((-1*(1+Groc.grocCount)), (1+Groc.grocCount))
        else:
            self.x = x
        if y == None:
            self.y = numpy.random.random_integers((-1*(1+Groc.grocCount)), (1+Groc.grocCount))
        else:
            self.y = y
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



    
grocList = []


savedFile = open(Groc.datafile, "r")
line = savedFile.readline()
while line: 
    list = line.split(Groc.fieldsep)
    birthdatetime = datetime.datetime.strptime(list[6].rstrip('\n'), "%Y-%m-%d %H:%M")
    newGroc = Groc(list[0],list[1], list[2], list[3], list[4], list[5], birthdatetime)
    newGroc.identify()
    grocList.append(newGroc)
    line = savedFile.readline()
savedFile.close()
    

    
grocList[1].census()
worldsize = 1+ grocList[1].getCount()
mapMark = 'g^'

world = plt.figure()
ax = world.add_subplot(111)
p = ax.plot((-1*worldsize), (-1*worldsize), mapMark, (-1*worldsize), worldsize, mapMark, worldsize, worldsize, mapMark, worldsize, (-1*worldsize), mapMark)
ax.set_xlabel('X Longitude')
ax.set_ylabel('Y Latitude')
ax.set_title('Groc World Map')
for thisGroc in grocList:
    thisGroc.introduce()
    thisGroc.identify()
    thisGroc.locate()
    p = ax.plot(thisGroc.x, thisGroc.y, 'bo')
    

plt.show()

grocFile = open(Groc.datafile, "w")
nl = "\n"
for thisGroc in grocList:
    grocText = thisGroc.dump()
    print grocText
    grocFile.write(grocText+nl)

grocFile.close()

            
