from direct.showbase.DirectObject import DirectObject
from direct.directnotify import DirectNotifyGlobal
from doomsday.mgrs.SceneManager import SceneManager
from doomsday.mgrs.DropManager import DropManager
from doomsday.world.MakeAToon import ToonCreator
from doomsday.round.Round import Round
from doomsday.world.WorldCollisions import WorldCollisions
from panda3d.core import AntialiasAttrib

class GameWorld(DirectObject):
    __module__ = __name__
    
    notify = DirectNotifyGlobal.directNotify.newCategory('GameWorld')
    
    def __init__(self):
        render.setPythonTag('Round', Round())
        render.setPythonTag('SceneManager', SceneManager())
        render.setPythonTag('WorldCollisions', WorldCollisions())
        render.setPythonTag('DropManager', DropManager())
        render.setAntialias(AntialiasAttrib.MAuto)
        render.attachNewNode("Cogs")
        render.attachNewNode("Barrels")
        ToonCreator()
        from doomsday.world.Intro import Intro
        #Intro()