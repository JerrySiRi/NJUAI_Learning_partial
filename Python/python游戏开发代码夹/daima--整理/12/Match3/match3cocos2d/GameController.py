from cocos.layer import Layer

class GameController(Layer):
    is_event_handler = True  #: 启用yglet的事件

    def __init__(self, model):
        super(GameController, self).__init__()
        self.model = model

    def on_mouse_press(self, x, y, buttons, modifiers):
        self.model.on_mouse_press(x, y)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.model.on_mouse_drag(x, y)

