from os.path import join

import pyglet.resource
import os.path
from cocos import director
from cocos.scene import Scene
from cocos.layer import MultiplexLayer
from Menus import MainMenu


def main():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    pyglet.resource.path = [join(script_dir, '..')]
    pyglet.resource.reindex()
    director.director.init(width=800, height=650, caption="Match 3")
    scene = Scene()
    scene.add(MultiplexLayer(
        MainMenu()
    ),
        z=1)
    director.director.run(scene)

if __name__ == '__main__':
    main()
