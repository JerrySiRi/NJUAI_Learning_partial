from direct.showbase.DirectObject import DirectObject
from direct.task.Task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence, Wait
from pandac.PandaModules import Vec4
from panda3d.core import *
from doomsday.world.ToonHall import ToonHall

class ToontownCentral(DirectObject):
    
    def __init__(self):
        self.scene = render.getPythonTag('SceneManager').createScene("TTC")
        self.build()
        
    def build(self):
        self.skybox = loader.loadModel("phase_3.5/models/props/TT_sky.bam")
        self.skybox.set_depth_write(False)
        self.skybox.find("**/Sky").setBin("background", 0)
        self.skybox.find('**/cloud1').setBin("background", 3)
        self.skybox.find('**/cloud2').setBin("background", 5)
        self.skybox.reparentTo(render)
        self.environ = loader.loadModel('ttc.bam')
    
    def __animateEnv(self):
        TTC = self.environ
        toonHall = TTC.find('**/sz13:toon_landmark_TT_toonhall_DNARoot')
        render.setPythonTag("ToonHall", ToonHall(toonHall, toonHall.find('**/door_double_round_ur')))
        phase_4 = 'phase_4/models/props/'
        self.fish = TTC.find('**/animated_prop_PetShopFishAnimatedProp_DNARoot')
        self.fish.removeNode()
        self.fish = Actor(phase_4 + 'exteriorfish-zero.bam', {'anim' : phase_4 + 'exteriorfish-swim.bam'})
        self.fish.reparentTo(TTC.find('**/sz22:toon_landmark_TT_pet_shop_DNARoot'))
        self.fish.loop('anim')
        self.periscope = Actor(TTC.find('**/animated_prop_HQPeriscopeAnimatedProp_DNARoot'), copy = 0)
        self.periscope.reparentTo(render)
        self.periscope.loadAnims({'anim': 'phase_3.5/models/props/HQ_periscope-chan.bam'})
        self.periscope.pose('anim', 0)
        self.periscopeTrack = Sequence(Wait(2.0), self.periscope.actorInterval('anim', startFrame=0, endFrame=40), Wait(0.7), self.periscope.actorInterval('anim', startFrame=40, endFrame=90), Wait(0.7), self.periscope.actorInterval('anim', startFrame=91, endFrame=121), Wait(0.7), self.periscope.actorInterval('anim', startFrame=121, endFrame=91), Wait(0.7), self.periscope.actorInterval('anim', startFrame=90, endFrame=40), Wait(0.7), self.periscope.actorInterval('anim', startFrame=40, endFrame=90), Wait(0.7), self.periscope.actorInterval('anim', startFrame=91, endFrame=121), Wait(0.5), self.periscope.actorInterval('anim', startFrame=121, endFrame=148), Wait(3.0))
        self.periscopeTrack.loop()
        self.telescope = Actor(TTC.find('**/animated_prop_HQTelescopeAnimatedProp_DNARoot'), copy = 0)
        self.telescope.reparentTo(render)
        self.telescope.loadAnims({'anim': 'phase_3.5/models/props/HQ_telescope-chan.bam'})
        self.telescope.pose('anim', 0)
        self.telescopeTrack = Sequence(Wait(5.0), self.telescope.actorInterval('anim', startFrame=0, endFrame=32), Wait(0.5), self.telescope.actorInterval('anim', startFrame=32, endFrame=78), Wait(0.5), self.telescope.actorInterval('anim', startFrame=79, endFrame=112), Wait(0.5), self.telescope.actorInterval('anim', startFrame=112, endFrame=79), Wait(0.5), self.telescope.actorInterval('anim', startFrame=78, endFrame=32), Wait(0.5), self.telescope.actorInterval('anim', startFrame=32, endFrame=78), Wait(0.5), self.telescope.actorInterval('anim', startFrame=79, endFrame=112), Wait(0.5), self.telescope.actorInterval('anim', startFrame=112, endFrame=148), Wait(4.0))
        self.telescopeTrack.loop()
        #base.taskMgr.add(self.__moveClouds, "Move Clouds")
        self.__fixTrashcans()
        self.environ.flattenStrong()
        self.scene.addModel(self.environ)
        render.find('**/TTC').setPythonTag('Class', self)
        
    def __fixTrashcans(self):
        TTC = self.environ
        trashcans = TTC.findAllMatches('**/prop_trashcan_metal_DNARoot')
        for trashcan in trashcans:
            pos = trashcan.getPos()
            hpr = trashcan.getHpr()
            trashcan.removeNode()
            new_trashcan = loader.loadModel('phase_5/models/props/trashcan_TT.bam')
            new_trashcan.setPos(pos)
            new_trashcan.setHpr(hpr)
            new_trashcan.reparentTo(TTC)
        
        
    def __moveClouds(self, task):
        model = self.skybox
        model.find("**/cloud1").setHpr(task.time * 0.3, 0, 0)
        model.find("**/cloud2").setHpr(task.time * -0.3, 0, 0) 
        return Task.cont
        
    def doFade(self):
        TTC = render.find('**/TTC')
        skyFade = self.skybox.colorScaleInterval(4, Vec4(0.1, 0.1, 0.1, 1), startColorScale=Vec4(1, 1, 1, 1), blendType='easeInOut')
        TTCFade = TTC.colorScaleInterval(3.8, Vec4(0.2509803921568627, 0.2509803921568627, 0.2509803921568627, 1), startColorScale=Vec4(1, 1, 1, 1), blendType='easeInOut')
        skyFade.start()
        TTCFade.start()
        
    def loadScene(self):
        self.scene.loadScene()
        self.__animateEnv()
        
    def unloadScene(self):
        base.taskMgr.remove("Move Clouds")
        self.scene.delete()