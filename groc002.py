#   Groc
#
#   Version Author  Date        Comment
#   001     tcd     10/16/16    Created
#   002     tcd     10/16/16    Saving the world

import datetime, numpy
import matplotlib.pyplot as plt

class Groc:
    'Base class for the groc'
    grocCount = 0    
    datafile = "/home/ted/py/groc/grocfile.dat"
    
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
            self.id = id
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
        dumpstring = '"' + self.name + '","' + self.mood + '","' + self.color + '",'
        dumpstring = dumpstring + str(self.x) + ',' + str(self.y) + ',' + str(self.id) + ',"' 
        dumpstring = dumpstring + self.birthdatetime.strftime("%Y-%m-%d %H:%M") + '"'
        return dumpstring
    
    
grocList = []




for count in range(0, 10):
    name = 'G'+str(count)
    newGroc = Groc(name, 'happy', 'green')
    newGroc.identify()
    newGroc.introduce()
    newGroc.locate()
    grocList.append(newGroc)
    
grocList[count].census()
worldsize = 1+ grocList[count].getCount()
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

grocFile = open(datafile, "w")
nl = "\n"
for thisGroc in grocList:
    grocText = thisGroc.dump()
    print grocText
    grocFile.write(grocText+nl)

grocFile.close()

            
