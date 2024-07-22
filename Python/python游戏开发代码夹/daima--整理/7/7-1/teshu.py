# coding=utf-8

from cocos.sprite import *
from cocos.scene import *
from cocos.actions import *
from cocos.layer import *
from cocos.menu import *
from cocos.layer.util_layers import ColorLayer
# 定义全局变量hero
hero = None
# 自定义GameLayer层类
class GameLayer(ColorLayer):
    def __init__(self):
        super(GameLayer, self).__init__(255, 255, 255, 255)
        # 声明全局变量hero
        global hero
        # 创建hero精灵
        hero = Sprite('assets/camel.png')
        hero.position = 560, 320
        self.add(hero)

# 自定义主菜单类
class MainMenu(Menu):

    def __init__(self):
        super(MainMenu, self).__init__()
        # 菜单项初始化设置
        self.font_item['font_size'] = 20
        self.font_item['color'] = (0, 0, 0, 255)
        self.font_item_selected['color'] = (0, 0, 0, 255)
        self.font_item_selected['font_size'] = 26

        item1 = MenuItem('使用CallFunc', self.on_callback1)

        x = 120
        y = 560
        step = 50

        self.create_menu([item1],
                         layout_strategy=fixedPositionMenuLayout(
                             [(x, y), (x, y - step)]))

    def my_func(self):
        hero.do(Hide())

    def on_callback1(self):
        action = CallFunc(self.my_func)
        hero.do(action)

if __name__ == '__main__':
    # 初始化导演，设置窗口的高、宽、标题
    director.init(width=1136, height=640, caption='特殊动作示例')

    # 创建主场景，并添加GameLayer到场景
    main_scene = Scene(GameLayer())
    # 添加主菜单到场景
    main_scene.add(MainMenu())

    # 开始启动main_scene场景
    director.run(main_scene)
