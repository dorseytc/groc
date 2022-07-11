#!/usr/bin/python3
import pygame
import groc
import math
import world
import time

def main():
  pygame.init()
  gauge = pygame.display.set_mode([1800, 800])
  gaugeColor = world.World.WHITE
  gauge.fill(gaugeColor)
  sunColor = world.World.YELLOW
  for i in range(2000):
    if i < 1000:
      height = (i/1000)*30
    else:
      height = ((2000-i)/1000)*30
    print("height", height)
    gauge.fill(gaugeColor)
    pygame.draw.circle(gauge, world.World.BLACK, (250, 300), 11)
    pygame.draw.circle(gauge, sunColor, (250, 300), 10)
    pygame.draw.circle(gauge, world.World.BLACK,  (300, 300 + height), 11)
    pygame.draw.circle(gauge, sunColor,  (300, 300 + height), 10)
    pygame.draw.rect(gauge, world.World.BLACK, pygame.Rect(200, 318, 200, 30 ))
    pygame.display.flip()
    #time.sleep(1)
    running = True
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        running = False
      elif event.type == pygame.MOUSEBUTTONDOWN: 
        x,y = event.pos
        if y < 60:
          y = y + 30
        else:
          y = y - 30 
        if x < textRect.center[0]:
          x = x + 30
        else:
          x = x - 30
        textRect.center = (x, y)

  print ("Done")


if __name__ == '__main__':
   main()
