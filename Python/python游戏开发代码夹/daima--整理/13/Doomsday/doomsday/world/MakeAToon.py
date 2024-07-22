from direct.showbase.DirectObject import DirectObject
from direct.directnotify import DirectNotifyGlobal
from direct.showbase.Transitions import Transitions
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectButton import DirectButton
from direct.task.Task import Task
from doomsday.avatar.Avatar import Avatar
from doomsday.avatar.AvatarAttributes import AvatarAttributes
from doomsday.base import Globals, SoundBank
from doomsday.world.ToontownCentral import ToontownCentral
import random

class ToonCreator(DirectObject):
    __module__ = __name__
    
    notify = DirectNotifyGlobal.directNotify.newCategory("ToonCreator")
    
    dataCache = {
      'Animal' : None,
      'Gender' : None,
      'Weight' : None,
      'Height' : None,
      'Color' : None,
      'HeadType' : None,
      'HeadLength' : None,
      'Shirt' : None,
      'Bottoms' : None
    }
    
    avatar = Avatar()
    subject = None
    
    def __init__(self):
        self.trans = Transitions(loader)
        self.scene = render.getPythonTag('SceneManager').createScene('Make-A-Toon')
        self.setupEnvironment()
        self.randomizeData()
        self.setupHUD()
        self.bgm = SoundBank.getSound('make_a_toon')
        self.bgm.setLoop(True)
        self.bgm.play()
        
    def setupHUD(self):
        gui1 = loader.loadModel('phase_3/models/gui/create_a_toon_gui.bam')
        gui2 = loader.loadModel('phase_3/models/gui/gui_toongen.bam')
        mickeyFont = loader.loadFont('MickeyFont.bam')
        self.guiElements = [
            OnscreenImage(image = gui1.find("**/CrtATn_TopBar"), parent=render2d, pos=(0, 0, 0.9), scale=(0.85, 0.85, 1)),
            OnscreenText(text = "Make Your Toon", pos = (0, 0.85), font = mickeyFont, fg = (1, 0, 0, 1),
                scale=(0.2, 0.2, 0.2)),
            DirectButton(clickSound=Globals.getClickSound(), rolloverSound=Globals.getRlvrSound(), geom = (gui1.find("**/CrtATn_R_Arrow_UP"), gui1.find("**/CrtATn_R_Arrow_DN"), gui1.find("**/CrtATn_R_Arrow_RLVR")), pos=(0.66, 0, 0.4), relief=None, command=self.setData, extraArgs=['Animal', 'prev']),
            DirectButton(clickSound=Globals.getClickSound(), rolloverSound=Globals.getRlvrSound(), geom = (gui1.find("**/CrtATn_R_Arrow_UP"), gui1.find("**/CrtATn_R_Arrow_DN"), gui1.find("**/CrtATn_R_Arrow_RLVR")), pos=(0, 0, 0.41), hpr=(0, 0, 180), command=self.setData, extraArgs=['Animal', 'next'], relief=None),
            OnscreenText(text = "Animal", pos = (0.325, 0.38), font = mickeyFont, fg = (1, 0, 0, 1), scale=(0.08, 0.08, 0.08)),
            DirectButton(clickSound=Globals.getClickSound(), rolloverSound=Globals.getRlvrSound(), geom = (gui1.find("**/CrtATn_R_Arrow_UP"), gui1.find("**/CrtATn_R_Arrow_DN"), gui1.find("**/CrtATn_R_Arrow_RLVR")), pos=(0.66, 0, 0.1), relief=None, command=self.setData, extraArgs=['Weight', 'prev']),
            DirectButton(clickSound=Globals.getClickSound(), rolloverSound=Globals.getRlvrSound(), geom = (gui1.find("**/CrtATn_R_Arrow_UP"), gui1.find("**/CrtATn_R_Arrow_DN"), gui1.find("**/CrtATn_R_Arrow_RLVR")), pos=(0, 0, 0.11), hpr=(0, 0, 180), command=self.setData, extraArgs=['Weight', 'next'], relief=None),
            OnscreenText(text = "Body", pos = (0.325, 0.1), font = mickeyFont, fg = (1, 0, 0, 1), scale=(0.08, 0.08, 0.08)),
            DirectButton(clickSound=Globals.getClickSound(), rolloverSound=Globals.getRlvrSound(), geom = (gui1.find("**/CrtATn_R_Arrow_UP"), gui1.find("**/CrtATn_R_Arrow_DN"), gui1.find("**/CrtATn_R_Arrow_RLVR")), pos=(0.66, 0, -0.20), relief=None, command=self.setData, extraArgs=['Height', 'prev']),
            DirectButton(clickSound=Globals.getClickSound(), rolloverSound=Globals.getRlvrSound(), geom = (gui1.find("**/CrtATn_R_Arrow_UP"), gui1.find("**/CrtATn_R_Arrow_DN"), gui1.find("**/CrtATn_R_Arrow_RLVR")), pos=(0, 0, -0.19), hpr=(0, 0, 180), command=self.setData, extraArgs=['Height', 'next'], relief=None),
            OnscreenText(text = "Height", pos = (0.325, -0.2), font = mickeyFont, fg = (1, 0, 0, 1), scale=(0.08, 0.08, 0.08)),
            DirectButton(clickSound=Globals.getClickSound(), rolloverSound=Globals.getRlvrSound(), geom = (gui1.find("**/CrtATn_R_Arrow_UP"), gui1.find("**/CrtATn_R_Arrow_DN"), gui1.find("**/CrtATn_R_Arrow_RLVR")), pos=(0.66, 0, -0.50), relief=None, command=self.setData, extraArgs=['HeadType', 'prev']),
            DirectButton(clickSound=Globals.getClickSound(), rolloverSound=Globals.getRlvrSound(), geom = (gui1.find("**/CrtATn_R_Arrow_UP"), gui1.find("**/CrtATn_R_Arrow_DN"), gui1.find("**/CrtATn_R_Arrow_RLVR")), pos=(0, 0, -0.49), hpr=(0, 0, 180), command=self.setData, extraArgs=['HeadType', 'next'], relief=None),
            OnscreenText(text = "Head", pos = (0.325, -0.5), font = mickeyFont, fg = (1, 0, 0, 1), scale=(0.08, 0.08, 0.08)),
            DirectButton(clickSound=Globals.getClickSound(), rolloverSound=Globals.getRlvrSound(), geom = (gui1.find("**/CrtATn_R_Arrow_UP"), gui1.find("**/CrtATn_R_Arrow_DN"), gui1.find("**/CrtATn_R_Arrow_RLVR")), pos=(0.66, 0, -0.8), relief=None, command=self.setData, extraArgs=['Color', 'prev']),
            DirectButton(clickSound=Globals.getClickSound(), rolloverSound=Globals.getRlvrSound(), geom = (gui1.find("**/CrtATn_R_Arrow_UP"), gui1.find("**/CrtATn_R_Arrow_DN"), gui1.find("**/CrtATn_R_Arrow_RLVR")), pos=(0, 0, -0.79), hpr=(0, 0, 180), command=self.setData, extraArgs=['Color', 'next'], relief=None),
            OnscreenText(text = "Length", pos = (0.328, -0.67), font = mickeyFont, fg = (1, 0, 0, 1), scale=(0.08, 0.08, 0.08)),
            DirectButton(clickSound=Globals.getClickSound(), rolloverSound=Globals.getRlvrSound(), geom = (gui1.find("**/CrtATn_R_Arrow_UP"), gui1.find("**/CrtATn_R_Arrow_DN"), gui1.find("**/CrtATn_R_Arrow_RLVR")), pos=(0.57, 0, -0.65), scale = 0.4, relief=None, command=self.setData, extraArgs=['HeadLength', 'short']),
            DirectButton(clickSound=Globals.getClickSound(), rolloverSound=Globals.getRlvrSound(), geom = (gui1.find("**/CrtATn_R_Arrow_UP"), gui1.find("**/CrtATn_R_Arrow_DN"), gui1.find("**/CrtATn_R_Arrow_RLVR")), pos=(0.11, 0, -0.64), scale = 0.4, hpr=(0, 0, 180), command=self.setData, extraArgs=['HeadLength', 'long'], relief=None),            
            OnscreenText(text = "Color", pos = (0.325, -0.8), font = mickeyFont, fg = (1, 0, 0, 1), scale=(0.08, 0.08, 0.08)),
            DirectButton(clickSound=Globals.getClickSound(), rolloverSound=Globals.getRlvrSound(), geom = (gui2.find("**/tt_t_gui_mat_girlUp"), gui2.find("**/tt_t_gui_mat_girlDown")), pos=(0.66, 0, 0.68), relief=None, command=self.randomizeData, extraArgs = ['girl'], scale=(0.55, 0.55, 0.55)),
            DirectButton(clickSound=Globals.getClickSound(), rolloverSound=Globals.getRlvrSound(), geom = (gui2.find("**/tt_t_gui_mat_boyUp"), gui2.find("**/tt_t_gui_mat_boyDown")), pos=(0, 0, 0.68), command=self.randomizeData, extraArgs = ['boy'], relief=None, scale=(0.55, 0.55, 0.55)),
            DirectButton(clickSound=Globals.getClickSound(), rolloverSound=Globals.getRlvrSound(), geom=(gui2.find("**/tt_t_gui_mat_okUp"), gui2.find("**/tt_t_gui_mat_okDown")), pos=(1, 0, -0.2), relief=None, command=self.done)
        ] 
        
    def done(self):
        self.trans.irisOut()
        self.bgm.stop()
        for element in self.guiElements:
            element.removeNode()
        base.taskMgr.doMethodLater(0.8, self.cleanUp, 'Cleanup Scene')
        
    def cleanUp(self, task):
        self.bgm.stop()
        self.scene.delete()
        ToontownCentral().loadScene()
        self.trans.irisIn()
        from doomsday.avatar.LocalAvatar import Player
        Player(self.avatar).setupToon()
        return Task.done
        
    def setData(self, key, value):
        attr = AvatarAttributes()
        tables = {'Animal' : attr.getAnimals(), 
                  'Gender' : ['boy', 'girl'],
                  'Color' : attr.convertColorDictToTbl(),
                  'Weight' : attr.getWeights(),
                  'Height' : attr.getHeights(),
                  'HeadType' : attr.getHeadTypes(),
                  'HeadLength' : ['short', 'long']}
        if(key not in self.dataCache):
            return
        if(value == 'prev' or value == 'next'):
            table = tables[key]
            index = 0
            for i in range(len(table)):
                if(table[i] == self.dataCache[key]):
                    index = i
            if(value == 'prev'):
                if(index == 0):
                    self.dataCache[key] = table[(len(table) - 1)]
                else:
                    self.dataCache[key] = table[index - 1]
            else:
                if(index == (len(table) - 1)):
                    self.dataCache[key] = table[0]
                else:
                    self.dataCache[key] = table[index + 1]
        else:
            self.dataCache[key] = value
        self.generateAvatar()
            
        
    def randomizeData(self, gender = None):
        def setData(key, value):
            self.dataCache[key] = value
        
        attr = AvatarAttributes()
        setData('Animal', random.choice(attr.getAnimals()))
        if(gender == None):
            setData('Gender', random.choice(['boy', 'girl']))
        else:
            setData('Gender', gender)
        setData('Weight', random.choice(attr.getWeights()))
        setData('Height', random.choice(attr.getHeights()))
        setData('Color', random.choice(attr.convertColorDictToTbl()))
        setData('HeadType', random.choice(attr.getHeadTypes()))
        setData('HeadLength', random.choice(['short', 'long']))
        self.generateAvatar()
    
    def generateAvatar(self):
        self.cleanupAvatar()
        for key in self.dataCache.keys():
            self.avatar.setData(key, self.dataCache[key])
        self.avatar.generate()
        self.avatar.getAvatar().setPosHprScale(-2, 0, 0, 200, 0, 0, 1, 1, 1)
        self.avatar.getAvatar().reparentTo(render)
        self.subject = self.avatar.getAvatar()
        self.subject.setName("Temp Toon")
        self.subject.loop('neutral')
        shirtColor = random.choice(AvatarAttributes().convertColorDictToTbl())
        bttColor = random.choice(AvatarAttributes().convertColorDictToTbl())
        self.subject.find("**/torso-top").setColor(shirtColor)
        self.subject.find("**/sleeves").setColor(shirtColor)
        self.subject.find('**/torso-bot').setColor(bttColor)
    
    def cleanupAvatar(self):
        if(self.subject != None):
            self.subject.stop('neutral')
            self.subject.cleanup()
            self.subject.removeNode()
        
    def setupEnvironment(self):
        self.trans.fadeIn(2)
        room = loader.loadModel('phase_3/models/gui/create_a_toon.bam')
        room.find('**/sewing_machine').removeNode()
        room.find('**/drafting_table').removeNode()
        room.find("**/wall_floor").setColor(0.7294117647058824, 0.5490196078431373, 0.2392156862745098, 1)
        room.setName("Room")
        self.scene.addModel(room)