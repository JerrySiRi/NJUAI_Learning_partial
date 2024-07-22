# -*- encoding:utf-8 -*-
import cocos
from pyglet.window import key
import cocos.euclid as eu


class SquareLand(cocos.layer.ScrollableLayer):
    is_event_handler = True

    def __init__(self):
        super(SquareLand, self).__init__()

        # 定义世界地图的宽和高
        self.px_width = 1000 + 4 * 98  # 1392
        self.px_height = 1000

        # 为了缩短后面代码的长度
        px_width = self.px_width
        px_height = self.px_height

        # 下面的代码中定义了两个图层，一个大的一个稍微小的
        # 这两个背景重叠起来就形成了一个带有边框的地图效果
        bg = cocos.layer.ColorLayer(170, 170, 0, 255, width=px_width,
                                    height=px_height)
        self.add(bg, z=0)

        margin = int(px_width * 0.01)
        # print 'margin',margin
        self.margin = margin
        bg = cocos.layer.ColorLayer(0, 170, 170, 255, width=px_width - 2 * margin,
                                    height=px_height - 2 * margin)
        bg.position = (margin, margin)
        self.add(bg, z=1)

        # 定义用户精灵
        self.player = cocos.sprite.Sprite("timg.jpg")
        self.player.position = (self.player.width / 2, self.player.height / 2)
        self.player.fastness = 200

        self.add(self.player, z=4)

        # 这里定义一个字典，来表示按钮是否别按下
        self.buttons = {  # button state : current value, 0 not pressed, 1 pressed
            key.LEFT: 0,
            key.RIGHT: 0,
            key.UP: 0,
            key.DOWN: 0
        }

        # 每一帧都会更新player的状态，具体参照step函数
        self.schedule(self.step)

    def on_enter(self):
        # 获取scroller的指针，用来设置set_focus,注意要调用父类的on_enter
        super(SquareLand, self).on_enter()
        self.scroller = self.get_ancestor(cocos.layer.ScrollingManager)

    def on_key_press(self, k, modifiers):
        # 请注意这里的小技巧
        if k in self.buttons:
            self.buttons[k] = 1

    def on_key_release(self, k, modifiers):
        if k in self.buttons:
            self.buttons[k] = 0

    # 用来判断是否到达地图的边缘，如果到达边缘则不会继续移动
    def clamp(self, actor, new_pos):
        x, y = new_pos
        if x - actor.width / 2 < self.margin:
            x = self.margin + actor.width / 2
        elif x + actor.width / 2 > self.px_width - self.margin:
            x = self.px_width - self.margin - actor.width / 2
        if y - actor.height / 2 < self.margin:
            y = self.margin + actor.height / 2
        elif y + actor.height / 2 > self.px_height - self.margin:
            y = self.px_height - self.margin - actor.height / 2
        return x, y

    def step(self, dt):
        btns = self.buttons
        # 请注意这里用来移动的小技巧
        move_dir = eu.Vector2(btns[key.RIGHT] - btns[key.LEFT],
                              btns[key.UP] - btns[key.DOWN])
        changed = False
        if move_dir:
            new_pos = self.player.position + self.player.fastness * dt * move_dir.normalize()
            new_pos = self.clamp(self.player, new_pos)

            self.player.position = new_pos
            changed = True

        if changed:
            self.update_after_change()

    def update_after_change(self):
        self.scroller.set_focus(*self.player.position)


if __name__ == '__main__':
    cocos.director.director.init(1024, 600)  # view_rectangle
    scene = cocos.scene.Scene()
    world_layer = SquareLand()
    scroller = cocos.layer.ScrollingManager()
    scroller.add(world_layer)
    scene.add(scroller)
    cocos.director.director.run(scene)