from direct.showbase.DirectObject import DirectObject
from doomsday.cog.Dept import Dept
from panda3d.core import VBase4

class Attributes(DirectObject):
    
    depts = [Dept('sales'), Dept('money'), Dept('legal'), Dept('corp')]
    handColors = {
    'corporate_raider' : VBase4(0.85, 0.55, 0.55, 1.0),
    'blood_sucker' : VBase4(0.95, 0.95, 1.0, 1.0),
    'spin_doctor' : VBase4(0.5, 0.8, 0.75, 1.0),
    'penny_pincher' : VBase4(1.0, 0.5, 0.6, 1.0),
    'loan_shark' : VBase4(0.5, 0.85, 0.75, 1.0),
    'cold_caller' : VBase4(0.55, 0.65, 1.0, 1.0),
    'big_cheese' : VBase4(0.75, 0.95, 0.75, 1.0),
    'legal_eagle' : VBase4(0.25, 0.25, 0.5, 1.0)
    }
    
    def __init__(self):
        pass
    
    def getHandColor(self, cogName):
        return self.handColors[cogName]
    
    def getASize(self):
        return 6.06
    
    def getBSize(self):
        return 5.29
    
    def getCSize(self):
        return 4.14
    
    def getDept(self, deptID):
        if(isinstance(deptID, int)):
            if(deptID <= len(self.depts)):
                return self.depts[deptID]
            else:
                return None
        elif(isinstance(deptID, str)):
            for dept in range(len(self.depts)):
                if(dept == deptID):
                    return dept
            return None;
                
