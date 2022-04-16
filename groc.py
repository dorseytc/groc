import datetime, numpy
import matplotlib.pyplot as plt

class Groc:
    'Base class for the groc'
    grocCount = 0    
    
    def __init__(self, name, mood, color):
        self.name = name
        self.mood = mood
        self.color = color
        'latitude is vertical coordinate y'
        self.latitude = numpy.random.random_integers((-1*(1+Groc.grocCount)), (1+Groc.grocCount))
        'longitude is horizontal coordinate x'
        self.longitude = numpy.random.random_integers((-1*(1+Groc.grocCount)), (1+Groc.grocCount))
        Groc.grocCount += 1
        self.id = Groc.grocCount
        self.birthdatetime = datetime.datetime.now()
        
    def introduce(self):
        print "My name is " + self.name + ".  I am " + self.color + " and I am feeling " + self.mood
        
    def identify(self):
        print "My ID is " + str(self.id) + " and I was born " + self.birthdatetime.strftime("%Y-%m-%d %H:%M")
        
    def locate(self):
        print self.name + " is at " + str(self.latitude) + ", " + str(self.longitude)
        
    def census(self):
        print "Total Groc Population is ", Groc.grocCount        

    def getCount(self):
        return self.grocCount

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
    p = ax.plot(thisGroc.longitude, thisGroc.latitude, 'bo')
    

plt.show()
