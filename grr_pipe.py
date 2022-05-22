#!/usr/bin/python3
#
# grr_pipe.py
#
# grr_pipe means
#
#  Groc Renderer via Pipe
#
# This class encapsulates all the interactions the world has 
# with the renderer.  That is to say, the world exists outside of
# how it is visualized.  This class encapsulates all logic related
# to the visualization of the world
#
# TDORSEY 2022-05-22 Created from the remnants of pipe logic in the
#                    original groc.py and render.py

import os
import groc


class Renderer():
  '''This class encapsulates all logic related to the visualization 
  of the world'''
  
  FIELDSEP = '|'
  NEWLINE = '\n'
  PIPENAME = "/tmp/grocpipe"

  def __init__(self, thisWorld):  
    
    super(Renderer, self).__init__()
    print("This Renderer requires a pipe reader")
    print("Please start a pipe reader now")
    self.theWorld = thisWorld
    if os.path.exists(self.PIPENAME):
      os.unlink(self.PIPENAME)
    if not os.path.exists(self.PIPENAME):
      os.mkfifo(self.PIPENAME, 0o600)
      self.renderPipe = open(self.PIPENAME, 'w', 
                                 newline=self.NEWLINE)

  def close(self):
    '''the main loop calls close once when the main loop has exited.
    close calls quit'''
    # cleanly close the pipe
    self.renderPipe.close()
    # destroy the pipe
    self.quit()

  def drawMoving(self, theGroc, oldX, oldY, newX, newY):
    '''this method gets called once for each groc that moves'''
    fs = self.FIELDSEP
    nl = self.NEWLINE
    self.renderPipe.write("MOVE" + fs + str(theGroc.id) + fs + 
                          str(oldX) + fs + str(oldY) + fs + 
                          str(newX) + fs + str(newY) + fs + 
                          theGroc.gender + fs + theGroc.mood + nl)
    self.renderPipe.flush()

  def drawStatic(self, theGroc, newX, newY):
    '''this gets called each time a groc must be rendered without moving;
     for example, his mood changes'''
    self.drawMoving(theGroc, newX, newY, newX, newY)

  def tick(self): 
    '''the main procedure calls tick once after all grocs are iterated;
     once per round'''
    fs = self.FIELDSEP
    nl = self.NEWLINE
    self.renderPipe.write("STAT" + fs + 
                          str(self.theWorld.currentTick) + fs + 
                          str(self.theWorld.happy) + fs + 
                          str(self.theWorld.lonely) + fs + 
                          str(self.theWorld.crowded) + nl)
    self.renderPipe.flush()


  def quit(self): 
    '''the close method calls quit AFTER all user activity is complete.
    In a graphic renderer, this would be after the USER dismisses 
    the render window.'''
    # destroy the pipe
    if os.path.exists(self.PIPENAME):
      os.unlink(self.PIPENAME) 
