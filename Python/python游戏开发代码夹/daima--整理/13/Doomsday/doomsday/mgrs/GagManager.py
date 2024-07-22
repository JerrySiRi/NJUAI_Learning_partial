from direct.showbase.DirectObject import DirectObject
from doomsday.gags.WeddingCake import WeddingCake
from doomsday.gags.BirthdayCake import BirthdayCake
from doomsday.gags.WholeCreamPie import WholeCreamPie
from doomsday.gags.WholeFruitPie import WholeFruitPie
from doomsday.gags.CreamPieSlice import CreamPieSlice
from doomsday.gags.FruitPieSlice import FruitPieSlice
from doomsday.gags.Cupcake import Cupcake
from doomsday.mgrs.LevelManager import LevelManager
from panda3d.core import VBase4

tartColor = VBase4(55.0 / 255.0, 40.0 / 255.0, 148.0 / 255.0, 1.0)
creamColor = VBase4(250.0 / 255.0, 241.0 / 255.0, 24.0 / 255.0, 1.0)
cakeColor = VBase4(253.0 / 255.0, 119.0 / 255.0, 220.0 / 255.0, 1.0)

class GagManager(DirectObject):
    
    def __init__(self):
        self.gags = {
           'Cupcake' : Cupcake(4, 6, 5, 0.3, tartColor),
           'Fruit Pie Slice' : FruitPieSlice(8, 10, 25, 0.5, tartColor),
           'Cream Pie Slice' : CreamPieSlice(14, 17, 50, 0.5, creamColor),
           'Whole Fruit Pie' : WholeFruitPie(24, 27, 75, 0.7, tartColor),
           'Whole Cream Pie' : WholeCreamPie(36, 40, 1000, 0.7, creamColor),
           'Birthday Cake' : BirthdayCake(48, 100, 77, 0.9, cakeColor),
           'Wedding Cake' : WeddingCake(120000000, 1200000000, 100, 0.9, cakeColor)
        }
        LevelManager(self)
        
    def getGags(self):
        return self.gags
        
    def getGagByName(self, gagName):
        return self.gags.get(gagName)