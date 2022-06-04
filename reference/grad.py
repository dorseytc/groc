import pygame
import groc

def interpolateScalar(v1, v2, scale):
  return (scale*v2) + (1-scale)*v1

def interpolateColor(color1, color2, scale):
  result = [None,None,None]
  for i in range(3):
    result[i] = interpolateScalar(color1[i], color2[i], scale)
  return tuple(result)
  


def main():
  pygame.init
  gauge = pygame.display.set_mode([1800, 800])
  #gaugeColor = groc.World.WHITE
  gaugeColor = groc.World.BLACK
  blue = (0,0,255)
  black = (0,0,0)
  red = (128,0,0)
  white = (255,255,255)
  gray = (159,159,159)
  colorList = [blue, black, red, white, gray]
  
  gauge.fill(gaugeColor)
  
  for i in range(101):
    for j in range(len(colorList)):
      for k in range(len(colorList)):
        if j == k:
          pass
        else:
          color = interpolateColor(colorList[j], colorList[k], i/100)
          rowindex = j*len(colorList) + k
          coord = ((i+1)*15,rowindex*30)
          pygame.draw.circle(gauge, black, coord, 8)
          pygame.draw.circle(gauge, color, coord, 7)
    pygame.display.flip()
  running = True
  while running:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        running = False

  print ("Done")


if __name__ == '__main__':
   main()
