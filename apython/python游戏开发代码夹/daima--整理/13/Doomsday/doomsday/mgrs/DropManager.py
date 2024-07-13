from direct.showbase.DirectObject import DirectObject
from doomsday.world.JellybeanReward import JellybeanReward
import random

class DropManager(DirectObject):
    
    def generateRandomDrop(self):
        #choice = random.randint(0, 1)
        reward = JellybeanReward(random.randint(5, 30))
        return reward.getEntity()
        