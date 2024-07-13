from direct.showbase.DirectObject import DirectObject

class GagBarrel(DirectObject):
    
    gagImages = {
      'Cupcake' : 'inventory_cup_cake',
      'Fruit Pie Slice' : 'inventory_fruit_pie_slice',
      'Cream Pie Slice' : 'inventory_cream_pie_slice',
      'Whole Fruit Pie' : 'inventory_fruitpie',
      'Whole Cream Pie' : 'inventory_creampie',
      'Birthday Cake' : 'inventory_cake',
      'Wedding Cake' : 'inventory_wedding'
    }
    
    def __init__(self, gag, supply = 100):
        self.gag = gag
        self.supply = supply
        
    def generate(self):
        self.barrel = loader.loadModel("phase_4/models/cogHQ/gagTank.bam")
        self.barrel.setScale(0.5)
        label = self.barrel.find('**/gagLabelDCS')
        label.setColor(0.15, 0.15, 0.1)
        self.gagNode = self.barrel.attachNewNode('gagNode')
        self.gagNode.setPosHpr(0.0, -2.62, 4.0, 0, 0, 0)
        self.gagNode.setColorScale(0.7, 0.7, 0.6, 1)
        icon = self.getGagImage()
        icon.reparentTo(self.gagNode)
        icon.setPos(0, -0.1, 0)
        icon.setScale(13)
        self.barrel.setPythonTag('Stats', self)
        self.barrel.reparentTo(render.find('**/Barrels'))
        return self.barrel
    
    def getGag(self):
        return self.gag
        
    def getGagImage(self):
        imageName = self.gagImages[self.gag]
        icons = loader.loadModel('phase_3.5/models/gui/inventory_icons.bam')
        icon = icons.find('**/%s' % imageName)
        icons.removeNode()
        return icon
    
    def setSupply(self, supply):
        self.supply = supply
        if(self.supply != 0):
            color = float(self.supply) * 5.1
            self.barrel.setColorScale(color, color, color, 1)
            label = self.barrel.find('**/gagLabelDCS')
            label.setColor(0.15, 0.15, 0.1)
        else:
            self.barrel.setColorScale(0.5, 0.5, 0.5, 1)
        
    def getSupply(self):
        return self.supply