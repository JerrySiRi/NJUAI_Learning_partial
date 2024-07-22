from direct.showbase.DirectObject import DirectObject
from doomsday.base import SoundBank

class ItemEntity(DirectObject):
    
    def __init__(self, cls, addCollision = True):
        self.cls = cls
        self.addCollision = addCollision
        self.setupDrop()
        
    def setupDrop(self):
        self.cls.getEntity().setPythonTag('Drop', self.cls)
        if(self.addCollision):
            wc = render.getPythonTag('WorldCollisions')
            wc.addDropCollision(self.cls.getEntity())
            
    def execute(self):
        ent = self.cls.getEntity()
        if not ent.isEmpty():
            SoundBank.getSound('drop_pickup').play()
            if(ent.getName() == "ent_jellybean"):
                jbAmt = ent.getPythonTag("Amount")
                toon = render.find('**/Toon').getPythonTag('Avatar')
                toon.setJellybeans(toon.getJellybeans() + jbAmt)
            elif(ent.getName() == "ent_clothes"):
                pass
            ent.removeNode()
        else:
            return