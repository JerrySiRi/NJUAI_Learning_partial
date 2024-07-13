from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectButton import DirectButton
from direct.gui.DirectWaitBar import DirectWaitBar
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectWaitBar import DGG
from panda3d.core import *
from direct.task.Task import Task
from doomsday.cog.Cogs import Cogs
from doomsday.gui.DDDialog import GlobalDialog
from Data import Data
import Globals, copy


class Hud(DirectObject):
    
    throwExpLbl = None
    
    def __init__(self, avatar):
        self.avatar = avatar
        self.setupHud()
        render.setPythonTag("Hud", self)
        #GlobalDialog(message = "You're a gay idiot.", doneEvent = "sjdkfa", style = 1)
        
    def showMessage(self):
        ImpressBT = Globals.getFont('ImpressBT.ttf')
        saveTxt = OnscreenText(text = 'Successfully saved game!', pos = (0.025, 0.5), 
                               font = ImpressBT, fg = (1, 0, 0, 1), scale = (0.08, 0.08, 0.08))
        base.taskMgr.doMethodLater(0.8, self.removeText, 'Remove Save TXT', extraArgs = [saveTxt], appendTask = True)
        
    def removeText(self, text, task):
        text.removeNode()
        return Task.done
    
    def showWaveInformation(self):
        round = render.getPythonTag("Round")
        next_wave = round.getNextWave()
        icon = None
        if next_wave.getInvasion() == None:
            icon = loader.loadModel("phase_3/models/gui/cog_icons.bam").find('**/cog')
        else:
            degrees = [0, 90, 180, 270, 360, -90, -180, -270, -360]
            icon = Cogs().getCogHead(next_wave.getInvasion().getCogName())
            x = -1
            for degree in degrees:
                pass
            """
                head = copy.copy(icon)
                head.lookAt(0, 280, 0)
                head.reparentTo(aspect2d)
                head.setScale(0.2)
                head.setX(x)
                x+=0.2
             """
        #icon.reparentTo(aspect2d)
        #icon.setScale(0.2)
        #icon.setPos(0, 20, 0)
        
    def setupHud(self):
        btnSrc = loader.loadModel('phase_3/models/gui/quit_button.bam')
        ImpressBT = Globals.getFont('ImpressBT.ttf')
        btnSrcUP = btnSrc.find('**/QuitBtn_UP')
        btnSrcDN = btnSrc.find('**/QuitBtn_DN')
        btnSrcRlvr = btnSrc.find('**/QuitBtn_RLVR')
        DirectButton(clickSound = Globals.getClickSound(), 
            rolloverSound = Globals.getRlvrSound(), geom = (btnSrcUP, btnSrcDN, btnSrcRlvr),
            relief = None, pos = (1.12, 0, -0.95), command = self.saveGame)
        OnscreenText(text = 'Save', pos = (1.12325, -0.97), font = ImpressBT)
        DirectButton(clickSound = Globals.getClickSound(), 
            rolloverSound = Globals.getRlvrSound(), geom = (btnSrcUP, btnSrcDN, btnSrcRlvr),
            relief = None, pos = (1.12, 0, -0.85), command = self.spawnCogs)
        OnscreenText(text = 'Spawn Cogs', pos = (1.12325, -0.87), font = ImpressBT)
        self.showWaveInformation()
        
    def drawEXPBar(self):
        self.throwExp = DirectWaitBar(relief=DGG.SUNKEN, frameSize=(-1,
             1,
             -0.15,
             0.15), borderWidth=(0.02, 0.02), scale=0.25, frameColor=(Globals.THROW_COLOR[0] * 0.7,
             Globals.THROW_COLOR[1] * 0.7,
             Globals.THROW_COLOR[2] * 0.7,
             1), barColor=(Globals.THROW_COLOR[0],
            Globals.THROW_COLOR[1],
             Globals.THROW_COLOR[2],
             1), pos=(0, 0, -0.8))
        self.throwExpLbl = OnscreenText(parent = self.throwExp, 
                    pos =(0, -0.05), scale = 0.18, fg = (0, 0, 0, 1), mayChange = 1, align = TextNode.ACenter)
        
    
    def updateEXPBar(self, levelMgr):
        exp = levelMgr.getEXP()
        neededEXP = levelMgr.getEXPToNextLevel()
        level = levelMgr.getLevel()
        if(self.throwExpLbl == None):
            self.drawEXPBar()
        if not neededEXP == 0:
            value = ((float(exp) / float(neededEXP)) * 100)
        else:
            value = 0
        self.throwExp.update(value)
        if(level != levelMgr.getMaxLevel()):
            self.throwExpLbl.setText("%s/%s" % (exp, neededEXP))
        else:
            self.throwExpLbl.setText("%s/MAX" % (exp))

    def spawnCogs(self):
        render.getPythonTag('Round').startWave()
    
    def saveGame(self):
        self.showMessage()
        data = Data()
        data.saveGame()
        
        
