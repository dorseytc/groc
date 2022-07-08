import food
import world

def main():
  radius = 100
  points = 100
  theWorld = world.World(1000,1000)
  anchor = food.Food(theWorld, 1000, 500, 500)
  orbitalPoints = theWorld.pointsOnACircle(radius, points)
  newList = []
  print (orbitalPoints)
  for spot in orbitalPoints:
    newList.append((spot[0] + anchor.x,spot[1] + anchor.y))
  print (newList)
  

if __name__ == '__main__':
   main()
