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
        

        

grocList = []
for count in range(0, 10):
    name = 'G'+str(count)
    print name
    newGroc = Groc(name, 'happy', 'green')
    newGroc.identify()
    newGroc.introduce()
    newGroc.locate()
    grocList.append(newGroc)
    
grocList[count].census()

for thisGroc in grocList:
    thisGroc.introduce()
    thisGroc.identify()
    thisGroc.locate()
    
continent = plt.figure()
