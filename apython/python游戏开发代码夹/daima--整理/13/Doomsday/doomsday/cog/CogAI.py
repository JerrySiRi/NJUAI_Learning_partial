from direct.showbase.DirectObject import DirectObject
from direct.actor.Actor import Actor
from direct.task.Task import Task
from panda3d.ai import AIWorld, AICharacter
from panda3d.core import VBase3, Vec4
from doomsday.cog.CogAttacks import CogAttacks
from doomsday.base import SoundBank
import random

class CogAI(DirectObject):
    
    cancelStep = False
    
    def __init__(self, cog, spawn, support = False):
        self.cog = cog
        self.spawn = spawn
        self.attack = True
        self.support = support
        self.flyIn()
        
    def setAI(self):
        collisions = render.getPythonTag('WorldCollisions')
        collisions.addCogGroundCollision(self.cog)
        self.AIWorld = AIWorld(render)
        self.AIChar = AICharacter('Cog', self.cog.getCog(), -125, 90, -14)
        self.AIWorld.addAiChar(self.AIChar)
        self.AIBehaviors = self.AIChar.getAiBehaviors()
        if self.support == False:
            self.AIBehaviors.pathFollow(8)
            self.AIBehaviors.addToPath(VBase3(110.60, -0.32, 4.57))
            checkpoints = self.spawn.getPath().getCheckpoints()
            for checkpoint in range(len(checkpoints)):
                self.AIBehaviors.addToPath(checkpoints[checkpoint].getPos())
            self.AIBehaviors.startFollow()
        else:
            self.AIBehaviors.pursue(render.find('**/Toon'))
        self.cog.getCog().loop('walk')
        base.taskMgr.add(self.AIUpdate, "AIUpdate")
        
    def calcChance(self, percent):
        if(random.randint(0, 100) < percent):
            return True
        else:
            return False
        
    def toggleAttack(self):
        if(self.attack):
            self.attack = False
        else:
            self.attack = True
        
    def AIUpdate(self, task):
        if(self.AIBehaviors.behaviorStatus('pathfollow') == 'done'):
            self.cog.getCog().loop('neutral')
            self.AIBehaviors.removeAi('pathfollow')
            toonHall = render.getPythonTag("ToonHall")
            toonHall.startCogEnter(self.cog)
            return Task.done
        else:
            if(self.cog.getHealth() > 0):
                if(self.calcChance(40) and self.attack):
                    def resumeAI(task):
                        self.AIBehaviors.resumeAi('pathfollow')
                        self.cog.getCog().loop('walk')
                        return Task.done
                    def enableAttacks(task):
                        return Task.done
                    avatar = render.find('**/Toon')
                    if(self.cog.getCog().getDistance(avatar) <= 20):
                        self.AIBehaviors.pauseAi('pathfollow')
                        self.cog.getCog().stop()
                        self.attack = False
                        self.cog.getCog().lookAt(avatar)
                        self.cog.getCog().play('throw-object')
                        attack = CogAttacks().getRandomAttack(self.cog.getLevel() * 2)
                        attack.execute(self.cog)
                        base.taskMgr.doMethodLater(10, enableAttacks, 'Toggle Attack')
                        base.taskMgr.doMethodLater(3, resumeAI, 'Resume AI')
                self.AIWorld.update()
                return Task.cont
            else:
                self.AIBehaviors.removeAi('pathfollow')
                return Task.done
        
    def flyIn(self):
        phase_4 = "phase_4/models/props"
        cog = self.cog.getCog()

        collisions = render.getPythonTag('WorldCollisions')
        collisions.addCogCollision(self.cog)
        self.propeller = Actor(loader.loadModel(phase_4 + "/propeller-mod.bam"), {'chan' : loader.loadModel(phase_4 + "/propeller-chan.bam")})
        self.propeller.reparentTo(cog.find('**/joint_head'))
        propSound = SoundBank.getSound('propeller')
        propSound.setLoop(True)
        propSound.setVolume(0.8)
        propSound.play()
        pos = cog.getPos()
        cog.setPos(pos.getX(), pos.getY(), pos.getZ() + 20)
        cog.pose('landing', 1)
        cog.colorScaleInterval(4.8, Vec4(1, 1, 1, 1), startColorScale=Vec4(0.2509803921568627, 0.2509803921568627, 0.2509803921568627, 0.25), blendType='easeInOut').start()
        path = cog.posInterval(5, pos, startPos = cog.getPos())
        path.start()
        self.propeller.loop('chan', fromFrame=0, toFrame=3)
        base.taskMgr.add(self.handleCogDead, 'Handle Cog Death')
        base.taskMgr.doMethodLater(4, self.playInSound, 'Play In Sound', extraArgs = [propSound], appendTask = True)
        base.taskMgr.doMethodLater(5, self.landCog, 'Land Cog')
        
    def handleCogDead(self, task):
        if(self.cog.isDefeated):
            self.cancelStep = True
            collisions = render.getPythonTag('WorldCollisions')
            collisions.addCogGroundCollision(cog = self.cog)
            return Task.done
        else:
            return Task.cont
        
        
    def landCog(self, task):
        if not self.cancelStep:
            base.taskMgr.remove('Handle Cog Death')
            self.propeller.play('chan', fromFrame=35, toFrame=87)
            self.cog.getCog().play('landing')
            base.taskMgr.doMethodLater(3, self.removePropeller, 'Remove Propeller')
        return Task.done
    
    def removePropeller(self, task):
        self.propeller.cleanup()
        self.propeller.removeNode()
        self.setAI()
        return Task.done
        
    def playInSound(self, sound, task):
        if not self.cancelStep:
            sound.stop()
            SoundBank.getSound('propeller_in').play()
        return Task.done
        