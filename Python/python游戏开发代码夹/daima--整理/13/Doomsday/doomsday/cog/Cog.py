from direct.showbase.DirectObject import DirectObject
from direct.interval.IntervalGlobal import ActorInterval, Sequence, Wait, Func
from direct.task.Task import Task
from panda3d.core import Vec4, TextNode
from doomsday.base import Globals, SoundBank
import random, copy

healthColors = [Vec4(0, 1, 0, 1), Vec4(1, 1, 0, 1), Vec4(1, 0.5, 0, 1), Vec4(1, 0, 0, 1), Vec4(0.3, 0.3, 0.3, 1)]
healthGlowColors = [Vec4(0.25, 1, 0.25, 0.5), Vec4(1, 1, 0.25, 0.5), Vec4(1, 0.5, 0.25, 0.5), Vec4(1, 0.25, 0.25, 0.5), Vec4(0.3, 0.3, 0.3, 0)]

class Cog(DirectObject):
    
    def __init__(self, name, dept, suit, head, handColor, height, minLevel, maxLevel):
        self.name = name
        self.dept = dept
        self.head = head
        self.headObj = None
        self.headAccessory = head.getAccessory()
        self.suit = suit
        self.handColor = handColor
        self.height = height
        self.level = random.randint(minLevel, maxLevel)
        self.minLevel = minLevel
        self.maxLevel = maxLevel
        self.version = 1
        self.hit = False
        self.isDefeated = False
        self.healthBar = None
        self.healthCondition = 0
        
    def generate(self, isSkeleton = False, isWaiter = False):
        self.isSkeleton = isSkeleton
        self.isWaiter = isWaiter
        self.suit.setupSuit(self.dept.getDept(), self.handColor, isSkeleton, isWaiter)
        self.suit.generate()
        self.cog = self.suit.getActor()
        self.cog.setPythonTag('Cog', self)
        self.cog.setName(self.name)
        self.cog.flattenStrong()
        if(self.level % 12 != 0):
            self.hp = (self.level + 1) * (self.level + 2)
        else:
            self.hp = (self.level / 12) * 200
        self.maxHp = self.hp
        if not isSkeleton:
            self.headObj = self.head.generate(self.headAccessory)
            self.head.getHead().reparentTo(self.cog.find('**/joint_head'))
        self.corpMedallion = self.cog.find('**/Medallion')
        self.generateHealthBar()
        self.createNameTag()
        if not self.isSkeleton:
            if(self.headObj.getChildren() == 0 and self.head.hasAccessory()):
                self.head.attemptAccessoryFix()
            
    def createNameTag(self):
        try:
            if(self.nameTag):
                self.nameTagPath.removeNode()
        except: pass
        self.nameTag = TextNode("NameTag")
        dept = self.dept.getGameDept()
        name = self.name
        if self.isSkeleton:
            name = "Skelecog"
        if(self.version == 1):
            self.nameTag.setText('%s\n%s\nLevel %s' % (name, dept, self.level))
        else:
            self.nameTag.setText('%s\n%s\nLevel %s v%s.0' % (name, dept, self.level, self.version))
        cogFont = Globals.getFont('vtRemingtonPortable.ttf')
        self.nameTag.setFont(cogFont)
        self.nameTagPath = render.attachNewNode(self.nameTag)
        self.nameTagPath.reparentTo(self.cog.find('**/joint_nameTag'))
        self.nameTagPath.setBillboardPointEye(0)
        head = self.head.getHead()
        jointPos = self.cog.find('**/joint_head').getPos(render)
        if(head != None):
            min, max = head.getTightBounds()
            size = max - min
            zPos = head.getPos(render).getZ() - size.getZ()
            pos = head.getPos(render).getZ() + size.getZ() + 2.4
        else:
            pos = jointPos.getZ() + 2.4
        self.nameTagPath.setZ(pos)
        self.nameTag.setAlign(TextNode.ACenter)
        self.nameTag.setCardColor(0.8, 0.8, 0.8, 0.5)
        self.nameTag.setCardAsMargin(0,0,0,-0.2)
        self.nameTag.setCardDecal(True)
        self.nameTag.setTextColor(0.2,0.2,0.2,1.0)
        self.nameTagPath.setScale(0.35)
        
    def playAnim(self, anim, playRate, loop):
        if(loop):
            ActorInterval(self.cog, anim, playRate = playRate).loop()
        else:
            ActorInterval(self.cog, anim, playRate = playRate)
            
    def updateHealthBar(self):
        health = float(float(self.hp) / float(self.maxHp))
        if health < 1:
            self.corpMedallion.hide()
            self.healthBar.show()
        if health > 0.95:
            condition = 0
        elif health > 0.7:
            condition = 1
        elif health > 0.3:
            condition = 2
        elif health > 0.05:
            condition = 3
        elif health > 0:
            condition = 4
        else:
            condition = 5
        if(self.healthCondition != condition):
            if(condition == 4):
                blinkTask = Task.loop(Task(self.__blinkRed), Task.pause(0.75), Task(self.__blinkGray), Task.pause(0.1))
                base.taskMgr.add(blinkTask, 'blink-task')
            elif(condition == 5):
                if(self.healthCondition == 4):
                    base.taskMgr.remove('blink-task')
                if(self.isDefeated == False):
                    blinkTask = Task.loop(Task(self.__blinkRed), Task.pause(0.25), Task(self.__blinkGray), Task.pause(0.1))
                    base.taskMgr.add(blinkTask, 'blink-task')
                    self.isDefeated = True
                    if not self.cog.hasPythonTag("Support"):
                        roundInstance = render.getPythonTag('Round')
                        wave = roundInstance.getCurrentWave()
                        wave.setCogsDefeated(wave.getCogsDefeated() + 1)
                    base.taskMgr.doMethodLater(1.5, self.setDefeated, 'Set Cog Defeated')
            else:
                self.healthBar.setColor(healthColors[condition], 1)
                self.healthBarGlow.setColor(healthGlowColors[condition], 1)     
            self.healthCondition = condition

    def __blinkRed(self, task):
        self.healthBar.setColor(healthColors[3], 1)
        self.healthBarGlow.setColor(healthGlowColors[3], 1)
        return Task.done
    
    def __blinkGray(self, task):
        if not self.healthBar:
            return
        self.healthBar.setColor(healthColors[4], 1)
        self.healthBarGlow.setColor(healthGlowColors[4], 1)
        return Task.done
    
    def generateHealthBar(self):
        self.removeHealthBar()
        model = loader.loadModel('phase_3.5/models/gui/matching_game_gui.bam')
        meter = model.find("**/minnieCircle")
        meter.setScale(3)
        meter.setH(180)
        meter.setColor(healthColors[0])
        joint = self.cog.find('**/joint_attachMeter')
        meter.reparentTo(joint)
        self.healthBar = meter
        glow = loader.loadModel('phase_3.5/models/props/glow.bam')
        glow.reparentTo(self.healthBar)
        glow.setScale(0.28)
        glow.setPos(-0.005, 0.01, 0.015)
        glow.setColor(healthGlowColors[0])
        meter.flattenLight()
        self.healthBarGlow = glow
        self.healthCondition = 0
        self.healthBar.hide()
        if(self.isSkeleton):
            self.healthBar.setPos(0, 0.1, 0)

    def removeHealthBar(self):
        if self.healthBar:
            self.healthBar.removeNode()
            self.healthBar = None
        if self.healthCondition == 4 or self.healthCondition == 5:
            taskMgr.remove(self.uniqueName('blink-task'))
        self.healthCondition = 0
        return
            
    def setVersion(self, version):
        self.version = version
        
    def getVersion(self):
        return self.version
    
    def destroyCog(self):
        self.suit.getShadow().deleteDropShadow()
        self.cog.cleanup()
        self.cog.removeNode()
    
    def setDefeated(self, task):
        def playSound(sound):
            SoundBank.getSound(sound).play()
        def generateReward(pos, hpr):
            reward = random.choice([True, False])
            if(reward):
                dropMgr = render.getPythonTag('DropManager')
                drop = dropMgr.generateRandomDrop()
                drop.reparentTo(render)
                drop.setPos(pos.getX(), pos.getY(), pos.getZ() + 0.8)
        if self.cog.isEmpty():
            return
        pos = self.cog.getPos()
        hpr = self.cog.getHpr()
        head = copy.copy(self.cog.find('**/Head'))
        self.destroyCog()
        self.suit.setupLoseSuit(self.dept.getDept(), self.handColor, self.isSkeleton, self.isWaiter)
        self.suit.generate()
        render.getPythonTag('WorldCollisions').addCogGroundCollision(ent = self.suit.getActor())
        self.cog = self.suit.getActor()
        if not self.isSkeleton:
            head.reparentTo(self.cog.find("**/joint_head"))
        self.cog.setPos(pos)
        self.cog.setHpr(hpr)
        self.cog.reparentTo(render)
        self.cog.play('lose')
        Sequence(
          Wait(1.5),
          Func(playSound, 'cog_laugh'),
          Wait(3.5),
          Func(playSound, 'cog_explode'),
          Func(generateReward, pos, hpr),
          Wait(8),
          Func(self.destroyCog),
        ).start()
        return Task.done

    def setLevel(self, level):
        self.level = level
        self.hp = (level + 1) * (level + 2)
        self.maxHp = self.hp
    
    def setHealth(self, hp):
        self.hp = hp
        self.updateHealthBar()
        
    def getHealth(self):
        return self.hp
    
    def setHit(self, flag):
        self.hit = flag
        
    def wasHit(self):
        return self.hit
            
    def stopAnim(self, anim):
        self.cog.stop()
        
    def cleanUp(self):
        self.cog.cleanup()
        self.cog.removeNode()
        del self
        
    def getName(self):
        return self.name
    
    def getDept(self):
        return self.dept
    
    def getHead(self):
        return self.headObj
    
    def isDefeated(self):
        return self.isDefeated
    
    def getHeight(self):
        return self.height
    
    def getLevelCurve(self):
        return [self.minLevel, self.maxLevel]
    
    def getLevel(self):
        return self.level
        
    def getCog(self):
        return self.cog
        