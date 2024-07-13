from cocos.scene import Scene
from cocos.layer import ColorLayer
from cocos.director import director
from cocos.text import Label

class Layer1(ColorLayer):
    #将这个层设置为事件处理程序，因为我希望能够在按键时转换到另一个场景
    is_event_handler = True

    def __init__(self):
        # 传入一个RGBA颜色值，因为它是一个ColorLayer
        super(Layer1, self).__init__(155, 89, 182, 1000)
        #设置一个简单的标签，没有设置额外的参数
        text = Label("这是第一个界面")
        # 为了确保位置保持不变，但是又不知道窗口的具体宽度和高度，所以将它们除以2
        text.position = director._window_virtual_width / 2, director._window_virtual_height / 2
        #添加文本
        self.add(text)

    # 按键按下
    def on_key_press(self, key, modifiers):
        director.replace(Scene(Layer2())) # 按下按键实现场景切换


#为第二个场景制作的第二层
class Layer2(ColorLayer):
    #将这个层设置为事件处理程序，因为我希望能够在按键时转换到另一个场景
    is_event_handler = True

    # 初始化并调用超级类，设置不同的背景颜色
    def __init__(self):
        super(Layer2, self).__init__(231, 76, 60, 1000)

        # 设置先生的文本
        text = Label("这是第二个界面")
        text.position = director._window_virtual_width / 2, director._window_virtual_height / 2
        self.add(text)

    # 按键按下
    def on_key_press(self, key, modifiers):
        director.replace(Scene(Layer1()))

director.init()
director.run(Scene(Layer1()))
