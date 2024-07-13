from direct.showbase.DirectObject import DirectObject
from doomsday.round.Wave import Wave
import random

class Waves(DirectObject):
    
    def __init__(self):
        pass
    
    def generateWave(self, skeletonsAllowed = False, waitersAllowed = False, levelCurve = [1, 12], cogAmountCurve = [2, 30]):
        cogAmount = random.randint(cogAmountCurve[0], cogAmountCurve[1])
        skeletons = False
        waiters = False
        if skeletonsAllowed:
            skeletons = random.choice([True, False])
        if waitersAllowed:
            waiters = random.choice([True, False])
        wave = Wave(levelCurve = levelCurve, cogAmount = cogAmount)
        wave.setSkeletonsAllowed(skeletons)
        wave.setWaitersAllowed(waiters)
        return wave