import cocos
from cocos.actions import *
from cocos.layer import *
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
    director.init( resizable=True, fullscreen=False )
    main_scene = cocos.scene.Scene()

    main_scene.add( BackgroundLayer(), z=0 )

    e = FadeOutTRTiles( grid=(16,12), duration=2 )
    # 一系列网格动作以StopGrid动作结束，否则场景将继续对每一帧进行双重渲染
    main_scene.do( e + Reverse(e) + StopGrid() )

    director.run (main_scene)

if __name__ == '__main__':
    main()
