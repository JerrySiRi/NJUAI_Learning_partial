from direct.showbase.DirectObject import DirectObject
from panda3d.core import VBase3

class Spawn(DirectObject):
    
    def __init__(self, pos, hpr):
        self.pos = pos
        self.hpr = hpr
        self.path = None
        self.occupied = False
        
    def setOccupied(self, flag):
        self.occupied = flag
        
    def isOccupied(self):
        return self.occupied
        
    def setPath(self, path):
        self.path = path
        
    def getPath(self):
        return self.path
        
    def getPos(self):
        return self.pos
    
    def getHpr(self):
        return self.hpr
    
class Path(DirectObject):
    
    checkpoints = []
    
    def addCheckpoint(self, checkpoint):
        self.checkpoints.append(checkpoint)
        
    def setCheckpoints(self, checkpoints):
        self.checkpoints = checkpoints
        
    def removeCheckpoint(self, pos):
        for checkpoint in self.checkpoints:
            if(checkpoint.getPos() == pos):
                self.checkpoints.remove(checkpoint)
        
    def getCheckpoints(self):
        return self.checkpoints
    
class Checkpoint(DirectObject):
    
    def __init__(self, pos):
        self.pos = pos
        
    def getPos(self):
        return self.pos