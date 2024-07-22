from direct.showbase.DirectObject import DirectObject
import random, copy
from doomsday.cog.PowerTie import PowerTie

class CogAttacks(DirectObject):
    attacks = [PowerTie()]
    
    def getRandomAttack(self, dmg):
        attack = copy.copy(random.choice(self.attacks))
        attack.setDamage(dmg)
        attack.generate()
        return attack
        