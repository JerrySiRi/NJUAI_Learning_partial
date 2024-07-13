import cocos
from cocos.director import director
import pyglet


class KeyDisplay(cocos.layer.Layer):
    is_event_handler = True

    def __init__(self):
        super(KeyDisplay, self).__init__()

        self.text = cocos.text.Label('Keys: ', font_size=18, x=100, y=280)
        self.add(self.text)

        self.keys_pressed = set()

    def update_text(self):
        key_names = [pyglet.window.key.symbol_string(k) for k in self.keys_pressed]
        self.text.element.text = 'Keys: ' + ','.join(key_names)

    def on_key_press(self, key, modifiers):
        # 按下按键自动触发本方法
        self.keys_pressed.add(key)
        self.update_text()

    def on_key_release(self, key, modifiers):
        # 松开按键自动触发本方法
        self.keys_pressed.remove(key)
        self.update_text()


class MouseDisplay(cocos.layer.Layer):
    is_event_handler = True

    def __init__(self):
        super(MouseDisplay, self).__init__()

        self.text = cocos.text.Label('Mouse @', font_size=18,
                                     x=100, y=240)
        self.add(self.text)

    def on_mouse_motion(self, x, y, dx, dy):
        # dx,dy为向量,表示鼠标移动方向
        self.text.element.text = 'Mouse @ {}, {}, {}, {}'.format(x, y, dx, dy)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.text.element.text = 'Mouse @ {}, {}, {}, {}'.format(x, y, buttons, modifiers)

    def on_mouse_press(self, x, y, buttons, modifiers):
        # 按下鼠标按键不仅更新鼠标位置,还改变标签的位置.这里使用director.get_virtual_coordinates(),用于保证即使窗口缩放过也能正确更新位置,如果直接用x,y会位置错乱,原因不明
        self.text.element.text = 'Mouse @ {}, {}, {}, {}'.format(x, y, buttons, modifiers)
        self.text.element.x, self.text.element.y = director.get_virtual_coordinates(x, y)


# 这次创建的窗口带调整大小的功能
director.init(resizable=True)
main_scene = cocos.scene.Scene(KeyDisplay(), MouseDisplay())
director.run(main_scene)