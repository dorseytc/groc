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
# TDORSEY 2022-05-25  Add Food
# TDORSEY 2022-05-26  Improve Food rendering
# TDORSEY 2022-05-27  Added sound
# TDORSEY 2022-06-01  Added click identification of food
# TDORSEY 2022-06-03  Day and night
# TDORSEY 2022-06-15  Ground and Air temperature gauge
#                     Grocs get cold

import pygame 


class Renderer():
  pygame.init()
  pygame.font.init()
  pygame.display.set_caption("Grocs")

  def __init__(self, thisWorld):

    super(Renderer, self).__init__()

    print("Renderer is grr_pygame 1.0")
    self.world = thisWorld
    self.screen = pygame.display.set_mode([thisWorld.MAXX, 
                                          thisWorld.MAXY])
    self.worldColor = self.world.WHITE
    self.screen.fill(self.worldColor)
    self.running = True
    self.font = pygame.font.Font('/usr/share/fonts/truetype/ubuntu/UbuntuMono-R.ttf', 12)
    self.text = self.font.render('Temp: ', True, 
                                 self.world.GREEN, self.worldColor)
    self.textRect = self.text.get_rect()
    self.textRect.center = (50, 50)
    pygame.mixer.init()
    self.eat=pygame.mixer.Sound('eat.ogg')
    self.food=pygame.mixer.Sound('food.ogg')
    self.lastSoundTick = self.world.currentTick

#render.drawFood
  def drawFood(self, theFood): 
    if theFood.calories <= 0:
      color = self.worldColor
    else:
      color = theFood.color #(255, 0, 0)
    size = 1 + round((theFood.calories / 500) * 9)
    pygame.draw.rect(self.screen, self.worldColor, pygame.Rect(
                          theFood.x - size+1, 
                          theFood.y - size+1,
                          size+2, size+2))
    pygame.draw.rect(self.screen, color, pygame.Rect(theFood.x - size,
                                                     theFood.y - size, 
                                                     size*2, size*2))
     
#render.drawMoving 
  def drawMoving(self, theGroc, oldX, oldY, newX, newY):
    assert not None in (oldX, oldY, newX, newY), 'Cannot move to None coordinates'
    if theGroc.gender == theGroc.MALE:
      groccolor = self.world.BLUE
    else:
      groccolor = self.world.RED
    distanceFromTarget = self.world.findDistanceXY(theGroc.x, 
                                 theGroc.y, theGroc.targetX, 
                                 theGroc.targetY) 
    hunger = theGroc.hungerThreshold - theGroc.fp 
    if theGroc.mood == theGroc.DEAD:
      eyecolor = groccolor
      groccolor = self.world.BLACK
      intensity = 2
    elif theGroc.mood == theGroc.COLD:
      eyecolor = self.world.YELLOW
      intensity = 3
    elif theGroc.mood == theGroc.LONELY:
      eyecolor = self.world.WHITE
      intensity = 2 + round(distanceFromTarget / 
                      max(self.world.MAXX, self.world.MAXY) * 6)
    elif theGroc.mood == theGroc.CROWDED:
      eyecolor = self.world.BLACK
      intensity = 2 + round(distanceFromTarget / 
                      max(self.world.MAXX, self.world.MAXY) * 6)
    elif theGroc.mood == theGroc.HUNGRY:
      eyecolor = self.world.GRAY
      intensity = 2 + round(hunger / theGroc.hungerThreshold * 6)
    else:
      eyecolor = groccolor
      intensity = 2 
    if oldX == newX and oldY == newY:
      isMoving = False
    else:
      pygame.draw.circle(self.screen, self.worldColor, (oldX, oldY), 10)
      isMoving = True
    if False:
      'turn off visualRange circle'
      pass
    elif theGroc.touchedTick == None:
      pass
    elif self.world.currentTick - theGroc.touchedTick < 50:
      if isMoving:
        pygame.draw.circle(self.screen, self.worldColor, 
                         (oldX, oldY), theGroc.visualRange())
      pygame.draw.circle(self.screen, self.world.YELLOW, 
                         (newX, newY), theGroc.visualRange())
      pygame.draw.circle(self.screen, self.worldColor, 
                         (newX, newY), theGroc.visualRange() - 1)
       
    elif self.world.currentTick - theGroc.touchedTick == 50: 
      if isMoving:
        pygame.draw.circle(self.screen, self.worldColor, 
                         (oldX, oldY), theGroc.visualRange())
      pygame.draw.circle(self.screen, self.worldColor,
                         (newX, newY), theGroc.visualRange())
      
    pygame.draw.circle(self.screen, groccolor, (newX, newY), 9)
    pygame.draw.circle(self.screen, eyecolor, (newX, newY), intensity)

#render.drawStatic
  def drawStatic(self, theGroc, newX, newY):
    assert not None in (newX, newY), 'Cannot render coordinates of None'
    self.drawMoving(theGroc, newX, newY, newX, newY)

#render.close
  def close(self):
    print("Awaiting user input to close")
    while (self.running):
      self.tick()
    self.quit()

#render.maybeDraw
  def maybeDraw(self, theGroc, newX, newY):
    if 0 < self.world.lightLevel < 1:
      self.drawStatic(theGroc, newX, newY)
    else:
      pass
      'theoretically not needed when light levels are steady'
      self.drawStatic(theGroc, newX, newY)
      
#render.quit
  def quit(self):
    pygame.quit()

#render.soundEat
  def soundEat(self):
    if self.world.mute:
      pass
    elif (self.lastSoundTick + 
        round(2*self.world.percentage())) < self.world.currentTick:
      self.eat.play()
      self.lastSoundTick = self.world.currentTick

#render.soundFood
  def soundFood(self):
    if self.world.mute:
      pass 
    else:
      self.food.play()

#render.tick
  def tick(self):
    pygame.display.set_caption(str(self.world.population) + " Grocs")
    text = self.font.render('Air: ' + 
               '{:>3}'.format(str(int(self.world.airTemperature*100))) + 
               ' Ground: ' + 
               '{:>3}'.format(str(int(self.world.groundTemperature*100))), 
               True, self.world.GREEN, self.worldColor)
    self.screen.blit(text, self.textRect)     
    pygame.display.flip()
    oldColor = self.worldColor
    self.worldColor = self.world.getWorldColor()
    if oldColor == self.worldColor:
      self.screen.fill(self.worldColor)
    else:
      self.screen.fill(self.worldColor)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.quit()
        self.running = False
      if event.type == pygame.MOUSEBUTTONDOWN:
        x, y = event.pos
        nearestGroc = self.world.findGrocNearXY(x, y) 
        nearestFood = self.world.findFoodNearXY(x, y)
        gdist = self.world.findDistanceXY(x, y, 
                                        nearestGroc.x, nearestGroc.y)
        fdist = self.world.findDistanceXY(x, y, 
                                        nearestFood.x, nearestFood.y)
        if gdist > nearestGroc.getPersonalRadius():
          pass
        else:
          nearestGroc.touch()
          print(nearestGroc.identify())
        if fdist > 30:
          pass
        else:
          print(nearestFood.identify())
 
