#!/usr/bin/python3
#
# grr_text.py
#
# grr_text means
#
#  Groc Renderer via text
#
# This class encapsulates all the interactions the world has 
# with the renderer.  That is to say, the world exists outside of
# how it is visualized.  This class encapsulates all logic related
# to the visualization of the world
#
# TDORSEY 2022-07-29 Created from grr_pipe.py

import os
import groc


class Renderer():
  '''This class encapsulates all logic related to the visualization 
  of the world'''
  
  def __init__(self, thisWorld):  
    
    super(Renderer, self).__init__()
    
    print("Renderer is grr_text 1.0")
    self.theWorld = thisWorld

  def close(self):
    '''the main loop calls close once when the main loop has exited.
    close calls quit'''
    # cleanly close the pipe
    # destroy the pipe
    self.quit()

  def drawFood(self, theFood):
    print("FOOD" + fs + str(theFood.calories) + fs + 
                          str(theFood.x) + fs + str(theFood.y) + nl) 

  def drawGrocMoving(self, theGroc, oldX, oldY, newX, newY):
    '''this method gets called once for each groc that moves'''
    fs = self.FIELDSEP
    nl = self.NEWLINE
    print("MOVE" + fs + str(theGroc.id) + fs + 
                          str(oldX) + fs + str(oldY) + fs + 
                          str(newX) + fs + str(newY) + fs + 
                          theGroc.gender + fs + theGroc.mood + nl)

  def drawGrocStatic(self, theGroc, newX, newY):
    self.drawGrocMoving(theGroc, newX, newY, newX, newY) 

  def maybeDraw(self, theGroc, newX, newY):
    '''this gets called any tick the Groc does not move.  
    May not be necessary to redraw'''
    self.drawGroc(theGroc, None, None, newX, newY)

  def soundEat(self):
    pass

  def soundFood(self):
    pass


  def tick(self): 
    '''the main procedure calls tick once after all grocs are iterated;
     once per round'''
    fs = self.FIELDSEP
    nl = self.NEWLINE
    print("STAT" + fs + 
                          str(self.theWorld.currentTick) + fs + 
                          str(self.theWorld.cold) + fs + 
                          str(self.theWorld.crowded) + fs + 
                          str(self.theWorld.dancing) + fs + 
                          str(self.theWorld.dead) + fs + 
                          str(self.theWorld.eating) + fs + 
                          str(self.theWorld.happy) + fs + 
                          str(self.theWorld.hungry) + fs + 
                          str(self.theWorld.lonely) + fs + 
                          str(self.theWorld.sleeping) + 
                          nl)


  def quit(self): 
    '''the close method calls quit AFTER all user activity is complete.
    In a graphic renderer, this would be after the USER dismisses 
    the render window.'''
    # destroy the pipe
    pass
