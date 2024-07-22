# coding=utf-8

from cocos.menu import *
from cocos.scene import *
from cocos.layer import *

# 自定义主菜单类
class MainMenu(Menu):

    def __init__(self):
        super(MainMenu, self).__init__()

        self.font_item['font_size'] = 32
        self.font_item_selected['font_size'] = 40

        item1 = MenuItem('开始', self.on_item1_callback)
        item2 = ToggleMenuItem('音效', self.on_item2_callback, False)
        
        self.create_menu([item1, item2],     #鼠标悬停到菜单上面时通过shake()实现晃动
                         selected_effect=shake(),
                         unselected_effect=shake_back())

    def on_item1_callback(self):
        print('刚刚使用了MenuItem')

    def on_item2_callback(self, value):
        print('刚刚使用了ToggleMenuItem', value)


if __name__ == "__main__":
    # 初始化导演
    director.init(caption="文本菜单例子")
    # 创建主菜单
    main_menu = MainMenu()
    # 创建主场景
    main_scene = Scene(main_menu)
    # 开始启动场景
    director.run(main_scene)
