from cocos import scene
from cocos.layer import Layer
from cocos.director import director
from cocos.sprite import Sprite

class Actors(Layer):
    def __init__(self):
        super(Actors, self).__init__()
        # 创建了一个精灵对象，而不是文本。将精灵添加到对象中，而不是使其成为本地对象
        # 这样做的好处是可以在其他函数中访问它
        self.actor = Sprite('assets/img/grossini.png')
        # 然后把它添加到层中，类似于文本
        self.actor.position = 320, 240
        # 最后把它添加到图层中
        self.add(self.actor)

# 现在我初始化控制器并运行场景
director.init()
director.run(scene.Scene(Actors()))