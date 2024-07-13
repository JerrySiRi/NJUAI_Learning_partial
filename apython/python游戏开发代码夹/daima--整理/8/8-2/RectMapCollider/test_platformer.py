from __future__ import division, print_function, unicode_literals
import pyglet
from pyglet.window import key

pyglet.resource.path.append(pyglet.resource.get_script_home())
pyglet.resource.reindex()

import cocos
from cocos import tiles, actions, layer, mapcolliders


class PlatformerController(actions.Action):
    on_ground = True
    MOVE_SPEED = 300
    JUMP_SPEED = 800
    GRAVITY = -1200

    def start(self):
        self.target.velocity = (0, 0)

    def step(self, dt):
        global keyboard, scroller
        if dt > 0.1: #注意，如果设置太大的dt将使播放器穿过墙壁，dt在启动时可能会变慢
            return
        vx, vy = self.target.velocity

        # 使用player、重力和其他加速度影响会更新速度
        vx = (keyboard[key.RIGHT] - keyboard[key.LEFT]) * self.MOVE_SPEED
        vy += self.GRAVITY * dt
        if self.on_ground and keyboard[key.SPACE]:
            vy = self.JUMP_SPEED

        # 用更新的速度计算（暂定）位移
        dx = vx * dt
        dy = vy * dt

        # 获取玩家当前的边界矩形
        last = self.target.get_rect()

        # 建立临时的矩形区域
        new = last.copy()
        new.x += dx
        new.y += dy

        # 考虑到遇到障碍，它将调整新的vx，vy
        self.target.velocity = self.target.collision_handler(last, new, vx, vy)

        # 更新on_ground的状态
        self.on_ground = (new.y == last.y)

        #更新player位置，玩家的位置固定在图像矩形的中心
        self.target.position = new.center

        #将滚动视图移动到播放器中心
        scroller.set_focus(*new.center)

description = """
显示如何使用地图对撞机来控制角色和地形之间的碰撞。
使用左右箭头和空格进行控制。
使用D显示单元格/图块信息
"""

def main():
    global keyboard, tilemap, scroller
    from cocos.director import director
    director.init(width=800, height=600, autoscale=False)

    print(description)
    # 创建一个图层来放置播放器
    player_layer = layer.ScrollableLayer()
    # 注意：此子画面的锚点位于CENTER中（cocos默认值）
    # 这意味着所有定位都必须使用其矩形的中心
    player = cocos.sprite.Sprite('witch-standing.png')
    player_layer.add(player)
    player.do(PlatformerController())

    # 将瓦片贴图和播放器精灵图层添加到滚动管理器
    scroller = layer.ScrollingManager()
    fullmap = tiles.load('platformer-map.xml')
    tilemap_walls = fullmap['walls']
    scroller.add(tilemap_walls, z=0)
    tilemap_decoration = fullmap['decoration']
    scroller.add(tilemap_decoration, z=1)
    scroller.add(player_layer, z=2)

    # 使用地图上的player_start令牌将玩家设置为开始
    start = tilemap_decoration.find_cells(player_start=True)[0]
    r = player.get_rect()

    #将player的中底与起始单元的中底对齐
    r.midbottom = start.midbottom

    # player图像锚点（位置）在精灵的中心
    player.position = r.center

    # 给 player一个碰撞处理程序
    mapcollider = mapcolliders.RectMapCollider(velocity_on_bump='slide')
    player.collision_handler = mapcolliders.make_collision_handler(
        mapcollider, tilemap_walls)

    # 用背景层颜色和滚动层构造场景
    platformer_scene = cocos.scene.Scene()
    platformer_scene.add(layer.ColorLayer(100, 120, 150, 255), z=0)
    platformer_scene.add(scroller, z=1)

    # 跟踪键盘按键
    keyboard = key.KeyStateHandler()
    director.window.push_handlers(keyboard)

    #允许显示有关单元格/图块的信息
    def on_key_press(key, modifier):
        if key == pyglet.window.key.D:
            tilemap_walls.set_debug(True)
    director.window.push_handlers(on_key_press)

    # 运行
    director.run(platformer_scene)

if __name__ == '__main__':
    main()
