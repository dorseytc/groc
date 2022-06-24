import food
import groc
import pygame
import world
import sys
import time
def pointsInCircumference(r, n=100):
  return [(math.cos(2*pi/n*x)*r,math.sin(2*pi/n*x)*r) for x in range(0,n+1)] 
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
  theGroc = []
  gaugeText = []
  gauge = []
  gaugeRect = []
  i = 0
  worldcolor = theWorld.BLACK
  eyecolor = theWorld.BLACK
  theWorld.render.screen.fill(worldcolor)
  pygame.display.set_caption("Animation Test")
  theGroc.append(groc.Groc(theWorld, groc.Groc.DANCING,
                           300, 300, 300, 300, 'M', 100))
  theFood = food.Food(theWorld, 500, 400, 300) 
  fontname = '/usr/share/fonts/truetype/ubuntu/UbuntuMono-R.ttf'
  largeFont = pygame.font.Font(fontname, 20)
  gaugeText.append("Hello Gauge")
  gauge.append(largeFont.render(gaugeText[0], True, 
            theWorld.GREEN, theWorld.BLACK))
  gaugeRect.append(gauge[0].get_rect())
  gaugeRect[0].topleft = (5, 25)
  gaugeText.append("Hello Gauge")
  gauge.append(largeFont.render(gaugeText[1], True, 
            theWorld.GREEN, theWorld.BLACK))
  gaugeRect.append(gauge[1].get_rect())
  gaugeRect[1].topleft = (5, 45)
  """
  theGroc.append(groc.Groc(theWorld, groc.Groc.DANCING, 
                           400, 300, 300, 300, 'F', 100))
  theGroc.append(groc.Groc(theWorld, groc.Groc.DANCING, 
                           300, 400, 400, 300, 'M', 100))
  theGroc.append(groc.Groc(theWorld, groc.Groc.DANCING, 
                           400, 400, 400, 300, 'F', 100))
  theGroc.append(groc.Groc(theWorld, groc.Groc.HUNGRY,
                           300, 500, 400, 300, 'M', 100))
  theGroc.append(groc.Groc(theWorld, groc.Groc.HUNGRY,
                           400, 500, 400, 300, 'F', 100))
  """
  running = True 
  while running:
    pygame.display.flip()
    theWorld.render.screen.fill(worldcolor)
    for j in range(len(theGroc)):
      yo = theGroc[j]
      theWorld.render.drawGrocStatic(yo, yo.x, yo.y)
      theWorld.render.drawFood(theFood)
      direction, finer = pickCompass(yo, theFood)
      yo.targetX, yo.targetY = orbitTarget(yo, theFood, 100)
      stepping = True
      while stepping:
        print("stepping ", yo.x, yo.y, " target ", yo.targetX, yo.targetY)
        yo.moveTowardTarget(3)
        if yo.x == yo.targetX and yo.y == yo.targetY:
          stepping = False
      gaugeText[0] = "Heading " + direction + " (" + finer + ")"
      gauge[0] = largeFont.render(gaugeText[0],
                   True, theWorld.GREEN, theWorld.BLACK)
      theWorld.render.screen.blit(gauge[0], gaugeRect[0])     
      gaugeText[1] = str(yo.x) + "," + str(yo.y) + " Target " + str(yo.targetX) + "," + str(yo.targetY)
      gauge[1] = largeFont.render(gaugeText[1],
                   True, theWorld.GREEN, theWorld.BLACK)
      theWorld.render.screen.blit(gauge[1], gaugeRect[1])     
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          running = False
    i += 1
    time.sleep(theWorld.defaultTick)

if __name__ == '__main__':
   main()
