from direct.directnotify import DirectNotifyGlobal
from direct.showbase.DirectObject import DirectObject
from panda3d.core import Vec4

animals = ['cat', 'dog', 'duck', 'mouse', 'pig', 'rabbit', 'bear', 'horse', 'monkey']
colors = {
    'white' : Vec4(1.0, 1.0, 1.0, 1.0),
    'peach' : Vec4(0.96875, 0.691406, 0.699219, 1.0),
    'bright red' : Vec4(0.933594, 0.265625, 0.28125, 1.0),
    'red' : Vec4(0.863281, 0.40625, 0.417969, 1.0),
    'maroon' : Vec4(0.710938, 0.234375, 0.4375, 1.0),
    'sienna' : Vec4(0.570312, 0.449219, 0.164062, 1.0),
    'brown' : Vec4(0.640625, 0.355469, 0.269531, 1.0),
    'tan' : Vec4(0.996094, 0.695312, 0.511719, 1.0),
    'coral' : Vec4(0.832031, 0.5, 0.296875, 1.0),
    'orange' : Vec4(0.992188, 0.480469, 0.167969, 1.0),
    'yellow' : Vec4(0.996094, 0.898438, 0.320312, 1.0),
    'cream' : Vec4(0.996094, 0.957031, 0.597656, 1.0),
    'citrine' : Vec4(0.855469, 0.933594, 0.492188, 1.0),
    'lime green' : Vec4(0.550781, 0.824219, 0.324219, 1.0),
    'sea green' : Vec4(0.242188, 0.742188, 0.515625, 1.0),
    'green' : Vec4(0.304688, 0.96875, 0.402344, 1.0),
    'light blue' : Vec4(0.433594, 0.90625, 0.835938, 1.0),
    'aqua' : Vec4(0.347656, 0.820312, 0.953125, 1.0),
    'blue' : Vec4(0.191406, 0.5625, 0.773438, 1.0),
    'periwinkle' : Vec4(0.558594, 0.589844, 0.875, 1.0),
    'royal blue' : Vec4(0.285156, 0.328125, 0.726562, 1.0),
    'slate blue' : Vec4(0.460938, 0.378906, 0.824219, 1.0),
    'purple' : Vec4(0.546875, 0.28125, 0.75, 1.0),
    'lavender' : Vec4(0.726562, 0.472656, 0.859375, 1.0),
    'pink' : Vec4(0.898438, 0.617188, 0.90625, 1.0)
}

class AvatarAttributes(DirectObject):
    __module__ = __name__
    
    notify = DirectNotifyGlobal.directNotify.newCategory('AvatarAttributes')
    
    def convertColorDictToTbl(self):
        colorsTbl = []
        for color in colors.values():
            colorsTbl.append(color)
        return colorsTbl
    
    def getAnimals(self):
        return animals
    
    def getHeadTypes(self, animal = None):
        return [250, 500, 1000]
    
    def getWeights(self):
        return ['skinny', 'stubby', 'fat']
    
    def getHeights(self):
        return ['short', 'medium', 'tall']
    
    def getColors(self):
        return colors
    
    def getColor(self, color):
        return colors[color]
        