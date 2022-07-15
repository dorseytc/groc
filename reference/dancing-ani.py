import pygame
import groc
import world
import sys
import time

def main():
  theWorld = world.World(1920,930)
  theWorld.start(sys.argv)
  theGroc = []
  i = 0
  worldcolor = theWorld.BLACK
  eyecolor = theWorld.BLACK
  theWorld.render.screen.fill(worldcolor)
  pygame.display.set_caption("Animation Test")
  theGroc.append(groc.Groc(theWorld, groc.Groc.SLEEPING, 
                           300, 300, 300, 300, 'M', 100))
  theGroc.append(groc.Groc(theWorld, groc.Groc.SLEEPING, 
                           400, 300, 300, 300, 'F', 100))
  theGroc.append(groc.Groc(theWorld, groc.Groc.SLEEPING, 
                           300, 400, 400, 300, 'M', 100))
  theGroc.append(groc.Groc(theWorld, groc.Groc.SLEEPING, 
                           400, 400, 400, 300, 'F', 100))
  theGroc.append(groc.Groc(theWorld, groc.Groc.HUNGRY,
                           300, 500, 400, 300, 'M', 100))
  theGroc.append(groc.Groc(theWorld, groc.Groc.HUNGRY,
                           400, 500, 400, 300, 'F', 100))
  running = True 
  while running:
    pygame.display.flip()
    theWorld.render.screen.fill(worldcolor)
    for j in range(len(theGroc)):
      x = theGroc[j].x
      y = theGroc[j].y
      if theGroc[j].gender == theGroc[j].MALE:
        groccolor = theWorld.BLUE
      else:
        groccolor = theWorld.RED
      if j in (0,1):
        cycle = 4
        if (i % cycle) - (cycle/2) < 0:
          polarity = 1
        else:
          polarity = -1
        intensity = 4
        pygame.draw.circle(theWorld.render.screen, groccolor, 
                     (x, y), 9)
        pygame.draw.circle(theWorld.render.screen, eyecolor, 
                           (x, y), intensity)
        pygame.draw.line(theWorld.render.screen, worldcolor, 
                         (x - 7, y + (3*polarity)), (x + 7, y + (3*polarity)))
        pygame.draw.line(theWorld.render.screen, worldcolor, 
                         (x - 6, y + (5*polarity)), (x + 6, y + (5*polarity)))
        pygame.draw.line(theWorld.render.screen, worldcolor, 
                         (x - 5, y + (7*polarity)), (x + 5, y + (7*polarity)))
      elif j in (2,3):
        cycle = 6
        if (i % cycle) - (cycle/2) < 0:
          polarity = 1
        else:
          polarity = -1
        intensity = 4
        pygame.draw.circle(theWorld.render.screen, groccolor, 
                     (x, y), 9)
        pygame.draw.circle(theWorld.render.screen, eyecolor, 
                           (x, y), intensity)
        pygame.draw.line(theWorld.render.screen, worldcolor, 
                         (x - 7, y + (3*polarity)), (x + 7, y + (3*polarity)))
        pygame.draw.line(theWorld.render.screen, worldcolor, 
                         (x - 6, y + (5*polarity)), (x + 6, y + (5*polarity)))
        pygame.draw.line(theWorld.render.screen, worldcolor, 
                         (x - 5, y + (7*polarity)), (x + 5, y + (7*polarity)))
      elif j in (4,5):
        cycle = 8
        if (i % cycle) - (cycle/2) < 0:
          polarity = 1
        else:
          polarity = -1
        intensity = 4
        pygame.draw.circle(theWorld.render.screen, groccolor, 
                     (x, y), 9)
        pygame.draw.circle(theWorld.render.screen, eyecolor, 
                           (x, y), intensity)
        pygame.draw.line(theWorld.render.screen, worldcolor, 
                         (x - 7, y + (3*polarity)), (x + 7, y - (3*polarity)))
        pygame.draw.line(theWorld.render.screen, worldcolor, 
                         (x - 6, y + (5*polarity)), (x + 6, y - (5*polarity)))
        pygame.draw.line(theWorld.render.screen, worldcolor, 
                         (x - 5, y + (7*polarity)), (x + 5, y - (7*polarity)))
         
       
      
    i += 1
    time.sleep(theWorld.defaultTick)

if __name__ == '__main__':
   main()
