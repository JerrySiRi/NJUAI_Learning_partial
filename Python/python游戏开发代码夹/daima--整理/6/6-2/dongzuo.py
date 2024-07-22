import cocos
from cocos.actions import Repeat, Reverse, ScaleBy, RotateBy


# 继承了带颜色属性的层类
class HelloWorld(cocos.layer.ColorLayer):
    def __init__(self):
        # 层调成蓝色
        super(HelloWorld, self).__init__(64, 64, 224, 255)
        label = cocos.text.Label('Hello, World!',
                                 font_name='Times New Roman',
                                 font_size=32,
                                 anchor_x='center', anchor_y='center')
        label.position = 320, 240
        self.add(label)

        # 新建一个精灵,在这里是一个小人
        sprite = cocos.sprite.Sprite('12345678.jpg')
        # 精灵锚点默认在正中间,只设置位置就好
        sprite.position = 320, 240
        # 放大三倍,添加到层,z轴设为1,比层更靠前
        sprite.scale = 3
        self.add(sprite, z=1)

        # 定义一个动作,即2秒内放大三倍
        scale = ScaleBy(3, duration=2)
        # 标签的动作:重复执行放大三倍缩小三倍又放大三倍...Repeat即为重复动作,Reverse为相反动作
        label.do(Repeat(scale + Reverse(scale)))
        # 精灵的动作:重复执行缩小三倍放大三倍又缩小三倍...
        sprite.do(Repeat(Reverse(scale) + scale))
        # 层的动作:重复执行10秒内360度旋转
        self.do(RotateBy(360, duration=10))


cocos.director.director.init()
main_scene = cocos.scene.Scene(HelloWorld())
cocos.director.director.run(main_scene)