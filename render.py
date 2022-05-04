#!/usr/bin/python
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
#                     

import pygame 
import os
import groc

pipe = groc.World.PIPENAME
try:
  print("Looking for the pipe")
  rpipe = open(pipe, "r")
except Exception as e:
  print(e)
  print("Start run.py first")
  exit()

line = ""
msgcount = 0
print ("Opened pipe")
pygame.init
screen = pygame.display.set_mode([1800, 800])
worldcolor = groc.World.WHITE
groccolor = groc.World.BLUE
screen.fill(worldcolor)
while True:
  msg = rpipe.read(1)
  if msg == groc.World.NEWLINE:
    movemsg = line.split(groc.World.FIELDSEP)
    grocId = movemsg[0]
    oldX = int(movemsg[1]) 
    oldY = int(movemsg[2])
    newX = int(movemsg[3])
    newY = int(movemsg[4])
    print (grocId, oldX, oldY, newX, newY)
    msgcount += 1
    pygame.draw.circle(screen, worldcolor, (oldX, oldY), 10)
    pygame.draw.circle(screen, groccolor, (newX, newY), 9)
    pygame.display.flip()
    line = ""
  else:
    line = line + msg
  if len(msg) != 1:
    print("Sender Terminated")
    break
print("Messages received: ", msgcount)
running = True
rpipe.close()
while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      running = False

