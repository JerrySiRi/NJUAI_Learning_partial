from doomsday.cog.CogAttack import CogAttack

class PowerTie(CogAttack):
    
    def __init__(self):
        CogAttack.__init__(self, self, 'phase_5/models/props/power-tie.bam', attackType = 'throw', hitSound = 'power_tie_impact', throwSound = 'power_tie_throw')
        self.damage = 5
        
    def setDamage(self, dmg):
        self.damage = dmg
        
    def getDamage(self):
        return self.damage