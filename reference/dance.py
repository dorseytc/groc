import pygame
import world
import sys
import time

def solveForX(radius, ax, ay, sy):
  sx = ((((radius ** 2) - ((sy - ay) ** 2)) ** .5) + ax)
  print("sfx", sx)
  return sx
def solveForY(radius, ax, ay, sx):
  sy = ((((radius ** 2) - ((sx - ax) ** 2)) ** .5) + ay)
  print("sfy", sy)
  return sy
def pickCompass(self, anchor):
  xdiff = abs(self.x - anchor.x)
  ydiff = abs(self.y - anchor.y)
  if self.x < anchor.x:
    'left half of the compass'
    if self.y < anchor.y:
      result = 'NW'
      if xdiff > ydiff:
        finer = 'WNW'
      else:
        finer = 'NNW'
    elif self.y > anchor.y:
      result = 'SW' 
      if xdiff > ydiff:
        finer = 'WSW'
      else:
        finer = 'SSW'
    else:
      result = 'W'
      finer = 'W'
  elif self.x > anchor.x:
    'right half of the compass'
    if self.y < anchor.y:
      result = 'NE'
      if xdiff > ydiff:
        finer = 'ENE'
      else:
        finer = 'NNE'
    elif self.y > anchor.y:
      result = 'SE'
      if xdiff > ydiff: 
        finer = 'ESE' 
      else:
        finer = 'SSE'
    else:
      result = 'E'
      finer = 'E'
  else:
    'middle of the compass'
    if self.y < anchor.y:
      result = 'N'
      finer = 'N'
    elif self.y > anchor.y:
      result = 'S'
      finer = 'S'
    else: 
      result = 'O'
      finer = 'O'
  return result, finer

def orbitTarget1(self, anchor, radius, clockwise=True):
      zdist = self.world.findDistance(self, anchor) 
      xdiff = (self.x - anchor.x)
      ydiff = (self.y - anchor.y) 
      print("zdist", zdist)
      if zdist < radius: 
        print("inside the orbit")
        targetX = self.x
        targetY = solveForY(radius, anchor.x, anchor.y, targetX)
      elif zdist > radius:
        print("outside the orbit")
        targetX, targetY = (anchor.x, anchor.y) 
      elif zdist == radius:
        print("orbit")
        if xdiff <= 0 and ydiff <= 0:
          'upper left - NW'
          if abs(xdiff) > abs(ydiff):
            'NNW'
            targetY = self.y - 5 
            targetX = solveForX(radius, anchor.x, anchor.y, targetY)
          else:
            'WNW'
            targetX = self.x + 5
            targetY = solveForY(radius, anchor.x, anchor.y, targetX)
        elif xdiff >= 0 and ydiff <= 0:
          'upper right - NE' 
          if abs(xdiff) > abs(ydiff):
            'ENE'
            targetY = self.y + 5
            targetX = solveForX(radius, anchor.x, anchor.y, targetY)
          else:
            'NNE'
            targetX = self.x + 5
            targetY = solveForY(radius, anchor.x, anchor.y, targetX)
        elif xdiff >= 0 and ydiff >= 0:
          'lower right - SE'
          if abs(xdiff) > abs(ydiff):
            'ESE'
            targetY = self.y + 5
            targetX = solveForX(radius, anchor.x, anchor.y, targetY)
          else:
            'SSE'
            targetX = self.x - 5
            targetY = solveForY(radius, anchor.x, anchor.y, targetX)
        elif xdiff <= 0 and ydiff >= 0:
          'lower left - SW'
          if abs(xdiff) > abs(ydiff):
            'SSW'
            targetY = self.y - 5
            targetX = solveForX(radius, anchor.x, anchor.y, targetY)
          else:
            'ESE'
            targetX = self.x - 5
            targetY = solveForY(radius, anchor.x, anchor.y, targetX)
      return (targetX, targetY)

def orbitTarget2(self, anchor, radius, clockwise=True):
  compass, finer = pickCompass(self, anchor)   
  targetX = self.x
  targetY = self.y
  if finer in ('WSW', 'W', 'WNW'):
    targetY = targetY - 5 
    targetX = round(solveForX(radius, anchor.x, anchor.y, targetY))
  elif finer in ('NNW', 'N', 'NNE'):
    targetX = targetX + 5
    targetY = round(solveForY(radius, anchor.x, anchor.y, targetX))
  elif finer in ('ENE', 'E', 'ESE'):
    targetY = targetY + 5 
    targetX = round(solveForX(radius, anchor.x, anchor.y, targetY))
  elif finer in ('SSE', 'S', 'SSW'):
    targetX = targetX - 5
    targetY = round(solveForY(radius, anchor.x, anchor.y, targetX))
  else:
    targetX = self.x
    targetY = self.y
  return (targetX, targetY)

def main():
  theWorld = world.World(1920,930)
  theWorld.start(sys.argv)
  gaugeText = []
  gauge = []
  gaugeRect = []
  i = 0
  worldcolor = theWorld.WHITE
  eyecolor = theWorld.BLACK
  theWorld.render.screen.fill(worldcolor)
  pygame.display.set_caption("Animation Test")
  theWorld.getGrocs(2)
  theWorld.spawnFood(500, 400, 300) 
  theFood = theWorld.foodList[0]
  fontname = '/usr/share/fonts/truetype/ubuntu/UbuntuMono-R.ttf'
  largeFont = pygame.font.Font(fontname, 20)
  running = True 
  while running:
    pygame.display.flip()
    theWorld.render.screen.fill(worldcolor)
    for j in range(len(theWorld.grocList)):
      yo = theWorld.grocList[j]
      direction, finer = pickCompass(yo, theFood)
      gaugeText = "Heading " + direction + " (" + finer + ")" +  str(yo.x) + "," + str(yo.y) + " Target " + str(yo.targetX) + "," + str(yo.targetY) + " Orbital Index: " + str(yo.orbitalIndex) + " #" + str(yo.orbiterNumber) + " Anchor " + str(theFood) + " Leader " + str(yo.orbitalLeader)
      gauge = largeFont.render(gaugeText, True, theWorld.GREEN, theWorld.BLACK)
      gaugeRect = gauge.get_rect()
      gaugeRect.topleft = (5, 5 + (20*j))
      theWorld.render.screen.blit(gauge, gaugeRect)     
      theWorld.render.drawGrocStatic(yo, yo.x, yo.y)
      theWorld.render.drawFood(theFood)
      yo.doOrbit(theFood, 100)
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          running = False
    i += 1
    time.sleep(theWorld.defaultTick)

if __name__ == '__main__':
   main()
