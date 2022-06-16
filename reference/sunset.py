#!/usr/bin/python3
import pygame
import groc
import math
import world
import time

def interpolateScalar(v1, v2, scale):
  return (scale*v2) + (1-scale)*v1

def interpolateColor(color1, color2, scale):
  result = [None,None,None]
  for i in range(3):
    result[i] = interpolateScalar(color1[i], color2[i], scale)
  return tuple(result)
  


def main():
  pygame.init()
  pygame.font.init()
  gauge = pygame.display.set_mode([1800, 800])
  gaugeColor = world.World.BLACK
  green = (0, 255, 0)
  blue = (0,0,255)
  paleblue = (0,0,128)
  black = (0,0,0)
  red = (128,0,0)
  deepred = (255,0,0)
  white = (255,255,255)
  gray = (159,159,159)
  #colorList = [black, red, blue, white]
  colorList = [black, paleblue, white]
  gauge.fill(gaugeColor)
  segments = len(colorList)-1 
  chunk = 100/segments
  print("segments", segments, "chunk", chunk)
  x,y = 400,400
  font = pygame.font.Font('/usr/share/fonts/truetype/ubuntu/UbuntuMono-R.ttf', 32)
  text = font.render('Light Level', True, green, blue)
  textRect = text.get_rect()
  textRect.center = (x//2, y//2)
 
  for i in range(100):
    foo = math.trunc(i//chunk)
    grad = (i % chunk)/chunk
    print("i", i, "foo", foo, "grad", grad)
    color = interpolateColor(colorList[foo], colorList[foo+1], grad)
    print("color", color)
    gauge.fill(color)
    pygame.draw.circle(gauge, red, (300, 300), 7)
    pygame.draw.circle(gauge, deepred, (30, 30), 7)
    pygame.draw.circle(gauge, blue, (600, 600), 7)
    pygame.draw.circle(gauge, paleblue, (900, 600), 7)
    text = font.render('Light Level: ' + str(i/100), True, green, blue)
    gauge.blit(text, textRect)
    pygame.display.flip()
    time.sleep(1)
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
