from direct.showbase.ShowBase import ShowBase
from doomsday.world.GameWorld import GameWorld
from panda3d.core import loadPrcFile
from pandac.PandaModules import loadPrcFileData


loadPrcFile('../../config/Config.prc')
loadPrcFileData('', 'hardware-animated-vertices 1')

from direct.directnotify.DirectNotifyGlobal import directNotify

class GameStart(ShowBase):
    __module__ = __name__
    notify = directNotify.newCategory('GameStart')
    debug = False
    fps = False
    
    def __init__(self):
        ShowBase.__init__(self)
        
        if(self.debug):
            loadPrcFileData('', 'want-pstats 1')
            self.notify.warning('Debug Mode enabled.')
            base.startDirect()
        if(self.fps):
            base.setFrameRateMeter(True)
        base.camera.setPos(0, -15, 3)
        base.disableMouse()
        GameWorld()
launch = GameStart()
launch.run()