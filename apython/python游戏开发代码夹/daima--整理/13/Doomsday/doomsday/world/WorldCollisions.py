from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import CollisionHandlerEvent, CollisionHandlerQueue, CollisionHandlerFloor, CollisionHandlerPusher, CollisionNode, CollisionTube, CollisionSphere, CollisionRay, CollisionTraverser, BitMask32
from doomsday.base import Globals, SoundBank
from doomsday.world.Splat import Splat
from panda3d.core import Vec4, Vec3
import math

collHdl = CollisionHandlerEvent()
collHdlF = CollisionHandlerFloor()
collHdlF.setMaxVelocity(8)
collHdlPush = CollisionHandlerPusher()

class WorldCollisions(DirectObject):
    
    def __init__(self):
        base.cTrav = CollisionTraverser()
        self.called = False
        
    def handleInCollisions(self, entry):
        cogCollNames = ['coll_body', 'coll_crit']
        intoNode = entry.getIntoNodePath()
        fromNode = entry.getFromNodePath()
        if(self.called):
            return
        self.called = True
        splatColor = Vec4(0.7, 0.7, 0.8, 1.0)
        splatScale = 0.7
        if(intoNode.getName() in cogCollNames):
            cog = intoNode.getParent().getPythonTag('Cog')
            gag = fromNode.getParent().getPythonTag('Stats')
            splatColor = gag.getSplatColor()
            splatScale = gag.getSplatScale()
            if not cog.wasHit():
                cog.setHit(True)
                if(cog.getLevel() > 1):
                    exp = int(math.ceil(float(cog.getLevel()) / 2.0) * gag.getLevel())
                else:
                    exp = int(gag.getLevel())
                render.getPythonTag("LevelManager").addEXP(exp)
                dmg = gag.getDamageCurve()[0]
                if(intoNode.getName() == cogCollNames[1]):
                    dmg = (dmg * 2) * 0.4
                cog.setHealth(cog.getHealth() - int(dmg))
                if(cog.getHealth() <= 0):
                    maxHp = float((cog.getLevel() + 1) * (cog.getLevel() + 2))
                    if(cog.getHealth() <= (-1 * (maxHp * 0.2))):
                        h = cog.getCog().getHpr(fromNode.getParent()).getX()
                        if(h > 0 and h < 90 or h < 270 and h > 0):
                            cog.getCog().play('slip-backward')
                        else:
                            cog.getCog().play('slip-forward')
                    else:
                        cog.getCog().play('pie-small')
        SoundBank.getSound('pie_coll').play()
        Splat(fromNode.getParent().getPos(), splatColor, splatScale).generate()
        fromNode.getParent().removeNode()
        
    def completeCollision(self, entry):
        self.called = False
        cogCollNames = ['coll_body', 'coll_crit']
        intoNode = entry.getIntoNodePath()
        if(intoNode.getName() in cogCollNames):
            if not intoNode.isEmpty():
                cog = intoNode.getParent().getPythonTag('Cog')
                if(cog != None):
                    cog.setHit(False)
            
    def handleDropCollision(self, entry):
        intoNode = entry.getIntoNodePath()
        fromNode = entry.getFromNodePath()
        if(intoNode.getName() == 'coll_toon'):
            if(fromNode.getName() == 'coll_drop'):
                fromNode.getParent().getPythonTag('Drop').execute()
                
    def handleAttackCollision(self, entry):
        intoNode = entry.getIntoNodePath()
        fromNode = entry.getFromNodePath()
        if(intoNode.getName() == 'coll_toon'):
            if(fromNode.getName() == 'coll_attack'):
                stats = fromNode.getParent().getPythonTag("Stats")
                avatar = intoNode.getParent().getPythonTag('Avatar')
                if(avatar.isHit() == False):
                    avatar.setHit(True)
                    avatar.setHealth(avatar.getHealth() - stats.getDamage())
                    if(fromNode.getParent().hasPythonTag("HitSound")):
                        SoundBank.getSound(fromNode.getParent().getPythonTag("HitSound")).play()
        fromNode.getParent().removeNode()
        
    def completeAttackCollision(self, entry):
        intoNode = entry.getIntoNodePath()
        avatar = intoNode.getParent().getPythonTag('Avatar')
        avatar.setHit(False)
        
    def addCogCollision(self, cog):
        ent = cog.getCog()
        head = cog.getHead()
        if(head != None):
            sphPos = cog.getHead().getZ(render) + 0.5
        else:
            sphPos = ent.find('**/joint_head').getPos(render).getZ() + 0.8        
        collTube = ent.attachNewNode(CollisionNode('coll_body'))
        collTube.node().addSolid(CollisionTube(0, 0, 0.5, 0, 0, cog.getHeight() - 2, 2))
        collTube.node().setIntoCollideMask(Globals.GagBitmask)
        collTube.node().setFromCollideMask(BitMask32.allOff())
        collSph = ent.attachNewNode(CollisionNode('coll_crit'))
        collSph.node().addSolid(CollisionSphere(0, 0, sphPos, 2))
        collSph.node().setIntoCollideMask(Globals.GagBitmask)
        base.cTrav.addCollider(collTube, collHdl)
        base.cTrav.addCollider(collSph, collHdl)
        
    def addCogGroundCollision(self, cog = None, ent = None):
        if ent == None:
            ent = cog.getCog()
        collGround = ent.attachNewNode(CollisionNode('coll_ground'))
        collGround.node().addSolid(CollisionRay(0, 0, 2, 0, 0, -1))
        collGround.node().setIntoCollideMask(BitMask32.allOff())
        collGround.node().setFromCollideMask(Globals.WallBitmask)
        collHdlF.addCollider(collGround, ent)
        base.cTrav.addCollider(collGround, collHdlF)
        
    def addAttackCollision(self, proj):
        collSph = proj.attachNewNode(CollisionNode('coll_attack'))
        collSph.node().addSolid(CollisionSphere(0, 0, 0, 1))
        collSph.node().setIntoCollideMask(BitMask32.allOff())
        collSph.node().setFromCollideMask(Globals.ProjBitmask)
        base.cTrav.addCollider(collSph, collHdl)
        self.accept("coll_attack-into", self.handleAttackCollision)
        self.accept("coll_attack-out", self.completeAttackCollision)
    
    def addToonCollision(self):
        toon = render.find('**/Toon')
        collTube = toon.attachNewNode(CollisionNode('coll_toon'))
        collTube.node().addSolid(CollisionTube(0, 0, 0.5, 0, 0, 8, 2))
        collTube.node().setIntoCollideMask(Globals.DropBitmask | Globals.ProjBitmask)
        collTube.node().setFromCollideMask(BitMask32.allOff())
        base.cTrav.addCollider(collTube, collHdl)
        
    def addDropCollision(self, drop):
        collSph = drop.attachNewNode(CollisionNode('coll_drop'))
        collSph.node().addSolid(CollisionSphere(0, 0, 0, 1))
        collSph.node().setIntoCollideMask(BitMask32.allOff())
        collSph.node().setFromCollideMask(Globals.DropBitmask)
        collGround = drop.attachNewNode(CollisionNode('coll_drop_ground'))
        collGround.node().addSolid(CollisionRay(0, 0, 0, 0, 0, -1))
        collGround.node().setIntoCollideMask(BitMask32.allOff())
        collGround.node().setFromCollideMask(Globals.WallBitmask)
        collGround.show()
        collHdlF.addCollider(collGround, drop)
        base.cTrav.addCollider(collSph, collHdl)
        base.cTrav.addCollider(collGround, collHdlF)
        self.accept("coll_drop-into", self.handleDropCollision)
        self.accept("coll_drop-out", self.completeCollision)
        
    def addGagCollision(self, gag):
        collNode = gag.attachNewNode(CollisionNode('coll_gag'))
        collNode.node().addSolid(CollisionSphere(0, 0, 0, 2))
        collNode.node().setIntoCollideMask(BitMask32.allOff())
        collNode.node().setFromCollideMask(Globals.GagBitmask | Globals.WallBitmask | Globals.FloorBitmask)
        base.cTrav.addCollider(collNode, collHdl)
        collHdl.addInPattern('%fn-into')
        collHdl.addOutPattern('%fn-out')
        self.accept("coll_gag-into", self.handleInCollisions)
        self.accept("coll_gag-out", self.completeCollision)
    