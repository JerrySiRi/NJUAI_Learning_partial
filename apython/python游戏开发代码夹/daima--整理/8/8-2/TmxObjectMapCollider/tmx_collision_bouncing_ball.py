import pyglet
from pyglet.window import key

pyglet.resource.path.append(pyglet.resource.get_script_home())
pyglet.resource.reindex()

import cocos
from cocos import tiles, actions, layer
from cocos import mapcolliders
from cocos.mapcolliders import TmxObjectMapCollider


class Ball(cocos.sprite.Sprite):
    def __init__(self, position, velocity, fn_collision_handler, fn_set_focus, color):
        super(Ball, self).__init__("circle6.png", color=color)
        self.opacity = 128
        self.position = position
        self.velocity = velocity
        self.fn_collision_handler = fn_collision_handler
        self.fn_set_focus = fn_set_focus
        self.schedule(self.step)

    def step(self, dt):
        vx, vy = self.velocity
        dx = vx * dt
        dy = vy * dt
        last = self.get_rect()
        new = last.copy()
        new.x += dx
        new.y += dy
        self.velocity = self.fn_collision_handler(last, new, vx, vy)
        self.position = new.center
        self.fn_set_focus(*self.position)


description = """
学习碰撞！！！！
"""


def main():
    global keyboard, walls, scroller
    from cocos.director import director
    director.init(width=800, height=600, autoscale=False)

    print(description)

    # 将tilemap和Player Sprite图层添加到滚动管理器
    scroller = layer.ScrollingManager()
    walls = tiles.load('tmx_collision.tmx')['walls']
    assert isinstance(walls, tiles.TmxObjectLayer)
    scroller.add(walls, z=0)

    #给 小球和墙之间一个碰撞处理程序
    mapcollider = TmxObjectMapCollider()
    mapcollider.on_bump_handler = mapcollider.on_bump_bounce
    fn_collision_handler = mapcolliders.make_collision_handler(mapcollider, walls)

    # 设置视觉焦点位置
    fn_set_focus = scroller.set_focus
    
    # 创建一个图层来放置播放器
    actors_layer = layer.ScrollableLayer()
    ball = Ball((300, 300), (600, 600), fn_collision_handler, fn_set_focus, (255, 0, 255)) 
    actors_layer.add(ball)

    scroller.add(actors_layer, z=1)

    # 使用“ player_start”属性设置玩家开始
    player_start = walls.find_cells(player_start=True)[0]
    ball.position = player_start.center

    # 设定焦点，以便玩家可以看到
    scroller.set_focus(*ball.position)

    # 提取不是墙的player_start
    walls.objects.remove(player_start)

    # 用背景层颜色和滚动层构造场景
    platformer_scene = cocos.scene.Scene()
    platformer_scene.add(layer.ColorLayer(100, 120, 150, 255), z=0)
    platformer_scene.add(scroller, z=1)

    # 跟踪键盘按键
    keyboard = key.KeyStateHandler()
    director.window.push_handlers(keyboard)

    # 运行scene
    director.run(platformer_scene)


if __name__ == '__main__':
    main()
