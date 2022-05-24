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
    assert not None in (oldX, oldY, newX, newY), 'Cannot move to None coordinates'
    if theGroc.gender == groc.Groc.MALE:
      groccolor = groc.World.BLUE
    else:
      groccolor = groc.World.RED
    if not None in (theGroc.x, theGroc.y, theGroc.targetX, theGroc.targetY):
      distanceFromTarget = theGroc.world.findDistance(theGroc.x, theGroc.y, 
                            theGroc.targetX, theGroc.targetY) 
    else:
      distanceFromTarget = 0
    hunger = theGroc.hungerThreshold - theGroc.fp 
    if theGroc.mood == groc.Groc.DEAD:
      eyecolor = groccolor
      groccolor = groc.World.BLACK
      intensity = 2
    elif theGroc.mood == groc.Groc.LONELY:
      eyecolor = groc.World.WHITE
      intensity = 2 + round(distanceFromTarget / max(self.world.MAXX, self.world.MAXY) * 6)
    elif theGroc.mood == groc.Groc.CROWDED:
      eyecolor = groc.World.BLACK
      intensity = 2 + round(distanceFromTarget / max(self.world.MAXX, self.world.MAXY) * 6)
    elif theGroc.mood == groc.Groc.HUNGRY:
      eyecolor = groc.World.GRAY
      intensity = 2 + round(hunger/theGroc.hungerThreshold * 6)
    else:
      eyecolor = groccolor
      intensity = 2 
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
    assert not None in (newX, newY), 'Cannot render coordinates of None'
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
