import cocos
from cocos.layer import Layer, ColorLayer
from cocos import layer
from cocos.sprite import Sprite
from cocos.actions import *
from cocos.director import director

class Actions(ColorLayer):
    def __init__(self):
        super(Actions, self).__init__(52, 152, 219, 1000)

        # 我用cocos初始化一个sprite精灵，将下面的路径的图像作为精灵
        self.sprite = Sprite('assets/img/grossini.png')

        # 把精灵的位置设置在屏幕中央
        self.sprite.position = 320, 240

        # 下面开始让精灵执行所有的动作
        self.fade_in()
        self.move_left()

    def fade_in(self):
        # 首先创建一个FadeIn动画对象
        fade_action = FadeIn(2)

        # 将精灵不透明度设置为0，这样它就不会在屏幕上闪烁
        self.sprite.opacity = 0

        # 把精灵添加到屏幕上
        self.add(self.sprite, z=1)

        #开始实现要2秒种的淡入效果
        self.sprite.do(fade_action)

    def move_left(self):
        # 创建一个MoveBy动画对象，设置它在X轴上移动-150，在Y轴上移动0，一共花费2秒种完成移动动作
        left = MoveBy((-150, 0), 2)

        # 最后让精灵向左移动
        self.sprite.do(left)

# 初始化控制器并运行层（这是cocos程序的固定用法）
director.init()
director.run(cocos.scene.Scene(Actions()))