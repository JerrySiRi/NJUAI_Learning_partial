import cocos
from cocos.actions import *
from cocos.layer import *
from pyglet import gl


class BackgroundLayer(cocos.layer.Layer):
    def __init__(self):
        super(BackgroundLayer, self).__init__()
        self.img = pyglet.resource.image('background_image.png')

    def draw(self):
        gl.glColor4ub(255, 255, 255, 255)
        gl.glPushMatrix()
        self.transform()
        self.img.blit(0, 0)
        gl.glPopMatrix()


def main():
    print(description)
    director.init(resizable=True, fullscreen=False)
    main_scene = cocos.scene.Scene()
    main_scene.add(BackgroundLayer(), z=0)

    def check_grid(self):
        assert self.grid.active == False

    e = FadeOutBLTiles(grid=(16, 12), duration=2)
    # a sequence of grid actions should terminate with the action StopGrid,
    # else the scene will continue to do a double render for each frame
    main_scene.do(e + Reverse(e) + StopGrid() + CallFuncS(check_grid))

    director.run(main_scene)


description = """
演示Fadeoutmultiles特效，并在StopGrid之后验证
self.grid.active == False
"""

if __name__ == '__main__':
    main()
