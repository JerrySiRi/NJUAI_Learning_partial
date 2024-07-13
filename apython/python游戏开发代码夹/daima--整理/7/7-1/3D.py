import cocos
from cocos.actions import *
from cocos.layer import *
import pyglet
from pyglet import gl

class BackgroundLayer(cocos.layer.Layer):
    def __init__(self):
        super(BackgroundLayer, self).__init__()
        self.img = pyglet.resource.image('background_image.png')

    def draw( self ):
        gl.glColor4ub(255, 255, 255, 255)
        gl.glPushMatrix()
        self.transform()
        self.img.blit(0,0)
        gl.glPopMatrix()

def main():
    director.init( resizable=True )
    director.set_depth_test()

    main_scene = cocos.scene.Scene()

    main_scene.add( BackgroundLayer(), z=0 )

    #在实际应用中，在一系列网格操作之后，应该调用StopGrid()停止操作。
    main_scene.do( JumpTiles3D( jumps=2, amplitude=100, grid=(16,12), duration=4) )
    director.run (main_scene)

if __name__ == '__main__':
    main()
