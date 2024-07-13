from direct.showbase.DirectObject import DirectObject
from direct.interval.IntervalGlobal import Sequence, Wait, Func
from doomsday.round.Wave import Wave
from doomsday.round.Waves import Waves
from doomsday.base import SoundBank
import random

#wave1 = Wave(levelCurve = [8, 12], cogAmount = 16)
#wave1.setInvasion(cogName = "The Big Cheese", isWaiter = True)
#wave1 = Wave(levelCurve = [1, 3], cogAmount = 16)


waves = Waves()
wave1 = waves.generateWave(skeletonsAllowed = False, waitersAllowed = False, levelCurve = [1, 3], cogAmountCurve = [12, 24])
wave2 = waves.generateWave(skeletonsAllowed = False, waitersAllowed = False, levelCurve = [2, 3], cogAmountCurve = [14, 30])
wave3 = waves.generateWave(skeletonsAllowed = False, waitersAllowed = False, levelCurve = [2, 6], cogAmountCurve = [8, 18])
wave4 = waves.generateWave(skeletonsAllowed = True, waitersAllowed = False, levelCurve = [4, 8], cogAmountCurve = [16, 28])
wave5 = waves.generateWave(skeletonsAllowed = True, waitersAllowed = True, levelCurve = [6, 9], cogAmountCurve = [6, 12])
wave6 = waves.generateWave(skeletonsAllowed = False, waitersAllowed = True, levelCurve = [9, 12], cogAmountCurve = [8, 20])
wave7 = waves.generateWave(skeletonsAllowed = False, waitersAllowed = False, levelCurve = [10, 12], cogAmountCurve = [20, 24])

"""
wave1 = Wave(levelCurve = [1, 3], cogAmount = 15)
wave1.setSkeletonsAllowed(False)
wave1.setSupport(name = "The Mingler", levelRange = [7, 11])

wave2 = Wave(levelCurve = [2, 5], cogAmount = 30)
wave2.setSkeletonsAllowed(True)

wave3 = Wave(levelCurve = [4, 7], cogAmount = 45)
wave3.setSkeletonsAllowed(True)

wave4 = Wave(levelCurve = [6, 11], cogAmount = 25)
wave4.setSkeletonsAllowed(True)

wave5 = Wave(levelCurve = [8, 12], cogAmount = 35)
wave5.setWaitersAllowed(True)
wave5.setSkeletonsAllowed(True)

wave6 = Wave(levelCurve = [10, 12], cogAmount = 20)
wave6.setWaitersAllowed(True)
wave6.setSkeletonsAllowed(True)


#wave1 = Wave(levelCurve = [1, 11], cogAmount = 16)
#wave1.setInvasion(cogName = 'The Mingler')
#wave1.setSkeletonsAllowed(True)

wave2 = Wave(levelCurve = [8, 12], cogAmount = 16)
wave2.setInvasion(cogName = "Mr. Hollywood")#Wave(levelCurve = [3, 5], cogAmount = 12)

wave3 = Wave(levelCurve = [8, 12], cogAmount = 16)
wave3.setInvasion(cogName = "Robber Baron")#Wave(levelCurve = [6, 8], cogAmount = 8)
"""

class Round(DirectObject):
    
    currentWave = -1
    bgms = ['bgm_doom', 'bgm_install', 'bgm_ceo', 'bgm_orchestra', 'bgm_bldg']
    
    def __init__(self):
        self.waves = [wave1, wave2, wave3, wave4, wave5, wave6, wave7]
        self.bgm = None
        
    def startWave(self):
        if(self.bgm != None):
            self.bgm.stop()
        if(self.currentWave == -1):
            wave = 0
            render.find('**/TTC').getPythonTag('Class').doFade()
        else:
            if((self.currentWave + 1) != len(self.waves)):
                wave = (self.currentWave + 1)
            else:
                wave = 0
        self.currentWave = wave
        waveObj = self.waves[wave]
        if(wave == 0):
            Sequence(
              Wait(3.4),
              Func(waveObj.spawnCogs)
            ).start()
        else:
            waveObj.spawnCogs()
        self.bgm = SoundBank.getSound(random.choice(self.bgms))
        self.bgm.setLoop(True)
        self.bgm.play()
        
    def setWaveCompleted(self):
        cogsLeft = render.find('**/Cogs').getChildren()
        for cog in cogsLeft:
            if(cog.hasPythonTag("Support")):
                cog.getPythonTag("Cog").setHealth(0)
        self.bgm.stop()
        if(self.currentWave == len(self.waves) - 1):
            self.currentWave = -1
        self.clearDummyNodes()
        self.startWave()
        
    def clearDummyNodes(self):
        dummyNodes = render.findAllMatches('**/dummy')
        for dummyNode in dummyNodes:
            dummyNode.removeNode()
        
    def getCurrentWave(self):
        return self.waves[self.currentWave]
    
    def getNextWave(self):
        if self.waves[self.currentWave] != len(self.waves) - 1:
            return self.waves[self.currentWave + 1]
        else:
            return None
        
    def getWaves(self):
        return self.waves