import sys
import os
sys.path.insert(0,os.path.join(os.path.dirname(__file__),'..'))
path = os.path.join(os.path.dirname(__file__)) + "cocos"
sys.path.insert(0,path)
from cocos.menu import *
from cocos.scene import *
from cocos.layer import *
from cocos.text  import *
class Hello(Layer):
    def __init__(self):
        super(Hello,self).__init__()
        self.label=Label('欢迎进入游戏',
		font_name='Times New Roman',
		font_size=32,
		anchor_x='center',anchor_y='center')
        self.label.position=320,240
        self.add(self.label)

class MainMenu1(Menu):
    def __init__(self,hello):
        super(MainMenu1,self).__init__()
        self.hello=hello
        self.menu_valign=BOTTOM
        self.menu_halign=LEFT
        items = [
                (MenuItem('开始游戏',self.on_quit)),
                ]
        self.create_menu(items,selected_effect=zoom_in(),unselected_effect=zoom_out())

    def on_quit(self):
        self.hello.label.element.text="游戏开始了！！！"


class MainMenu(Menu):
    def __init__(self):
        super(MainMenu,self).__init__()

        self.menu_valign = BOTTOM
        self.menu_halign = RIGHT

        items =[
                (MenuItem('关闭游戏',self.on_quit)),
                ]
        self.create_menu(items,selected_effect=zoom_in(),unselected_effect=zoom_out())

    def on_quit(self):
        pyglet.app.exit()



if __name__== "__main__":
    director.init()
    hello_layer=Hello()
    main_scene=Scene(hello_layer)
    main_scene.add(MainMenu())
    main_scene.add(MainMenu1(hello_layer ))
    director.run(main_scene)