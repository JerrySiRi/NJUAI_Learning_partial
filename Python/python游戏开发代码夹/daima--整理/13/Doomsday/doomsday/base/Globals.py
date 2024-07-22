from panda3d.core import *

# 碰撞BitMasks
WallBitmask = BitMask32.bit(1)
FloorBitmask = BitMask32.bit(2)
DoorBitmask = BitMask32.bit(3)
GagBitmask = BitMask32.bit(4)
DropBitmask = BitMask32.bit(5)
ProjBitmask = BitMask32.bit(6)

LARGE_BEAN_AMT = 20
THROW_COLOR = VBase3(255 / 255.0, 145 / 255.0, 66 / 255.0)

#声音
clickSound = None
rlvrSound = None

def getClickSound():
    clickSound = loader.loadSfx('phase_3/audio/sfx/GUI_click.ogg')
    return clickSound

def getRlvrSound():
    rlvrSound = loader.loadSfx('phase_3/audio/sfx/GUI_rollover.ogg')
    return rlvrSound    

def getFont(name):
    return loader.loadFont("phase_3/models/fonts/%s" % (name))