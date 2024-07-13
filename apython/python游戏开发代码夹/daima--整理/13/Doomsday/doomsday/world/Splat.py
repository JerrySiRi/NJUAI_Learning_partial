from direct.showbase.DirectObject import DirectObject
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence, Func, Wait

class Splat(DirectObject):
    
    def __init__(self, pos, color, scale):
        self.pos = pos
        self.color = color
        self.scale = scale
        
    def generate(self):
        self.splat = Actor('phase_3.5/models/props/splat-mod.bam', {'chan' : 'phase_3.5/models/props/splat-chan.bam'})
        self.splat.setBillboardPointEye()
        self.splat.setColor(self.color)
        self.splat.setScale(self.scale)
        self.splat.setPos(self.pos)
        self.splat.play('chan')
        self.splat.reparentTo(render)
        Sequence(
          Wait(0.5),
          Func(self.destroy)
        ).start()
        
    def destroy(self):
        self.splat.cleanup()
        self.splat.removeNode()
        del self.splat
        del self
        
        
        