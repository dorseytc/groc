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
      if j in (0,1):
        frame = (i % 100) 
        intensity = 3 + (abs(50 - frame)/50*5)
        if theGroc[j].gender == theGroc[j].MALE:
          groccolor = theWorld.BLUE
          mouth = intensity/2 - 9
        else:
          groccolor = theWorld.RED
          mouth = 9 - intensity/2
        pygame.draw.circle(theWorld.render.screen, groccolor, 
                     (theGroc[j].x, theGroc[j].y), 9)
        pygame.draw.circle(theWorld.render.screen, eyecolor, 
                           (theGroc[j].x + mouth, theGroc[j].y), intensity)
      elif j in (2,3):
        frame = (i % 100) 
        intensity = 3 + (abs(60 - frame)/50*3)
        if theGroc[j].gender == theGroc[j].MALE:
          groccolor = theWorld.BLUE
          mouth = intensity/2 - 9
        else:
          groccolor = theWorld.RED
          mouth = 9 - intensity/2
        pygame.draw.circle(theWorld.render.screen, groccolor, 
                     (theGroc[j].x, theGroc[j].y), 9)
        pygame.draw.circle(theWorld.render.screen, eyecolor, 
                           (theGroc[j].x + mouth, theGroc[j].y), intensity)
      elif j in (4,5):
        cycle = 10
        frame = (i % cycle)
        intensity = 2 + (abs((cycle/2) - frame)/cycle*6)
        if theGroc[j].gender == theGroc[j].MALE:
          groccolor = theWorld.BLUE
          mouth = intensity/2 - 9
        else:
          groccolor = theWorld.RED
          mouth = 9 - intensity/2
        pygame.draw.circle(theWorld.render.screen, groccolor, 
                     (theGroc[j].x, theGroc[j].y), 9)
        pygame.draw.circle(theWorld.render.screen, eyecolor, 
                           (theGroc[j].x + mouth, theGroc[j].y), intensity)
        for event in pygame.event.get():
          if event.type == pygame.QUIT:
            running = False
         
       
      
    i += 1
    time.sleep(theWorld.defaultTick)

if __name__ == '__main__':
   main()
