from cocos.director import director
from cocos.layer import ColorLayer
from cocos.scene import Scene
from cocos.scenes import FadeTransition, SplitColsTransition
from cocos.text import Label

class Layer1(ColorLayer):
    is_event_handler = True

    def __init__(self):
        super(Layer1, self).__init__(155, 89, 182, 1000)

        text = Label("这是第一个界面")
        text.position = director._window_virtual_width / 2, director._window_virtual_height / 2
        self.add(text)

    def on_key_press(self, key, modifiers):
        # 使用replace()调用过度动画特效FadeTransition
        director.replace(FadeTransition(Scene(Layer2())))

class Layer2(ColorLayer):
    is_event_handler = True

    def __init__(self):
        super(Layer2, self).__init__(231, 76, 60, 1000)

        text = Label("这是第二个界面")
        text.position = director._window_virtual_width / 2, director._window_virtual_height / 2
        self.add(text)

    def on_key_press(self, key, modifiers):
        # 使用replace()调用过度动画特效SplitColsTransition
        director.replace(SplitColsTransition(Scene(Layer1())))
        
director.init()
director.run(Scene(Layer1()))