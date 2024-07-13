from direct.showbase.DirectObject import DirectObject
from direct.actor.Actor import Actor
from panda3d.core import Texture, Vec4
from doomsday.avatar.ShadowCaster import ShadowCaster

phase_4 = 'phase_4/models/char'
phase_5 = 'phase_5/models/char'
suitAnims = [
  [phase_4, 'neutral'],
  [phase_4, 'walk'],
  [phase_5, 'landing'],
  [phase_5, 'throw-object'],
  [phase_4, 'pie-small'],
  [phase_4, 'squirt-small'],
  [phase_4, 'slip-backward'],
  [phase_4, 'slip-forward']
]
medallionColors = {'corp' : Vec4(0.863, 0.776, 0.769, 1.0), 'money' : Vec4(0.749, 0.769, 0.749, 1.0), 'legal' : Vec4(0.749, 0.776, 0.824, 1.0), 'sales' : Vec4(0.843, 0.745, 0.745, 1.0)}

class Suit(DirectObject):
    
    def __init__(self, suit, scale):
        self.suitType = suit
        self.scale = scale
        self.isLose = False
        self.shadow = None
        
    def setupSuit(self, dept, handColor, isSkeleton = False, isWaiter = False):
        self.isLose = False
        if not isSkeleton:
            suit = loader.loadModel('phase_4/models/char/suit%s-mod.bam' % (self.suitType))
        else:
            suit = loader.loadModel('phase_5/models/char/cog%s_robot-zero.bam' % (self.suitType))
            self.scale = self.scale * 1.0173
            parts = suit.findAllMatches('**/pPlane*')
            for partNum in range(0, parts.getNumPaths()):
                bb = parts.getPath(partNum)
                bb.setTwoSided(1)
            tie = suit.find('**/tie')
            if tie.isEmpty():
                return
            if(dept == 'corp'): 
                tieType = 'boss'
            else:
                tieType = dept
            tieTex = loader.loadTexture('phase_5/maps/cog_robot_tie_%s.jpg' % (tieType))
            tieTex.setMinfilter(Texture.FTLinearMipmapLinear)
            tieTex.setMagfilter(Texture.FTLinear)
            tie.setTexture(tieTex, 1)
        self.suit = suit
        self.dept = dept
        if not isWaiter and not isSkeleton:
            self.setClothing(dept, handColor)
        elif isWaiter:
            self.setClothing('waiter', handColor)
        self.generateMedallion()
        
    def setupLoseSuit(self, dept, handColor, isSkeleton = False, isWaiter = False):
        self.isLose = True
        if not isSkeleton:
            suit = loader.loadModel('phase_4/models/char/suit%s-lose-mod.bam' % (self.suitType))
        else:
            suit = loader.loadModel('phase_5/models/char/cog%s_robot-lose-mod.bam' % (self.suitType))
            self.scale = self.scale * 1.0173
            parts = suit.findAllMatches('**/pPlane*')
            for partNum in range(0, parts.getNumPaths()):
                bb = parts.getPath(partNum)
                bb.setTwoSided(1)
            tie = suit.find('**/tie')
            if tie.isEmpty():
                return
            if(dept == 'corp'): 
                tieType = 'boss'
            else:
                tieType = dept
            tieTex = loader.loadTexture('phase_5/maps/cog_robot_tie_%s.jpg' % (tieType))
            tieTex.setMinfilter(Texture.FTLinearMipmapLinear)
            tieTex.setMagfilter(Texture.FTLinear)
            tie.setTexture(tieTex, 1)
        self.suit = suit
        self.dept = dept
        if not isWaiter and not isSkeleton:
            self.setClothing(dept, handColor)
        elif isWaiter:
            self.setClothing('waiter', handColor)
        
    def generate(self):
        if not self.isLose:
            animDict = self.getAnimations()
            self.actor = Actor(self.suit, animDict)
        else:
            self.actor = Actor(self.suit, {'lose' : loader.loadModel('phase_4/models/char/suit%s-lose.bam' % (self.suitType))})
        self.shadow = ShadowCaster(self.actor)
        self.shadow.initializeDropShadow()
        self.actor.setScale(self.scale)
        
    def generateMedallion(self):
        icons = loader.loadModel('phase_3/models/gui/cog_icons.bam')
        chestJoint = self.suit.find('**/joint_attachMeter')
        medallion = icons.find('**/%sIcon' % (self.dept.title()))
        medallion.reparentTo(chestJoint)
        medallion.setPosHprScale(0.02, 0.05, 0.04, 180.0, 0.0, 0.0, 0.51, 0.51, 0.51)
        medallion.setColor(medallionColors[self.dept])
        medallion.setName('Medallion')
        icons.removeNode()
        
    def getShadow(self):
        return self.shadow
        
    def getActor(self):
        return self.actor
        
    def getSuit(self):
        return self.suit
    
    def getAnimations(self):
        anims = {}
        for anim in suitAnims:
            animName = anim[1]
            anims[animName] = loader.loadModel('%s/suit%s-%s.bam' % (anim[0], self.suitType, animName))
        return anims    
    
    # Clothing Types: 0 = Sellbot, 1 = Cashbot, 2 = Lawbot, 3 = Bossbot, 4 = Waiter   
    def setClothing(self, clothingType, handColor):
        clothingMatches = {'sales' : 's', 'money' : 'm', 'legal' : 'l', 'corp' : 'c', 'waiter' : 'waiter_m'}
        clothingParts = ['sleeve', 'blazer', 'leg']
        for part in clothingParts:
            nodeNames = {'sleeve' : 'arms', 'leg' : 'legs', 'blazer' : 'torso'}
            texture = loader.loadTexture('phase_3.5/maps/%s_%s.jpg' % (clothingMatches[clothingType], part))
            self.suit.find('**/%s' % (nodeNames[part])).setTexture(texture, 1)
        self.suit.find('**/hands').setColor(handColor)
            