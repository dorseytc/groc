#!/usr/bin/python3
#
# grr_pyg
#
#   receive messages from world.py containing instructions
#   on groc movement.  Uses pygame. (Other versions may use other
#   rendering mechanisms) 
#
#   grr_pyg means
#       groc renderer - pygame
#
# TDORSEY 2022-05-21  Created from the bones of render.py
#     

import pygame 
import groc

class Renderer():
  pygame.init
  pygame.display.set_caption("Grocs")

  def __init__(self, x, y):

    super(Renderer, self).__init__()

    self.screen = pygame.display.set_mode([x, y])
    self.worldcolor = groc.World.WHITE
    self.screen.fill(self.worldcolor)
    self.running = True

 #pygame1.drawMoving
  def drawMoving(self, theGroc, oldX, oldY, newX, newY):
    if theGroc.gender == groc.Groc.MALE:
      groccolor = groc.World.BLUE
    else:
      groccolor = groc.World.RED
    if theGroc.mood == groc.Groc.LONELY:
      eyecolor = groc.World.WHITE
    elif theGroc.mood == groc.Groc.CROWDED:
      eyecolor = groc.World.BLACK
    else:
      eyecolor = groccolor
    if oldX == newX and oldY == newY:
      'has not moved'
      pass
    else:
      pygame.draw.circle(self.screen, self.worldcolor, (oldX, oldY), 10)
    pygame.draw.circle(self.screen, groccolor, (newX, newY), 9)
    pygame.draw.circle(self.screen, eyecolor, (newX, newY), 2)
    #pygame.display.flip()

#     drawStatic
  def drawStatic(self, theGroc, newX, newY):
    self.drawMoving(theGroc, newX, newY, newX, newY)

  def close(self):
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
