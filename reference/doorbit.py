# groc.findOrbitalLeader
    def findOrbitalLeader(self, anchor):
      leader = None
      for anotherGroc in self.world.grocList:
        if (anotherGroc.id == self.id):
          pass
        elif (anotherGroc.orbitAnchor == anchor):
          if (anotherGroc.orbiterNumber == self.orbiterNumber - 1):
            leader = anotherGroc
            break
      return leader
 
# groc.doOrbit
    def doOrbit(self, anchor, radius, points=100):
      assert None not in (anchor, radius, points), "invalid parms"
      def getHeadway():
        countOfOrbiters = self.countGrocsInOrbit(anchor) + 1
        return round(points/countOfOrbiters)
      def getNthStation(currentStation, n):
        return (currentStation + n) % points
      def findOrbitalLeader(self, anchor):
        leader = None
        for anotherGroc in self.world.grocList:
          if (anotherGroc.id == self.id):
            pass
          elif (anotherGroc.orbitAnchor == anchor):
            if (anotherGroc.orbiterNumber == self.orbiterNumber - 1):
              leader = anotherGroc
              break
        return leader
      def hasHeadway(headway):
        if self.orbitalLeader == None:
          result = True
        elif (getNthStation(self.orbitalIndex, headway) == 
              self.orbitalLeader.orbitalIndex):
          result = True
        elif (getNthStation(self.orbitalIndex, headway+1) == 
              self.orbitalLeader.orbitalIndex):
          result = True
        else:
          result = False
        return result
      if not (self.orbitAnchor == anchor):
        self.orbiterNumber = self.countGrocsInOrbit(anchor) 
        self.orbitAnchor = anchor
        self.orbitalIndex = 0
        self.orbitalPoints = self.world.pointsOnACircle(radius, points)
      if self.orbiterNumber > 0:
        self.orbitalLeader = findOrbitalLeader(anchor)
      else:
        self.orbitalLeader = None
      newX, newY = self.orbitalPoints[self.orbitalIndex]
      headway = getHeadway()
      self.setTarget((round(newX) + anchor.x), 
                     (round(newY) + anchor.y),
                     "Orbital index "  + str(self.orbitalIndex) + 
                     " Headway " + str(headway))
      if self.x == self.targetX and self.y == self.targetY:
        if not hasHeadway(headway):
          pass
        else:
          self.orbitalIndex = getNthStation(self.orbitalIndex, 1)
          newX, newY = self.orbitalPoints[self.orbitalIndex]
          self.setTarget(round(newX) + anchor.x, round(newY) + anchor.y,
                     "Orbital index "  + str(self.orbitalIndex))
      #self.moveTowardTarget()
