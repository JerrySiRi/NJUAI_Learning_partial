from direct.showbase.DirectObject import DirectObject
from panda3d.core import VBase3
from doomsday.round.Spawn import Spawn, Path, Checkpoint
from doomsday.cog.Cogs import Cogs
from doomsday.cog.CogAI import CogAI
import random, copy

spawn1 = Spawn(pos = VBase3(-143.27, 3.51, 0.53), hpr = VBase3(268.63, 0, 0))
path1 = Path()
path1.setCheckpoints([
  Checkpoint(VBase3(5.10, 3.36, 4.03)),
  Checkpoint(VBase3(-71.93, 3.67, -1.97)),
  Checkpoint(VBase3(-81.12, -6.09, -3.14)),
  Checkpoint(VBase3(-111.17, -4.9, -0.9))
])
spawn1.setPath(path1)

spawn2 = Spawn(pos = VBase3(-120.86, -62.32, 0.53), hpr = VBase3(298.88, 0, 0))
path2 = Path()
path2.setCheckpoints([
  Checkpoint(VBase3(18.27, -5.33, 4.02)),
  Checkpoint(VBase3(-40.64, -24.57, -1.29)),
  Checkpoint(VBase3(-73.70, -52.55, -2.44))
])
spawn2.setPath(path2)

spawn3 = Spawn(pos = VBase3(-3.75, -98, 3.03), hpr = VBase3(22.45, 0, 0))
path3 = Path()
path3.setCheckpoints([
  Checkpoint(VBase3(41.20, -15.16, 4.02)),
  Checkpoint(VBase3(13.74, -31.82, 4.03))
])
spawn3.setPath(path3)

spawn4 = Spawn(pos = VBase3(-48.82, 88.51, 0.53), hpr = VBase3(219.51, 0, 0))
path4 = Path()
path4.setCheckpoints([
  Checkpoint(VBase3(41.20, -15.16, 4.02)),
  Checkpoint(VBase3(-9.47, 11.58, 0.1))
])
spawn4.setPath(path4)

spawn5 = Spawn(pos = VBase3(-2.10, 104.26, 3.03), hpr = VBase3(162.54, 0, 0))
path5 = Path()
path5.setCheckpoints([
  Checkpoint(VBase3(30.10, -0.22, 4.03)),
  Checkpoint(VBase3(-6.36, 45.55, 0.1))
])
spawn5.setPath(path5)

spawn6 = Spawn(pos = VBase3(31.57, 103.38, 2.53), hpr = VBase3(212.20, 0, 0))
path6 = Path()
path6.setCheckpoints([
  Checkpoint(VBase3(94.54, 0.17, 4.03)),
  Checkpoint(VBase3(58.03, 12.66, 4.03)),
  Checkpoint(VBase3(44.39, 69.24, 4.03)),
  Checkpoint(VBase3(48.08, 70.32, 4.03)),
  Checkpoint(VBase3(64.02, 70.59, 4.03)),
  Checkpoint(VBase3(66.94, 70.18, 4.03)),
  Checkpoint(VBase3(73.35, 81.67, 3.03))
])
spawn6.setPath(path6)

spawn7 = Spawn(pos = VBase3(17.89, -75.58, 2.53), hpr = VBase3(38.78, 0, 0))
path7 = Path()
path7.setCheckpoints([
  Checkpoint(VBase3(40.02, -14.09, 4.03)),
  Checkpoint(VBase3(18.66, -32.33, 4.03)),
  Checkpoint(VBase3(-2.53, -50.42, 0.03))
])
spawn7.setPath(path7)

spawn8 = Spawn(pos = VBase3(-65.83, 58.61, -0.27), hpr = VBase3(325.49, 0, 0))
path8 = Path()
path8.setCheckpoints([
  Checkpoint(VBase3(72.2, 10.66, 4.02)),
  Checkpoint(VBase3(11.12, 11.49, 4.02)),
  Checkpoint(VBase3(-9.20, 23.93, 0.02))
])
spawn8.setPath(path8)

spawn9 = Spawn(pos = VBase3(-103.62, 36.39, -1.32), hpr = VBase3(202.49, 0, 0))
path9 = Path()
path9.setCheckpoints([
  Checkpoint(VBase3(41.50, -10.06, 4.03)),
  Checkpoint(VBase3(-15.08, -0.98, 0.03)),
  Checkpoint(VBase3(-43, 33.69, -1.49)),
  Checkpoint(VBase3(-62.81, 51.94, -1.62)),
  Checkpoint(VBase3(-90.10, 53, -1.31))
])
spawn9.setPath(path9)

