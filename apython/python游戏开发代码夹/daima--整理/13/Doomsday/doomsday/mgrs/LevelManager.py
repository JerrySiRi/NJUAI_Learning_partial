from direct.showbase.DirectObject import DirectObject

class LevelManager(DirectObject):
    
    level = 0
    exp = 0
    unlockedGags = []
    
    unlockGags = {
      1: 'Cupcake',
      3: 'Fruit Pie Slice',
      5: 'Cream Pie Slice',
      10 : 'Whole Fruit Pie',
      15 : 'Whole Cream Pie',
      20 : 'Birthday Cake',
      30 : 'Wedding Cake'
    }
    
    unlockLaff = {
      3 : 5, 7 : 5, 14: 10, 18 : 20
    }
    
    def __init__(self, gagMgr):
        render.setPythonTag('LevelManager', self)
        self.gagMgr = gagMgr
        self.levels = [
            Level(requiredExp = 0),
            Level(requiredExp = 30),
            Level(requiredExp = 75),
            Level(requiredExp = 150),
            Level(requiredExp = 200),
            Level(requiredExp = 250),
            Level(requiredExp = 325),
            Level(requiredExp = 400),
            Level(requiredExp = 475),
            Level(requiredExp = 525),
            Level(requiredExp = 625),
            Level(requiredExp = 725),
            Level(requiredExp = 825),
            Level(requiredExp = 925),
            Level(requiredExp = 1025),
            Level(requiredExp = 1200),
            Level(requiredExp = 1375),
            Level(requiredExp = 1550),
            Level(requiredExp = 1725),
            Level(requiredExp = 1990),
            Level(requiredExp = 2100),
            Level(requiredExp = 2300),
            Level(requiredExp = 2500),
            Level(requiredExp = 2700),
            Level(requiredExp = 2900),
            Level(requiredExp = 3100),
            Level(requiredExp = 3300),
            Level(requiredExp = 3500),
            Level(requiredExp = 3700),
            Level(requiredExp = 3900),
        ]
        self.levelUp()
        
    def addEXP(self, exp):
        self.exp += exp
        if self.level < len(self.levels):
            if(self.exp >= self.levels[self.level].getRequiredEXP()):
                self.levelUp()
        render.getPythonTag("Hud").updateEXPBar(self)
        
    def getEXP(self):
        return self.exp
    
    def getEXPToNextLevel(self):
        if(self.level < len(self.levels)):
            return self.levels[self.level].getRequiredEXP()
        else:
            return 0
    
    def unlockGag(self, gagName):
        avatar = render.find('**/Toon').getPythonTag('Avatar')
        avatar.setCurrentGag(gagName)
        self.unlockedGags.append(self.gagMgr.getGagByName(gagName))
        
    def boostLaff(self, amount):
        avatar = render.find('**/Toon').getPythonTag('Avatar')
        avatar.maxHp += amount
        avatar.hp += amount
        avatar.updateLaffMeter()
        
    def levelUp(self):
        self.level += 1
        rewards = self.hasRewards()
        if(len(rewards) > 0):
            if(len(rewards) == 1):
                if(isinstance(rewards[0], str)):
                    self.unlockGag(rewards[0])
                else:
                    self.boostLaff(rewards[0])
            else:
                for reward in rewards:
                    if(isinstance(reward, str)):
                        self.unlockGag(reward)
                    else:
                        self.boostLaff(reward)
        print("Leveled up to Level %s!" % (str(self.level)))
        render.getPythonTag("Hud").updateEXPBar(self)
        
    def hasRewards(self):
        rewards = []
        gag = self.unlockGags.get(self.level)
        boost = self.unlockLaff.get(self.level)
        if(gag != None):
            rewards.append(gag)
        if(boost != None):
            rewards.append(boost)
        return rewards
        
    def getUnlockedGags(self):
        return self.unlockedGags
    
    def getMaxLevel(self):
        return len(self.levels)
    
    def getLevel(self):
        return self.level

class Level(DirectObject):
    
    def __init__(self, requiredExp):
        self.requiredExp = requiredExp
        
    def getRequiredEXP(self):
        return self.requiredExp