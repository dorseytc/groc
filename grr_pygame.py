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
# TDORSEY 2022-06-16  Format temperature and time gauge at top left
# TDORSEY 2022-06-18  Toggle groc halo for emphasis
# TDORSEY 2022-06-20  Sleeping animations
# TDORSEY 2022-06-21  Eating animations

import pygame 


class Renderer():
  pygame.init()
  pygame.font.init()
  pygame.display.set_caption("Grocs")

  def __init__(self, thisWorld):

    super(Renderer, self).__init__()

    print("Renderer is grr_pygame 1.0")
    self.world = thisWorld
    self.running = True
    # screen stuff
    self.screen = pygame.display.set_mode([thisWorld.MAXX, 
                                          thisWorld.MAXY])
    self.worldColor = self.world.WHITE
    self.highlightedGroc = None
    self.screen.fill(self.worldColor)
    self.screenshot = True
    # font stuff
    self.fontname = '/usr/share/fonts/truetype/ubuntu/UbuntuMono-R.ttf'
    self.largeFont = pygame.font.Font(self.fontname, 20)
    self.temps = self.largeFont.render(format('Temp: ', '<25'), True, 
                                 self.world.GREEN, self.world.BLACK)
    self.tempsRect = self.temps.get_rect()
    self.tempsRect.topleft = (5,5)
    self.times = self.largeFont.render(format('Current Time:', '<25'), 
                                 True, self.world.GREEN, self.world.BLACK)
    self.timesRect = self.times.get_rect()
    self.timesRect.topleft = (5, 25)
    self.smallFont = pygame.font.Font(self.fontname, 14)
    # sound stuff
    pygame.mixer.init()
    self.eat=pygame.mixer.Sound('eat.ogg')
    self.food=pygame.mixer.Sound('food.ogg')
    self.lastSoundTick = self.world.currentTick

#render.drawDeath
  def drawDeath(self, theDead): 
    self.screenshot = True
 
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
     
#render.drawGauge
  def drawGauge(self):
    'time and temperature gauge'
    tempstr = ('Air: ' + 
      '{:>3}'.format(str(int(self.world.airTemperature*100))) + 
      self.world.DEGREESIGN + ' Ground: ' + 
      '{:>3}'.format(str(int(self.world.groundTemperature*100))) + 
      self.world.DEGREESIGN)
    timestr = ('Current Time: ' + str(self.world.currentGrocTime()))
    gaugeWidth = '<' + str(max(len(tempstr), len(timestr)))
    self.temps = self.largeFont.render(format(tempstr, gaugeWidth), 
                   True, self.world.GREEN, self.world.BLACK)
    self.screen.blit(self.temps, self.tempsRect)     
    self.times = self.largeFont.render(format(timestr, gaugeWidth), 
                   True, self.world.GREEN, self.world.BLACK)
    self.screen.blit(self.times, self.timesRect)

