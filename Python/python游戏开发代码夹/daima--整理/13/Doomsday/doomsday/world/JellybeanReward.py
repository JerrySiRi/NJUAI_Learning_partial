from doomsday.world.ItemEntity import ItemEntity
from doomsday.avatar.AvatarAttributes import AvatarAttributes
from doomsday.base import Globals
import random

class JellybeanReward(ItemEntity):
    
    def __init__(self, amount):
        self.amount = amount
        self.generate()
        
    def generate(self):
        if(self.amount >= Globals.LARGE_BEAN_AMT):
            mdl = 'phase_5.5/models/estate/jellybeanJar.bam'
        else:
            mdl = 'phase_4/models/props/jellybean4.bam'
        self.entity = loader.loadModel(mdl)
        if(self.amount < Globals.LARGE_BEAN_AMT):
            self.entity.setColor(random.choice(AvatarAttributes().convertColorDictToTbl()))
            self.entity.setScale(3)
        self.entity.setName('ent_jellybean')
        self.entity.setPythonTag('Amount', self.amount)
        ItemEntity.__init__(self, self, addCollision = True)
    
    def getEntity(self):
        return self.entity