from direct.showbase.DirectObject import DirectObject
from direct.task.Task import Task
from doomsday.shop.GagCannon import GagCannon
from doomsday.shop.GagBarrel import GagBarrel
import copy

class Cattlelog(DirectObject):
    
    def __init__(self):
        self.cattlelog = [
          PurchaseableItem('Gag Cannon', cost = 200, cls = GagCannon()),
          PurchaseableItem('Cupcake Supply Barrel', cost = 20, cls = GagBarrel('Cupcake')),
          PurchaseableItem('Fruit Pie Slice Supply Barrel', cost = 25, cls = GagBarrel('Fruit Pie Slice')),
          PurchaseableItem('Cream Pie Slice Supply Barrel', cost = 30, cls = GagBarrel('Cream Pie Slice')),
          PurchaseableItem('Whole Fruit Pie Supply Barrel', cost = 40, cls = GagBarrel('Whole Fruit Pie')),
          PurchaseableItem('Whole Cream Pie Supply Barrel', cost = 50, cls = GagBarrel('Whole Cream Pie')),
          PurchaseableItem('Birthday Cake Supply Barrel', cost = 75, cls = GagBarrel('Birthday Cake')),
          PurchaseableItem('Wedding Cake Supply Barrel', cost = 100, cls = GagBarrel('Wedding Cake'))
        ]
        
    def showItem(self, item):
        cls = item.getClass()
        name = item.getName()
        cost = item.getCost()
        preview = copy.copy(cls.generate())
        
class PurchaseableItem(DirectObject):
    
    def __init__(self, name, cost, cls):
        self.name = name
        self.cost = cost
        self.cls = cls
        
    def getName(self):
        return self.name
    
    def getCost(self):
        return self.cost
    
    def getClass(self):
        return self.cls