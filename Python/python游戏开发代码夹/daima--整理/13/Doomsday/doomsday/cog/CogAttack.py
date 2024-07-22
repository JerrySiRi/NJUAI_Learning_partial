from direct.showbase.DirectObject import DirectObject
from direct.actor.Actor import Actor
from direct.task.Task import Task
from direct.interval.IntervalGlobal import ProjectileInterval, Sequence, Wait, Func
from panda3d.core import Point3
from doomsday.base import SoundBank

class CogAttack(DirectObject):
    
    def __init__(self, cls, mdl, attackType, anim = None, hitSound = None, throwSound = None):
        self.cls = cls
        self.mdl = mdl
        self.anim = anim
        self.attackType = attackType
        self.hitSound = hitSound
        self.throwSound = throwSound
        
    def generate(self):
        if(self.attackType == 'throw'):
            if(self.anim == None):
                self.projectile = loader.loadModel(self.mdl)
            else:
                self.projectile = Actor(loader.loadModel(self.mdl), {'chan' : loader.loadModel(self.anim)})
            self.projectile.setName("Projectile")
            self.projectile.setPythonTag("Stats", self.cls)
            if(self.attackType == 'throw' and self.hitSound != None):
                self.projectile.setPythonTag("HitSound", self.hitSound)
            
    def execute(self, cog = None):
        if(self.attackType == 'throw'):
            if not self.projectile.isEmpty():
                ent = cog.getCog()
                ent.play('throw-object')
                handJoint = ent.find('**/joint_Rhold')
                self.projectile.reparentTo(handJoint)
                def destroy(att_range):
                    self.projectile.removeNode()
                    att_range.removeNode()
                    del self
                def releaseProj(task):
                    if(cog.getHealth() > 0):
                        attackRange = ent.find('**/joint_nameTag').attachNewNode("Attack Range")
                        attackRange.setPos(0, 50, -5)
                        self.projectile.setBillboardPointEye()
                        wc = render.getPythonTag('WorldCollisions')
                        wc.addAttackCollision(self.projectile)
                        self.projectile.reparentTo(render)
                        projTrack = ProjectileInterval(self.projectile, endPos = Point3(attackRange.getPos(render)), startPos = (handJoint.getPos(render)), gravityMult = 0.7, duration = 1)
                        projTrack.start()
                        if(self.throwSound != None):
                            SoundBank.getSound(self.throwSound).play()
                        ent.play('neutral')
                        Sequence(
                          Wait(2),
                          Func(destroy, range)
                        )
                    return Task.done
                base.taskMgr.doMethodLater(1.5, releaseProj, 'Release Projectile')  
            else:
                return 
        else:
            return