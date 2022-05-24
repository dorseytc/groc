#!/usr/bin/python3
#
# grr_pygame
#
#   receive messages from world.py containing instructions
#   on groc movement.  Uses pygame. (Other versions may use other
#   rendering mechanisms) 
#
#   grr_pygame means
#       groc renderer - pygame
#
# TDORSEY 2022-05-21  Created from the bones of render.py
# TDORSEY 2022-05-24  Support HUNGRY and DEAD
#     

import pygame 
import groc

class Renderer():
  pygame.init
  pygame.display.set_caption("Grocs")

  def __init__(self, thisWorld):

    super(Renderer, self).__init__()

    print("Renderer is grr_pyg 1.0")
    self.world = thisWorld
    self.screen = pygame.display.set_mode([self.world.MAXX, 
                                          self.world.MAXY])
    self.worldcolor = self.world.WHITE
    self.screen.fill(self.worldcolor)
    self.running = True

 #pygame1.drawMoving
  def drawMoving(self, theGroc, oldX, oldY, newX, newY):
    if theGroc.gender == groc.Groc.MALE:
      groccolor = groc.World.BLUE
    else:
      groccolor = groc.World.RED
    if theGroc.mood == groc.Groc.DEAD:
      groccolor = groc.World.BLACK
      eyecolor = groc.World.BLACK
    elif theGroc.mood == groc.Groc.LONELY:
      eyecolor = groc.World.WHITE
    elif theGroc.mood == groc.Groc.CROWDED:
      eyecolor = groc.World.BLACK
    elif theGroc.mood == groc.Groc.HUNGRY:
      eyecolor = groc.World.GRAY
    else:
      eyecolor = groccolor
    if None in (theGroc.x, theGroc.y, theGroc.targetX, theGroc.targetY):
      intensity = 2 
    else:
      zdist = theGroc.world.findDistance(theGroc.x, theGroc.y, 
                                    theGroc.targetX, theGroc.targetY) 
      intensity = 2 + round((zdist / max(self.world.MAXX, self.world.MAXY)) * 6)
    if oldX == newX and oldY == newY:
      'has not moved'
      pass
    else:
      pygame.draw.circle(self.screen, self.worldcolor, (oldX, oldY), 10)
    pygame.draw.circle(self.screen, groccolor, (newX, newY), 9)
    pygame.draw.circle(self.screen, eyecolor, (newX, newY), intensity)
    #pygame.display.flip()

#     drawStatic
  def drawStatic(self, theGroc, newX, newY):
    self.drawMoving(theGroc, newX, newY, newX, newY)

  def close(self):
    print("Awaiting user input to close")
    while (self.running):
      self.tick()
    self.quit()

  def quit(self):
    pygame.quit()

  def tick(self):
    pygame.display.flip()
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.quit()
        self.running = False
      if event.type == pygame.MOUSEBUTTONDOWN:
        x, y = event.pos
        nearestGroc = self.world.findNearbyGroc(x, y) 
        zdist = self.world.findDistance(x, y, nearestGroc.x, nearestGroc.y)
        if zdist > nearestGroc.personalRadius:
          pass
        else:
          print(nearestGroc.identify())
