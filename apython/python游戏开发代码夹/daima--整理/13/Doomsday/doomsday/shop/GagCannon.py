from direct.showbase.DirectObject import DirectObject
from direct.task.Task import Task
from direct.interval.IntervalGlobal import ProjectileInterval, Sequence, Wait, Func
from doomsday.shop import ShopGlobals
from doomsday.base import SoundBank
from panda3d.core import Vec3
from panda3d.bullet import *
import copy

def_supply = ShopGlobals.DEFAULT_GAG_CANNON_MAX_SUPPLY

class GagCannon(DirectObject):
    
    def __init__(self, gag = None, supply = def_supply, health = 20, fireSpeed = 2, searchTime = 4):
        self.gag = None
        self.maxSupply = supply
        self.supply = 0
        self.maxHp = health
        self.hp = health
        self.fireSpeed = fireSpeed
        self.searchTime = searchTime
        self.maxDistance = 100
        self.target = None
        self.cannon = None
        self.gagMgr = None
        self.firing = False
        self.gagProp = None
        self.fireSound = SoundBank.getSound('cannon_fire')
        self.adjustSound = SoundBank.getSound('cannon_adjust')
        self.whizzSound = SoundBank.getSound('cannon_whizz')
        
    def generate(self):
        self.cannon = loader.loadModel("phase_4/models/minigames/toon_cannon.bam")
        base.taskMgr.doMethodLater(self.searchTime, self.lookAround, 'Look Around')
        base.taskMgr.doMethodLater(self.searchTime, self.searchForTarget, 'Search For Target')
        self.adjustSound.setVolume(0.2)
        self.adjustSound.setLoop(True)
        return self.cannon
    
    def addGagProp(self):
        self.gagMgr = render.getPythonTag('GagManager')
        self.gagProp = self.gagMgr.getGagByName(self.gag).generate()
        self.gagProp.setName("Turrent_Prop")
        self.gagProp.reparentTo(self.cannon.find('**/cannon'))
        self.gagProp.setPos(0, 5.3, 0)
        self.gagProp.setHpr(0, 270, 0)
        
    def removeGagProp(self):
        if(self.gagProp != None):
            self.gagProp.removeNode()
            
    def lookAround(self, task):
        if(self.target == None):
            self.adjustSound.play()
            cannon = self.cannon.find('**/cannon')
            def reset(task):
                if(self.target == None):
                    cannon.hprInterval(2, Vec3(0, 0, 0)).start()
                    Sequence(
                      Wait(2),
                      Func(self.adjustSound.stop)
                    ).start()
                base.taskMgr.doMethodLater(self.searchTime, self.lookAround, 'Look Around')
                return Task.done
            def lookOtherWay(task):
                if(self.target == None):
                    cannon.hprInterval(4, Vec3(-40, 0, 0)).start()
                    base.taskMgr.doMethodLater(4, reset, 'Reset H')
                return Task.done
            cannon.hprInterval(2, Vec3(40, 0, 0)).start()
            base.taskMgr.doMethodLater(2, lookOtherWay, 'Look Other Way')
        return Task.done
    
    def attemptSupplyRefill(self, task):
        if(self.supply <= round(float(self.maxSupply) * 0.4)):
            barrels = render.find('**/Barrels').getChildren()
            for barrel in barrels:
                if(self.cannon.getDistance(barrel) <= 25):
                    stats = barrel.getPythonTag('Stats')
                    if(stats.getSupply() > 0):
                        neededSupply = self.maxSupply - self.supply
                        barrelSupply = stats.getSupply()
                        if(barrelSupply >= neededSupply):
                            self.supply += (barrelSupply - neededSupply)
                            stats.setSupply(barrelSupply - neededSupply)
                        else:
                            self.supply += barrelSupply
                            stats.setSupply(0)
                        self.gag = stats.getGag()
                        self.addGagProp()
        return Task.done
    
    def searchForTarget(self, task):
        if not self.firing and self.target == None:
            cogs = render.find('**/Cogs').getChildren()
            distances = []
            for cog in cogs:
                distance = self.cannon.getDistance(cog)
                if(distance <= self.maxDistance):
                    distances.append(distance)
            if(len(distances) > 0):
                distances.sort()
                checkDistanceIndex = 0
                for cog in cogs:
                    distance = self.cannon.getDistance(cog)
                    if(distance == distances[checkDistanceIndex]):
                        if(self.supply > 0):
                            #if(self.isTargetReachable(cog)):
                                self.setTarget(cog)
                                self.cannon.find('**/cannon').lookAt(self.target, 0, 0, 5)
                                self.cannon.find('**/cannon').setP(self.cannon.find('**/cannon').getP() + 1.5)
                                base.taskMgr.doMethodLater(self.fireSpeed, self.attackTarget, 'Attack Target')
                                break
                            #else:
                                #if(checkDistanceIndex + 1 < len(distances)):
                                    #checkDistanceIndex += 1
                                #else:
                                    #checkDistanceIndex = 0
                        else:
                            base.taskMgr.doMethodLater(self.fireSpeed, self.attemptSupplyRefill, 'Attempt Supply Refill')
        return Task.cont
    
    def isTargetReachable(self, target):
        rayFrom = self.gagProp.getPos()
        rayTo = target.find('**/Head').getPos(render)
        
        world = BulletWorld()
        result = world.rayTestClosest(rayFrom, rayTo).getNode()
        if(result != None):
            print(result.getName())
            if(result.getName() == 'Head'):
                return True
        return False
    
    def resetCannon(self, task):
        if not self.gagProp.isEmpty():
            self.gagProp.show()
            base.taskMgr.add(self.lookAround, 'Look Around')
        return Task.done

    def attackTarget(self, task):
        if(self.hp > 0):
            if(self.target != None):
                cog = self.target.getPythonTag('Cog')
                if(cog.getHealth() > 0):
                    self.gagProp.hide()
                    gag = copy.copy(self.gagProp)
                    gag.reparentTo(render)
                    gag.setPos(self.gagProp.getPos(render))
                    gag.setHpr(self.gagProp.getHpr(render))
                    endPos = self.target.find('**/Head').getPos(render)
                    self.projectile = ProjectileInterval(gag, startPos=gag.getPos(render), endPos=endPos, gravityMult=1, duration=1)
                    gag.show()
                    self.projectile.start()
                    self.fireSound.play()
                    self.whizzSound.play()
                    render.getPythonTag('WorldCollisions').addGagCollision(gag)
                    self.target = None
                    self.firing = False
                    base.taskMgr.doMethodLater(2, self.removeGag, 'Remove Gag', extraArgs = [gag, self.projectile], appendTask = True)
                    base.taskMgr.doMethodLater(2, self.resetCannon, 'Reset Cannon')
                    self.cannon.find('**/cannon').setHpr(0, 0, 0)
                    self.setSupply(self.getSupply() - 1)
                else:
                    self.target = None
                    self.firing = False
                    base.taskMgr.doMethodLater(2, self.resetCannon, 'Reset Cannon')
                    self.cannon.find('**/cannon').setHpr(0, 0, 0)
        return Task.done
    
    def removeGag(self, gag, trajectory, task):
        trajectory.finish()
        gag.removeNode()
        return Task.done
        
    def setTarget(self, target = None):
        self.target = target
        
    def getTarget(self):
        return self.target
    
    def setMaxHealth(self, maxHp):
        self.maxHp = maxHp
    
    def getMaxHealth(self):
        return self.maxHp
    
    def setHealth(self, hp):
        self.hp = hp
        
    def getHealth(self):
        return self.hp
    
    def setSupply(self, supply):
        self.supply = supply
        if(self.supply == 0):
            self.gag = None
            self.removeGagProp()
        
    def getMaxSupply(self):
        return self.maxSupply
        
    def getSupply(self):
        return self.supply
    
    def getFireSpeed(self):
        return self.fireSpeed
    
    def getSearchTime(self):
        return self.searchTime
    
class PotentialTarget(DirectObject):
    
    def __init__(self, distance, level):
        self.distance = distance
        self.level = level
        
    def getDistance(self):
        return self.distance
    
    def getLevel(self):
        return self.level