spawn10 = Spawn(pos = VBase3(-35.75, -89.60, 0.53), hpr = VBase3(4.79, 0, 0))
path10 = Path()
path10.setCheckpoints([
  Checkpoint(VBase3(88.33, -1.36, 4.03)),
  Checkpoint(VBase3(82.46, -7.92, 4.03)),
  Checkpoint(VBase3(42.45, -11.09, 4.03)),
  Checkpoint(VBase3(20.22, -26, 4.03)),
  Checkpoint(VBase3(-20.9, -64.37, 0.03))
])
spawn10.setPath(path10)

spawns = [spawn1, spawn2, spawn3, spawn4, spawn5, spawn6, spawn7, spawn8, spawn9, spawn10]
Maximum_Cogs_On_Ground = 12
Minimum_Cogs_On_Ground = 5
cogs = Cogs()

class Wave(DirectObject):
    
    cogsDeployed = 0
    cogsDefeated = 0
    cogsPending = 0
    support = {}
    
    def __init__(self, levelCurve, cogAmount, spawnInGroups = False, useSpawns = spawns):
        self.levelCurve = levelCurve
        self.cogAmount = cogAmount
        self.spawnInGroups = spawnInGroups
        self.useSpawns = spawns
        self.invasion = None
        self.cogsPending = self.cogAmount
        self.skeletonsAllowed = False
        self.waitersAllowed = False
        self.skeletonsOnly = False
        self.waitersOnly = False
        
    def spawnCogs(self):
        if(self.cogsPending == 0):
            self.cogsPending = self.cogAmount
            self.cogsDefeated = 0
            self.cogsDeployed = 0
        groundedCogs = self.cogsDeployed - self.cogsDefeated
        spawnRequestSize = 0
        if(groundedCogs == 0):
            if(self.cogsPending >= len(self.useSpawns)):
                spawnRequestSize = (len(self.useSpawns))
            else:
                spawnRequestSize = self.cogsPending
            availableSpawns = copy.copy(self.useSpawns)
            for _ in range(spawnRequestSize):
                spawn = random.choice(availableSpawns)
                availableSpawns.remove(spawn)
                if(self.invasion != None):
                    inv = self.invasion
                    cog = cogs.generateCog(name = inv.getCogName(), skeleton = inv.isSkeleton, waiter = inv.isWaiter)
                    cog.getCog().reparentTo(render.find('**/Cogs'))
                    cog.getCog().setPos(spawn.getPos())
                    cog.getCog().setHpr(spawn.getHpr())
                    CogAI(cog, spawn)
                else:
                    level = random.randint(self.levelCurve[0], self.levelCurve[1])
                    skeleton = False
                    waiter = False
                    if(self.skeletonsAllowed or self.waitersAllowed):
                        if(self.waitersAllowed == True):
                            waiter = random.choice([False, True])
                        elif(self.skeletonsAllowed == True):
                            skeleton = random.choice([False, True])
                        if skeleton:
                            waiter = False
                        elif self.skeletonsOnly:
                            skeleton = True
                            waiter = False
                        if waiter == False:
                            if(self.waitersOnly):
                                waiter = True
                    cog = cogs.generateCog(level = level, skeleton = skeleton, waiter = waiter)
                    cog.getCog().reparentTo(render.find('**/Cogs'))
                    cog.getCog().setPos(spawn.getPos())
                    cog.getCog().setHpr(spawn.getHpr())   
                    CogAI(cog, spawn)
        else:
            if(self.cogsPending > len(self.useSpawns)):
                allowedCogs = Maximum_Cogs_On_Ground - groundedCogs
                spawnRequestSize = random.randint(1, (len(self.useSpawns)))
                if(spawnRequestSize > allowedCogs):
                    spawnRequestSize = allowedCogs
            else:
                allowedCogs = Maximum_Cogs_On_Ground - groundedCogs
                spawnRequestSize = random.randint(1, self.cogsPending)
                if(spawnRequestSize > allowedCogs):
                    spawnRequestSize = allowedCogs
            if(spawnRequestSize == 0):
                return
            availableSpawns = copy.copy(self.useSpawns)
            for _ in range(spawnRequestSize):
                spawn = random.choice(availableSpawns)
                availableSpawns.remove(spawn)
                if(self.invasion != None):
                    inv = self.invasion
                    cog = cogs.generateCog(name = inv.getCogName(), skeleton = inv.isSkeleton, waiter = inv.isWaiter)
                    cog.getCog().reparentTo(render.find('**/Cogs'))
                    cog.getCog().setPos(spawn.getPos())
                    cog.getCog().setHpr(spawn.getHpr())       
                    CogAI(cog, spawn)      
                else:
                    level = random.randint(self.levelCurve[0], self.levelCurve[1])
                    skeleton = False
                    waiter = False
                    if(self.skeletonsAllowed or self.waitersAllowed):
                        if(self.waitersAllowed == True):
                            waiter = random.choice([False, True])
                        elif(self.skeletonsAllowed == True):
                            skeleton = random.choice([False, True])
                        if skeleton:
                            waiter = False
                        elif self.skeletonsOnly:
                            skeleton = True
                            waiter = False
                        if waiter == False:
                            if(self.waitersOnly):
                                waiter = True
                    cog = cogs.generateCog(level = level, skeleton = skeleton, waiter = waiter)
                    cog.getCog().reparentTo(render.find('**/Cogs'))
                    cog.getCog().setPos(spawn.getPos())
                    cog.getCog().setHpr(spawn.getHpr())    
                    CogAI(cog, spawn)
            if(self.support != [] and len(availableSpawns) > 0):
                minLevel = None
                maxLevel = None
                name = None
                dept = None
                supportRequestSize = random.randint(1, len(availableSpawns))
                if('minLevel' in self.support):
                    minLevel = self.support['minLevel']
                    maxLevel = self.support['maxLevel']
                if('name' in self.support):
                    name = self.support['name']
                if('dept' in self.support):
                    dept = self.support['dept']
                for _ in range(supportRequestSize):
                    spawn = random.choice(availableSpawns)
                    availableSpawns.remove(spawn)
                    if(minLevel != None and maxLevel != None):
                        if(minLevel != maxLevel):
                            supCogLvl = random.randint(minLevel, maxLevel)
                        else:
                            supCogLvl = minLevel
                        supCogG = cogs.generateCog(name = name, level = supCogLvl, dept = dept)
                        supCogG.getCog().reparentTo(render.find('**/Cogs'))
                        supCogG.getCog().setPos(spawn.getPos())
                        supCogG.getCog().setHpr(spawn.getHpr())
                        supCogG.getCog().setPythonTag("Support", True)
                        CogAI(supCogG, spawn, support = True)
        self.cogsDeployed += spawnRequestSize
        self.cogsPending -= spawnRequestSize
        
    def setSupport(self, name = None, levelRange = None):
        self.support = {}
        if(name != None):
            self.support['name'] = name
        if(levelRange != None):
            self.support['minLevel'] = levelRange[0]
            self.support['maxLevel'] = levelRange[1]

    def setSkeletonsAllowed(self, flag):
        self.skeletonsAllowed = flag
        
    def areSkeletonsAllowed(self):
        return self.skeletonsAllowed
    
    def setSkeletonsOnly(self):
        self.skeletonsOnly = True
        self.skeletonsAllowed = True
    
    def isSkeletonsOnly(self):
        return self.skeletonsOnly
    
    def setWaitersAllowed(self, flag):
        self.waitersAllowed = flag
        
    def areWaitersAllowed(self):
        return self.waitersAllowed
    
    def setWaitersOnly(self):
        self.waitersOnly = True
        self.waitersAllowed = True
    
    def isWaitersOnly(self):
        return self.waitersOnly
        
    def setInvasion(self, cogName, isSkeleton = False, isWaiter = False):
        self.invasion = Invasion(cogName, isSkeleton, isWaiter)
        if(isWaiter and not isSkeleton):
            self.setWaitersOnly()
        elif(isSkeleton and not isWaiter):
            self.setSkeletonsOnly()
        elif(isWaiter and isSkeleton):
            self.setWaitersAllowed(isWaiter)
            self.setSkeletonsAllowed(isSkeleton)
        
    def getInvasion(self):
        return self.invasion
        
    def setCogsDefeated(self, cogsDefeated):
        self.cogsDefeated = cogsDefeated
        if(self.cogsPending == 0):
            if(self.cogsDefeated == self.cogsDeployed):
                render.getPythonTag('Round').setWaveCompleted()
        else:
            self.spawnCogs()
        
    def getCogsDefeated(self):
        return self.cogsDefeated
    
    def getCogsDeployed(self):
        return self.cogsDeployed
        
class Invasion(DirectObject):
    
    def __init__(self, cogName, isSkeleton = False, isWaiter = False):
        self.cogName = cogName
        self.isSkeleton = isSkeleton
        self.isWaiter = isWaiter
        
    def isSkeleton(self):
        return self.isSkeleton
    
    def isWaiter(self):
        return self.isWaiter
    
    def getCogName(self):
        return self.cogName