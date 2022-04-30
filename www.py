#!/usr/bin/python
#
# www.py
#
# TDORSEY 2022-04-28  Created
#
import pygame, os
pipe = "/tmp/grocpipe"
try:
  print("Looking for the pipe")
  rpipe = open(pipe, "r")
except Exception as e:
  print(e)
  print("Start groc.py first")
  exit()

line = ""
msgcount = 0
print ("Opened pipe")
pygame.init
screen = pygame.display.set_mode([800, 250])
worldcolor = (255, 255, 255)
groccolor = (0, 0, 255)
screen.fill(worldcolor)
while True:
  msg = rpipe.read(1)
  if msg == '\n':
    movemsg = line.split(",")
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

