import pygame
import groc
def main():
  pygame.init
  gauge = pygame.display.set_mode([1100, 800])
  gaugeColor = groc.World.WHITE
  happyColor = groc.World.BLUE
  lonelyColor = groc.World.RED
  crowdedColor = groc.World.BLACK
  totalGrocs = 500
  happyStat = totalGrocs
  lonelyStat = 0 
  crowdedStat = 0
  gauge.fill(gaugeColor)
  for i in range(500):
    happyStat = totalGrocs - lonelyStat - crowdedStat
    if i < 250:
      lonelyStat = lonelyStat + i
    else:
      crowdedStat = crowdedStat + i 
    pygame.draw.circle(gauge, happyColor, (i, happyStat), 9) 
    pygame.draw.circle(gauge, lonelyColor, (i, lonelyStat), 9) 
    pygame.draw.circle(gauge, crowdedColor, (i, crowdedStat), 9) 
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
