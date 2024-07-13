from direct.showbase.DirectObject import DirectObject
from panda3d.core import VBase4

class Dept(DirectObject):
    
    depts = {
        'sales' : 'Sellbot', 
        'money' : 'Cashbot', 
        'legal' : 'Lawbot',
        'corp' : 'Bossbot'
    }
    
    handColors = {
        'sales' : VBase4(0.95, 0.75, 0.95, 1.0), 
        'money' : VBase4(0.65, 0.95, 0.85, 1.0), 
        'legal' : VBase4(0.75, 0.75, 0.95, 1.0),
        'corp' : VBase4(0.95, 0.75, 0.75, 1)
    }
    
    def __init__(self, dept):
        self.dept = dept;
        
    def getHandColor(self):
        return self.handColors[self.dept]
        
    def getGameDept(self):
        return self.depts[self.dept]
        
    def getDept(self):
        return self.dept
    
    def getDepts(self):
        return self.depts