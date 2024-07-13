from direct.showbase.DirectObject import DirectObject
from direct.actor.Actor import Actor

class Gag(DirectObject):
    
    def __init__(self, name, cls, model, anim = None, scale = 1):
        self.name = name
        self.cls = cls
        self.model = model
        self.anim = anim
        self.scale = scale
        
    def addCollision(self, gag):
        wrldColl = render.getPythonTag('WorldCollisions')
        wrldColl.addGagCollision(gag)
        
    def generate(self):
        if(self.anim != None):
            gag = Actor(loader.loadModel(self.model), {'chan' : loader.loadModel(self.anim)})
            gag.loop('chan')
        else:
            gag = loader.loadModel(self.model)
        gag.setScale(self.scale)
        gag.setPythonTag('Stats', self.cls)
        self.gag = gag
        return gag 
    
    def getLevel(self):
        levels = {0 : 6, 1 : 7, 2 : 5, 3 : 4, 4 : 1, 5 : 2, 6 : 3}
        gagMgr = render.getPythonTag('GagManager')
        gags = list(gagMgr.getGags().keys())
        lvl = levels.get(gags.index(self.name))
        return lvl
        
        