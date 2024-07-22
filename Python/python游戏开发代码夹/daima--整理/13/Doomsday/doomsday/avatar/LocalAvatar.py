from sys import argv
from direct.task import Task
from direct.actor.Actor import Actor
from pandac.PandaModules import CollisionTraverser, BitMask32
from direct.interval.IntervalGlobal import ActorInterval, ProjectileInterval
from direct.showbase.InputStateGlobal import inputState
from direct.controls.GravityWalker import GravityWalker
from direct.showbase.DirectObject import DirectObject
from panda3d.core import Point3, Vec3, NodePath
from doomsday.base.Hud import Hud
from doomsday.base import SoundBank
from doomsday.avatar.LaffMeter import LaffMeter
from doomsday.mgrs.GagManager import GagManager
import copy

class Player(DirectObject):
    keyMap = {'left': 0,
     'right': 0,
     'forward': 0,
     'backward': 0,
     'control': 0}
    movingJumping = False
    movingNeutral = False
    movingForward = False
    movingRotation = False
    movingBackward = False
    movementEnabled = True
    throwingPie = False
    canThrowPie = True
    currentGag = None
    gagMgr = None
    hit = False
    data = {}
    hp = 15
    maxHp = 15
    jellybeans = 0

    def __init__(self, avatar):
        self.data = avatar.getData()
        self.localAvatar = avatar.getAvatar()
        self.gag = None
        self.setupToon()
        self.walkSound = SoundBank.getSound('toon_walk')
        self.runSound = SoundBank.getSound('toon_run')
        self.laffMeter = LaffMeter(self)
        self.laffMeter.setPos(-1.18, 0, -0.84)
        self.laffMeter.start()
        self.localAvatar.setPythonTag('Avatar', self)
        self.gagMgr = GagManager()
        render.setPythonTag('GagManager', self.gagMgr)
        from doomsday.shop.GagCannon import GagCannon
        from doomsday.shop.GagBarrel import GagBarrel
        gagCannon = GagCannon().generate()
        gagCannon.reparentTo(render)
        gagCannon.setPos(43.36, -0.82, 4.03) 
        gagCannon.setH(89.47)  
        #gagCannon2 = GagCannon().generate()
        #gagCannon2.reparentTo(render)
        #gagCannon2.setPos(-60.18, -9.06, 1.23) 
        #gagCannon2.setH(93.90)   
        barrel = GagBarrel('Wedding Cake').generate()
        barrel.setPos(43.36, 6.71, 4.03)
        barrel.setH(89.47)
        barrel = GagBarrel('Wedding Cake').generate()
        barrel.setPos(-57.20, -5.61, 1.23)
        barrel.setH(91.19)
        return
    
    def getData(self):
        return self.data
    
    def playMovementSound(self, sound):
        sound.setVolume(0.8)
        sound.setLoop(True)
        sound.play()

    def setHealth(self, paramHealth):
        self.hp = paramHealth
        self.laffMeter.adjustFace(self.hp, self.maxHp, quietly=0)
        
    def setJellybeans(self, amt):
        self.jellybeans = amt
        
    def getJellybeans(self):
        return self.jellybeans
        
    def teleportIn(self):
        portal_chan = loader.loadModel('phase_3.5/models/props/portal-chan.bam')
        portal = Actor(loader.loadModel('phase_3.5/models/props/portal-mod.bam'), {'chan' : portal_chan})
        portal.setScale(1.3)
        portal.setBin('fixed', 40)
        portal.setDepthWrite(False)
        portal.setDepthTest(False)
        portal.reparentTo(self.localAvatar.find('**/joint_nameTag'))
        portal.setPos(0, -2, -0.05)
        portal.setHpr(0, 0, 0)
        portal.play('chan', fromFrame=60)
        
    def setMovement(self, flag):
        self.movementEnabled = flag
        if(flag is False):
            self.movingJumping = False
            self.movingBackward = False
            self.movingForward = False
            self.movingNeutral = False
            self.movingRotation = False
            #base.taskMgr.remove('controlManager')
            self.keyMap = {
            'left': 0, 'right': 0, 'forward': 0, 'backward': 0,
            'control': 0}
            self.walkControls.setWalkSpeed(0, 0, 0, 0)
        else:
            base.taskMgr.add(self.handleMovement, 'controlManager')
            self.walkControls.enableAvatarControls()
        base.localAvatar.physControls = self.walkControls

    def setHit(self, flag):
        self.hit = flag

    def isHit(self):
        return self.hit

    def getHealth(self):
        return self.hp

    def getAvatar(self):
        return self.localAvatar

    def setupCamera(self):
        base.camera.reparentTo(self.localAvatar)
        base.camera.setPos(0, -13.2375, 3.2375)

    def getAirborneHeight(self):
        return 3.2624999999999997

    def setWatchKey(self, key, input, keyMapName):
        def watchKey(active = True):
            if active == True:
                inputState.set(input, True)
                self.keyMap[keyMapName] = 1
            else:
                inputState.set(input, False)
                self.keyMap[keyMapName] = 0
        
        if(self.movementEnabled):
            base.accept(key, watchKey, [True])
            base.accept(key + '-up', watchKey, [False])

    def handleMovement(self, task):
        if self.keyMap['control'] == 1:
            if self.keyMap['forward'] or self.keyMap['backward'] or self.keyMap['left'] or self.keyMap['right'] and self.throwingPie == False:
                if self.movingJumping == False:
                    if self.localAvatar.physControls.isAirborne:
                        self.setMovementAnimation('running-jump-idle')
                    elif self.keyMap['forward']:
                        if self.movingForward == False:
                            self.setMovementAnimation('run')
                    elif self.keyMap['backward']:
                        if self.movingBackward == False:
                            self.setMovementAnimation('walk', playRate=-1.0)
                    elif self.keyMap['left'] or self.keyMap['right']:
                        if self.movingRotation == False:
                            self.setMovementAnimation('walk')
                elif not self.localAvatar.physControls.isAirborne:
                    if self.keyMap['forward']:
                        if self.movingForward == False:
                            self.setMovementAnimation('run')
                    elif self.keyMap['backward']:
                        if self.movingBackward == False:
                            self.setMovementAnimation('walk', playRate=-1.0)
                    elif self.keyMap['left'] or self.keyMap['right']:
                        if self.movingRotation == False:
                            self.setMovementAnimation('walk')
            elif self.movingJumping == False:
                if self.localAvatar.physControls.isAirborne:
                    self.setMovementAnimation('jump-idle')
                elif self.movingNeutral == False:
                    self.setMovementAnimation('neutral')
            elif not self.localAvatar.physControls.isAirborne:
                if self.movingNeutral == False:
                    self.setMovementAnimation('neutral')
        elif self.keyMap['forward'] == 1:
            if self.movingForward == False:
                if not self.localAvatar.physControls.isAirborne:
                    self.setMovementAnimation('run')
        elif self.keyMap['backward'] == 1:
            if self.movingBackward == False:
                if not self.localAvatar.physControls.isAirborne:
                    self.setMovementAnimation('walk', playRate=-1.0)
        elif self.keyMap['left'] or self.keyMap['right']:
            if self.movingRotation == False:
                if not self.localAvatar.physControls.isAirborne:
                    self.setMovementAnimation('walk')
        elif not self.localAvatar.physControls.isAirborne:
            if self.movingNeutral == False and self.throwingPie == False:
                self.setMovementAnimation('neutral')
        return Task.cont

    def setMovementAnimation(self, loopName, playRate = 1.0):
        if 'jump' in loopName:
            self.movingJumping = True
            self.movingForward = False
            self.movingNeutral = False
            self.movingRotation = False
            self.movingBackward = False
            self.walkSound.stop()
            self.runSound.stop()
        elif loopName == 'run':
            self.movingJumping = False
            self.movingForward = True
            self.movingNeutral = False
            self.movingRotation = False
            self.movingBackward = False
            self.walkSound.stop()
            self.playMovementSound(self.runSound)
        elif loopName == 'walk':
            self.movingJumping = False
            self.movingForward = False
            self.movingNeutral = False
            if playRate == -1.0:
                self.movingBackward = True
                self.movingRotation = False
            else:
                self.movingBackward = False
                self.movingRotation = True
            self.runSound.stop()
            self.playMovementSound(self.walkSound)
        elif loopName == 'neutral':
            self.movingJumping = False
            self.movingForward = False
            self.movingNeutral = True
            self.movingRotation = False
            self.movingBackward = False
            self.runSound.stop()
            self.walkSound.stop()
        elif loopName == 'pie-throw' or loopName == 'pie-throw-2':
            self.throwingPie = True
            self.movingJumping = False
            self.movingForward = False
            self.movingNeutral = False
            self.movingRotation = False
            self.movingBackward = False
            self.runSound.stop()
            self.walkSound.stop()
        if loopName == 'pie-throw':
            ActorInterval(self.localAvatar, 'pie-throw', playRate=playRate, startFrame=0, endFrame=45).loop()
        elif loopName == 'pie-throw-2':
            ActorInterval(self.localAvatar, 'pie-throw', playRate=playRate, startFrame=45, endFrame=90).loop()
        else:
            ActorInterval(self.localAvatar, loopName, playRate=playRate).loop()
            
    def calculateHeight(self, task):
        self.height = task.time * 1.75
        if task.time >= 4:
            self.height = 5
            return Task.done
        return Task.cont

    def gagStart(self):
        if self.throwingPie == False and self.canThrowPie == True:
            base.accept('delete', self.null)
            self.canThrowPie = False
            gagMgr = render.getPythonTag('GagManager')
            self.gag = copy.copy(gagMgr.getGagByName(self.currentGag).generate())
            self.gag.reparentTo(self.localAvatar.find('**/def_joint_right_hold'))
            self.setMovementAnimation('pie-throw')
            base.taskMgr.add(self.calculateHeight, 'Calculate Height')
        return

    def gagThrow(self):
        if self.throwingPie:
            self.setMovementAnimation('pie-throw-2')
            taskMgr.doMethodLater(0.75, self.gagRelease, 'gag release')
        else:
            self.throwingPie = False
        base.taskMgr.remove('Calculate Height')

    def gagRelease(self, task):
        gagRange = NodePath('Gag Range')
        gagRange.reparentTo(self.localAvatar.find('**/joint_nameTag'))
        gagRange.setPos(0, 75, 0)
        gagRange.setHpr(90, -90, 90)
        if self.gag == None:
            gagRange.removeNode()
            base.taskMgr.doMethodLater(0.1, self.enableThrowing, 'Enable Gag Throw')
            return
        else:
            if self.height > 1:
                grav = 0.7 + self.height / 10
            else:
                grav = 0.7
            if self.height > 5.2:
                base.taskMgr.add(self.enableThrowing, 'Enable Gag Throw')
                return
            self.gag.reparentTo(render)
            self.gag.setHpr(gagRange.getHpr(render))
            self.gagMgr.getGagByName(self.currentGag).addCollision(self.gag)
            handJoint = self.localAvatar.find('**/def_joint_right_hold')
            startPos = Vec3(handJoint.getPos(render).getX(), handJoint.getPos(render).getY(), handJoint.getPos(render).getZ() + 0.8)
            self.projectile = ProjectileInterval(self.gag, startPos=startPos, endPos=gagRange.getPos(render), duration=1, gravityMult=grav)
            self.projectile.start()
            SoundBank.getSound('pie_throw').play()
            base.taskMgr.doMethodLater(0.8, self.enableThrowing, 'Enable Gag Throw')
            base.taskMgr.doMethodLater(2, self.destroyGag, 'Destroy Gag', extraArgs = [self.gag, self.projectile], appendTask = True)
            base.accept('delete-up', self.null)
            base.accept('p-up', self.null)
            self.throwingPie = False
            return Task.done
        
    def destroyGag(self, gag, trajectory, task):
        trajectory.finish()
        gag.removeNode()
        return Task.done

    def null(self):
        pass

    def enableThrowing(self, task):
        self.canThrowPie = True
        self.setMovementAnimation('neutral')
        base.accept('delete', self.gagStart)
        base.accept('delete-up', self.gagThrow)
        base.accept('p', self.gagStart)
        base.accept('p-up', self.gagThrow)
        return Task.done

    def removeGag(self, task):
        if self.gag != None:
            self.gag.removeNode()
            self.gag = None
        return Task.done

    def setupPhysics(self):
        base.accept('delete', self.gagStart)
        base.accept('delete-up', self.gagThrow)
        base.accept('p', self.gagStart)
        base.accept('p-up', self.gagThrow)
        self.setWatchKey('arrow_up', 'forward', 'forward')
        self.setWatchKey('w', 'forward', 'forward')
        self.setWatchKey('control-arrow_up', 'forward', 'forward')
        self.setWatchKey('control-w_up', 'forward', 'forward')
        self.setWatchKey('alt-arrow_up', 'forward', 'forward')
        self.setWatchKey('alt-w_up', 'forward', 'forward')
        self.setWatchKey('shift-arrow_up', 'forward', 'forward')
        self.setWatchKey('shift-w_up', 'forward', 'forward')
        self.setWatchKey('arrow_down', 'reverse', 'backward')
        self.setWatchKey('s', 'reverse', 'backward')
        self.setWatchKey('control-arrow_down', 'reverse', 'backward')
        self.setWatchKey('control-s', 'reverse', 'backward')
        self.setWatchKey('alt-arrow_down', 'reverse', 'backward')
        self.setWatchKey('alt-s', 'reverse', 'backward')
        self.setWatchKey('shift-arrow_down', 'reverse', 'backward')
        self.setWatchKey('shift-s', 'reverse', 'backward')
        self.setWatchKey('arrow_left', 'turnLeft', 'left')
        self.setWatchKey('a', 'turnLeft', 'left')
        self.setWatchKey('control-arrow_left', 'turnLeft', 'left')
        self.setWatchKey('control-a', 'turnLeft', 'left')
        self.setWatchKey('alt-arrow_left', 'turnLeft', 'left')
        self.setWatchKey('alt-a', 'turnLeft', 'left')
        self.setWatchKey('shift-arrow_left', 'turnLeft', 'left')
        self.setWatchKey('shift-a', 'turnLeft', 'left')
        self.setWatchKey('arrow_right', 'turnRight', 'right')
        self.setWatchKey('d', 'turnRight', 'right')
        self.setWatchKey('control-arrow_right', 'turnRight', 'right')
        self.setWatchKey('control-d', 'turnRight', 'right')
        self.setWatchKey('alt-arrow_right', 'turnRight', 'right')
        self.setWatchKey('alt-d', 'turnRight', 'right')
        self.setWatchKey('shift-arrow_right', 'turnRight', 'right')
        self.setWatchKey('shift-d', 'turnRight', 'right')
        self.setWatchKey('control', 'jump', 'control')
        base.taskMgr.add(self.handleMovement, 'controlManager')

    def setupToon(self):
        self.localAvatar.setName('Toon')
        self.localAvatar.setPythonTag('Avatar', self)
        geom = self.localAvatar.getGeomNode()
        geom.getChild(0).setSx(0.730000019073)
        geom.getChild(0).setSz(0.730000019073)
        base.localAvatar = self.localAvatar
        wallBitmask = BitMask32(1)
        floorBitmask = BitMask32(2)
        base.cTrav = CollisionTraverser()
        walkControls = GravityWalker(legacyLifter=True)
        walkControls.setWallBitMask(wallBitmask)
        walkControls.setFloorBitMask(floorBitmask)
        walkControls.setWalkSpeed(8.0, 20.0, 4.0, 20.0)
        walkControls.initializeCollisions(base.cTrav, self.localAvatar, floorOffset=0.025, reach=4.0)
        walkControls.setAirborneHeightFunc(self.getAirborneHeight)
        walkControls.enableAvatarControls()
        self.walkControls = walkControls
        self.localAvatar.physControls = walkControls
        self.localAvatar.physControls.placeOnFloor()
        self.setupPhysics()
        Hud(self)
        self.setupCamera()
        render.getPythonTag('WorldCollisions').addToonCollision()
        
    def setCurrentGag(self, gagName):
        self.currentGag = gagName
        
    def getCurrentGag(self):
        return self.currentGag
    
    def updateLaffMeter(self):
        self.laffMeter.adjustFace(self.hp, self.maxHp, quietly = 0)