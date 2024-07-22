import cocos
class LayerBlue(cocos.layer.ColorLayer):
    def __init__(self):
        super(LayerBlue, self).__init__(0, 128, 128, 255,
                                        width=120, height=80)
        self.position = (50, 50)

class LayerRed(cocos.layer.ColorLayer):
    def __init__(self):
        super(LayerRed, self).__init__(128, 0, 128, 255,
                                       width=120, height=80)
        self.position = (100, 80)

class LayerYellow(cocos.layer.ColorLayer):
    def __init__(self):
        super(LayerYellow, self).__init__(128, 128, 0, 255,
                                          width=120, height=80)
        self.position = (150, 110)

cocos.director.director.init()
main_scene = cocos.scene.Scene()
main_scene.add(LayerBlue(), z=0)
main_scene.add(LayerRed(), z=1)
main_scene.add(LayerYellow(), z=2)
cocos.director.director.run(main_scene)