#render.drawGrocMoving
  def drawGrocMoving(self, theGroc, oldX, oldY, newX, newY):
    assert not None in (oldX, oldY, newX, newY), 'Cannot move to x,y None'
    if theGroc.gender == theGroc.MALE:
      groccolor = self.world.BLUE
    else:
      groccolor = self.world.RED
    distanceFromTarget = self.world.ifNone(
      self.world.findDistanceXY(theGroc.x, theGroc.y, 
                                theGroc.targetX, theGroc.targetY), 0)
    hunger = theGroc.hungerThreshold - theGroc.fp 
    if theGroc.mood == theGroc.DEAD:
      eyecolor = groccolor
      eyeshape = "circle"
      groccolor = self.world.BLACK
      intensity = 2
    elif theGroc.mood == theGroc.COLD:
      eyecolor = self.world.GRAY
      eyeshape = "square"
      intensity = 6
    elif theGroc.mood == theGroc.LONELY:
      eyecolor = self.world.WHITE
      eyeshape = "circle"
      intensity = 2 + round(distanceFromTarget / 
                      self.world.maxDistance * 6)
    elif theGroc.mood == theGroc.CROWDED:
      eyecolor = self.world.BLACK
      eyeshape = "circle"
      intensity = 2 + round(distanceFromTarget / 
                      self.world.maxDistance * 6)
    elif theGroc.mood == theGroc.HUNGRY:
      eyecolor = self.world.GRAY
      eyeshape = "circle"
      intensity = 2 + round(hunger / theGroc.hungerThreshold * 6)
    elif theGroc.mood == theGroc.EATING:
      eyecolor = self.worldColor
      eyeshape = "circle"
      intensity = 2
    elif theGroc.mood == theGroc.SLEEPING:
      eyecolor = self.worldColor
      eyeshape = "circle"
      intensity = 2
    else:
      eyecolor = groccolor
      eyeshape = "circle"
      intensity = 2 
    if oldX == newX and oldY == newY:
      isMoving = False
    else:
      pygame.draw.circle(self.screen, self.worldColor, (oldX, oldY), 11)
      isMoving = True

    if self.highlightedGroc == theGroc:
      if self.world.lightLevel < .5: 
        halocolor = self.world.YELLOW
      else:
        halocolor = self.world.GREEN
      pygame.draw.circle(self.screen, halocolor, (newX, newY), 10)
    pygame.draw.circle(self.screen, groccolor, (newX, newY),9)
    if theGroc.mood == theGroc.SLEEPING:
      frame = ((theGroc.id + 
                self.world.currentTick - theGroc.moodSince) % 100) 
      intensity = 3 + (abs(60 - frame)/50*3)
      mouthCenter = (9 - (intensity/2)) * theGroc.faceTowards
      pygame.draw.circle(self.screen, eyecolor,
                           (newX + mouthCenter , newY), intensity)
    elif theGroc.mood == theGroc.EATING:
      cycle = 10
      frame = ((theGroc.id + 
                self.world.currentTick - theGroc.moodSince) % cycle)
      intensity = 2 + (abs((cycle/2) - frame)/cycle*6)
      mouthCenter = (9 - (intensity/2)) * theGroc.faceTowards
      pygame.draw.circle(self.screen, eyecolor,
                           (newX + mouthCenter , newY), intensity)
    elif eyeshape == "circle":
        pygame.draw.circle(self.screen, eyecolor, (newX, newY), intensity)
    else:
      pygame.draw.rect(self.screen, eyecolor, 
                       pygame.Rect(newX - (intensity//2), 
                                   newY - (intensity//2), 
                                   intensity, intensity))
    if self.highlightedGroc == theGroc:
      pygame.draw.line(self.screen, halocolor, (newX - 6, newY + 4), 
                       (newX + 6, newY + 4))
    if None == self.highlightedGroc:
      pass
    elif None in (self.highlightedGroc.targetX, 
                  self.highlightedGroc.targetY):
      pass
    else:
      intensity = (20 - (self.world.currentTick % 20)) 
      targetColor = self.world.interpolateColor(
                               self.world.RED, 
                               self.worldColor, 
                               intensity/20)
      pygame.draw.rect(self.screen, self.world.YELLOW, 
        pygame.Rect(self.highlightedGroc.targetX - (intensity+1),
                    self.highlightedGroc.targetY - (intensity+1),
                    2*(1+intensity), 2*(1*intensity)))
      pygame.draw.rect(self.screen, targetColor,
        pygame.Rect(self.highlightedGroc.targetX - (intensity),
                    self.highlightedGroc.targetY - (intensity),
                    2*intensity, 2*intensity))


#render.drawGrocStatic
  def drawGrocStatic(self, theGroc, newX, newY):
    assert not None in (newX, newY), 'Cannot render x,y of None'
    self.drawGrocMoving(theGroc, newX, newY, newX, newY)

#render.close
  def close(self):
    print("Ready to close")
    while (self.running):
      self.tick()
    self.quit()

#render.highlightGroc
  def highlightGroc(self, theGroc):
    if theGroc == None:
      pass 
    else:
      self.highlightedGroc = theGroc
      grocDetails = theGroc.identify().split('\n')
      length = max(len(max(grocDetails, key=len)),35)
      height = 14
      if theGroc.x < 300 and theGroc.y < ((height * len(grocDetails)) + 47):
        top = 5
        left = self.world.MAXX - 250
      else:
        top = 47
        left = 5
      for i in range(len(grocDetails)):
        line = self.smallFont.render(
                                  grocDetails[i].ljust(length), True, 
                                  self.world.GREEN, 
                                  self.world.BLACK)
        lineRect = line.get_rect() 
        lineRect.topleft = (left, top + (height*i))
        self.screen.blit(line, lineRect)     

#render.maybeDraw
  def maybeDraw(self, theGroc, newX, newY):
    if 0 < self.world.lightLevel < 1:
      self.drawGrocStatic(theGroc, newX, newY)
    else:
      pass
      'theoretically not needed when light levels are steady'
      self.drawGrocStatic(theGroc, newX, newY)

#render.maybeScreenshot
  def maybeScreenshot(self):
    if self.screenshot:
      pygame.image.save(self.screen, 
                      "./images/dead_" + 
                      str(self.world.currentTick) + 
                      ".png")
      self.screenshot = False

      
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
    self.drawGauge() 
    self.highlightGroc(self.highlightedGroc)     
    pygame.display.flip()
    oldColor = self.worldColor
    self.worldColor = self.world.getWorldColor()
    self.maybeScreenshot()
    if oldColor == self.worldColor:
      self.screen.fill(self.worldColor)
    else:
      self.screen.fill(self.worldColor)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.quit()
        self.running = False
        print("User clicked 'QUIT'")
      if event.type == pygame.MOUSEBUTTONDOWN:
        x, y = event.pos
        nearestGroc = self.world.findGrocNearXY(x, y) 
        nearestFood = self.world.findFoodNearXY(x, y)
        gdist = self.world.findDistanceXY(x, y, 
                                        nearestGroc.x, nearestGroc.y)
        fdist = self.world.findDistanceXY(x, y, 
                                        nearestFood.x, nearestFood.y)
        if gdist > nearestGroc.getPersonalSpace():
          self.highlightedGroc = None
        elif nearestGroc == self.highlightedGroc:
          self.highlightedGroc = None
        else:   
          self.highlightedGroc = nearestGroc
          print(nearestGroc.identify())
        if fdist > 30:
          pass
        else:
          print(nearestFood.identify())
 


    
