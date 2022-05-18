#!/usr/bin/python3
#
# render.py
#
#   receive messages from world.py containing instructions
#   on groc movement.  Uses pygame. (Other versions may use other
#   rendering mechanisms) 
#
# TDORSEY 2022-04-28  Created
# TDORSEY 2022-05-01  Renamed to render.py
# TDORSEY 2022-05-02  Move pipe definitions to World class
# TDORSEY 2022-05-04  Additional fields in renderPipe message
#                     Support gender-determined coloration
# TDORSEY 2022-05-05  Blank Line fix
# TDORSEY 2022-05-07  pydoc-enabled, import enabled
# TDORSEY 2022-05-15  visible moods
# TDORSEY 2022-05-15  pipe receives MOVE and STAT messages

import pygame 
import os
import groc

def main():
  pipe = groc.World.PIPENAME
  try:
    print("Looking for the pipe")
    rpipe = open(pipe, "r")
  except Exception as e:
    print(e)
    print("Start run.py first")
    exit()

  print ("Opened pipe")
  pygame.init
  screen = pygame.display.set_mode([1800, 800])
  worldcolor = groc.World.WHITE
  screen.fill(worldcolor)
  line = ""
  msgcount = 0
  running = True
  reading = True
  while (running):
    if (reading):
      msg = rpipe.read(1)
      if msg == groc.World.NEWLINE:
        movemsg = line.split(groc.World.FIELDSEP)
        x = len(movemsg) 
        messageType = movemsg[0] 
        msgcount += 1
        if messageType == "MOVE":
          grocId = movemsg[1]
          oldX = int(movemsg[2]) 
          oldY = int(movemsg[3])
          newX = int(movemsg[4])
          newY = int(movemsg[5])
          gender = movemsg[6]
          mood = movemsg[7]
          if gender == groc.Groc.MALE:
            groccolor = groc.World.BLUE
          else:
            groccolor = groc.World.RED
          if mood == groc.Groc.LONELY:
            eyecolor = groc.World.WHITE
          elif mood == groc.Groc.CROWDED:
            eyecolor = groc.World.BLACK
          else:
            # mood == groc.Groc.HAPPY:
            eyecolor = groccolor
          if oldX == newX and oldY == newY:
            'has not moved'
            pass
          else:
            pygame.draw.circle(screen, worldcolor, (oldX, oldY), 10)
          pygame.draw.circle(screen, groccolor, (newX, newY), 9)
          pygame.draw.circle(screen, eyecolor, (newX, newY), 2)
          pygame.display.flip()
          line = ""
        elif messageType == "STAT":
          currentTick = int(movemsg[1])
          happyCount = int(movemsg[2]) 
          lonelyCount =  int(movemsg[3])
          crowdedCount = int(movemsg[4])
          line = ""
          print(messageType, currentTick, 
                happyCount, lonelyCount, crowdedCount) 
        else:
          print("unrecognized message type: ", messageType)
      else:
        line = line + msg
      if len(msg) != 1:
        print("Sender Terminated")
        print("Messages received: ", msgcount)
        reading = False
        rpipe.close()
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        running = False
      if event.type == pygame.MOUSEBUTTONDOWN:
        x, y = event.pos
        print("Clicked at " + str(x) + "," + str(y))
  

if __name__ == '__main__':
  main()
