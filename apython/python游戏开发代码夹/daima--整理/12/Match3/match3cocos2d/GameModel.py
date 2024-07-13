__all__ = ['GameModel']

import pyglet
import os.path
import sys
from os.path import join, isdir, basename
from random import choice, randint
from glob import glob

from cocos.actions import *
from cocos.sprite import Sprite
from cocos import *
from status import status

CELL_WIDTH, CELL_HEIGHT = 100, 100
ROWS_COUNT, COLS_COUNT = 6, 8

#游戏状态值
WAITING_PLAYER_MOVEMENT = 1
PLAYER_DOING_MOVEMENT = 2
SWAPPING_TILES = 3
IMPLODING_TILES = 4
DROPPING_TILES = 5
GAME_OVER = 6


class GameModel(pyglet.event.EventDispatcher):
    def __init__(self):
        super(GameModel, self).__init__()
        self.tile_grid = {}  # Dict仿真稀疏矩阵 key: tuple(x,y), value : tile_type
        self.imploding_tiles = []  # 用于爆破精灵列表 IMPLODING_TILES
        self.dropping_tiles = []  # 在DROPPING_TILES中使用的正在删除的砖精灵列表
        self.swap_start_pos = None  # 点击第一个精灵准备交换位置
        self.swap_end_pos = None  # 单击的第二个的位置以进行交换
        # 替换是Windows兼容性。
        script_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')
        os.chdir(script_dir)
        if isdir('images'):
            image_base_path = join(script_dir, 'images')
        else:
            image_base_path = join(sys.prefix, 'share', 'match3cocos2d', 'images')
        pyglet.resource.path = [image_base_path]
        pyglet.resource.reindex()
        self.available_tiles = [basename(s) for s in glob(join(image_base_path, '*.png'))]
        self.game_state = WAITING_PLAYER_MOVEMENT
        self.objectives = []
        self.on_game_over_pause = 0

    def start(self):
        self.set_next_level()

    def set_next_level(self):
        self.play_time = self.max_play_time = 60
        for elem in self.imploding_tiles + self.dropping_tiles:
            self.view.remove(elem)
        self.on_game_over_pause = 0
        self.fill_with_random_tiles()
        self.set_objectives()
        pyglet.clock.unschedule(self.time_tick)
        pyglet.clock.schedule_interval(self.time_tick, 1)

    def time_tick(self, delta):
        self.play_time -= 1
        self.dispatch_event("on_update_time", self.play_time / float(self.max_play_time))
        if self.play_time == 0:
            pyglet.clock.unschedule(self.time_tick)
            self.game_state = GAME_OVER
            self.dispatch_event("on_game_over")

    def set_objectives(self):
        objectives = []
        while len(objectives) < 3:
            tile_type = choice(self.available_tiles)
            sprite = self.tile_sprite(tile_type, (0, 0))
            count = randint(1, 20)
            if tile_type not in [x[0] for x in objectives]:
                objectives.append([tile_type, sprite, count])

        self.objectives = objectives

    def fill_with_random_tiles(self):
        """
        用随机tiles填充tile_grid
        """
        for elem in [x[1] for x in self.tile_grid.values()]:
            self.view.remove(elem)
        tile_grid = {}
        # 用随机tile类型填充数据矩阵
        while True:  # 循环，直到我们有一个有效的表（没有内爆线）
            for x in range(COLS_COUNT):
                for y in range(ROWS_COUNT):
                    tile_type, sprite = choice(self.available_tiles), None
                    tile_grid[x, y] = tile_type, sprite
            if len(self.get_same_type_lines(tile_grid)) == 0:
                break
            tile_grid = {}

        # 基于指定的tile类型构建精灵
        for key, value in tile_grid.items():
            tile_type, sprite = value
            sprite = self.tile_sprite(tile_type, self.to_display(key))
            tile_grid[key] = tile_type, sprite
            self.view.add(sprite)

        self.tile_grid = tile_grid

    def swap_elements(self, elem1_pos, elem2_pos):
        tile_type, sprite = self.tile_grid[elem1_pos]
        self.tile_grid[elem1_pos] = self.tile_grid[elem2_pos]
        self.tile_grid[elem2_pos] = tile_type, sprite

    def implode_lines(self):
        """
        :return: 用多于3个相同类型的元素进行处理
        """
        implode_count = {}
        for x, y in self.get_same_type_lines(self.tile_grid):
            tile_type, sprite = self.tile_grid[x, y]
            self.tile_grid[x, y] = None
            self.imploding_tiles.append(sprite)  # tiles内爆炸销毁
            # 内嵌爆炸动画
            sprite.do(ScaleTo(0, 0.5) | RotateTo(180, 0.5) + CallFuncS(self.on_tile_remove))
            implode_count[tile_type] = implode_count.get(tile_type, 0) + 1
        # Decrease counter for tiles matching objectives
        for elem in self.objectives:
            if elem[0] in implode_count:
                Scale = ScaleBy(1.5, 0.2)
                elem[2] = max(0, elem[2] - implode_count[elem[0]])
                elem[1].do((Scale + Reverse(Scale)) * 3)
        # 删除已完成的目标
        self.objectives = [elem for elem in self.objectives if elem[2] > 0]
        if len(self.imploding_tiles) > 0:
            self.game_state = IMPLODING_TILES  # 等待爆炸动画完成
            pyglet.clock.unschedule(self.time_tick)
        else:
            self.game_state = WAITING_PLAYER_MOVEMENT
            pyglet.clock.schedule_interval(self.time_tick, 1)
        return self.imploding_tiles

    def drop_groundless_tiles(self):
        """
       在所有栏上，从下到上：
        a）计算间隙或向下移动已经计算的间隙
        b）顶部落下的瓷砖与间隙一样多
        :return:
        """
        tile_grid = self.tile_grid

        for x in range(COLS_COUNT):
            gap_count = 0
            for y in range(ROWS_COUNT):
                if tile_grid[x, y] is None:
                    gap_count += 1
                elif gap_count > 0:  #从Y移动到y-gap_count
                    tile_type, sprite = tile_grid[x, y]
                    if gap_count > 0:
                        sprite.do(MoveTo(self.to_display((x, y - gap_count)), 0.3 * gap_count))
                    tile_grid[x, y - gap_count] = tile_type, sprite
            for n in range(gap_count):  # 下降多少tiles作为间隙计数
                tile_type = choice(self.available_tiles)
                sprite = self.tile_sprite(tile_type, self.to_display((x, y + n + 1)))
                tile_grid[x, y - gap_count + n + 1] = tile_type, sprite
                sprite.do(
                    MoveTo(self.to_display((x, y - gap_count + n + 1)), 0.3 * gap_count) +
                    CallFuncS(self.on_drop_completed))
                self.view.add(sprite)
                self.dropping_tiles.append(sprite)

    def on_drop_completed(self, sprite):
        self.dropping_tiles.remove(sprite)
        if len(self.dropping_tiles) == 0:  # 全部落下的
            self.implode_lines()  # 检查新的碰撞

    def on_tile_remove(self, sprite):
        status.score += 1
        self.imploding_tiles.remove(sprite)
        self.view.remove(sprite)
        if len(self.imploding_tiles) == 0:  #碰撞爆炸完成，跌落tile填补缺口
            self.dispatch_event("on_update_objectives")
            self.drop_groundless_tiles()
            if len(self.objectives) == 0:
                pyglet.clock.unschedule(self.time_tick)
                self.dispatch_event("on_level_completed")

    def set_controller(self, controller):
        self.controller = controller

    def set_view(self, view):
        self.view = view

    def tile_sprite(self, tile_type, pos):
        """
        :param tile_type: 数字ID必须在可用图像的范围内
        :param pos:精灵的位置
        :return: 根据tile_type编译精灵
        """
        sprite = Sprite(tile_type)
        sprite.position = pos
        sprite.scale = 1
        return sprite

    def on_tiles_swap_completed(self):
        self.game_state = DROPPING_TILES
        if len(self.implode_lines()) == 0:
            # 没有碰撞爆炸，回滚游戏

            # 开始为两个对象交换动画
            tile_type, sprite = self.tile_grid[self.swap_start_pos]
            sprite.do(MoveTo(self.to_display(self.swap_end_pos), 0.4))
            tile_type, sprite = self.tile_grid[self.swap_end_pos]
            sprite.do(MoveTo(self.to_display(self.swap_start_pos), 0.4) +
                CallFunc(self.on_tiles_swap_back_completed))

            # 恢复网格
            self.swap_elements(self.swap_start_pos, self.swap_end_pos)
            self.game_state = SWAPPING_TILES

    def on_tiles_swap_back_completed(self):
        self.game_state = WAITING_PLAYER_MOVEMENT

    def to_display(self, row_col):
        """
        :param row:
        :param col:
        :return: (x, y) 从来自二维( row, col) 阵列位置的显示坐标
        """
        row, col = row_col
        return CELL_WIDTH / 2 + row * CELL_WIDTH, CELL_HEIGHT / 2 + col * CELL_HEIGHT

    def to_model_pos(self, view_x_y):
        view_x, view_y = view_x_y
        return int(view_x / CELL_WIDTH), int(view_y / CELL_HEIGHT)

    def get_same_type_lines(self, tile_grid, min_count=3):
        """
        识别由微元连续元素组成的垂直和水平线
        :param min_count: 识别直线中的最小连续元素
        """
        all_line_members = []

        # 检查垂直线
        for x in range(COLS_COUNT):
            same_type_list = []
            last_tile_type = None
            for y in range(ROWS_COUNT):
                tile_type, sprite = tile_grid[x, y]
                if last_tile_type == tile_type:
                    same_type_list.append((x, y))
                # 结束行，因为类型改变或到达边缘
                if tile_type != last_tile_type or y == ROWS_COUNT - 1:
                    if len(same_type_list) >= min_count:
                        all_line_members.extend(same_type_list)
                    last_tile_type = tile_type
                    same_type_list = [(x, y)]

        # 检查水平线
        for y in range(ROWS_COUNT):
            same_type_list = []
            last_tile_type = None
            for x in range(COLS_COUNT):
                tile_type, sprite = tile_grid[x, y]
                if last_tile_type == tile_type:
                    same_type_list.append((x, y))
                # 行结束，因为类型改变或到达边缘
                if tile_type != last_tile_type or x == COLS_COUNT - 1:
                    if len(same_type_list) >= min_count:
                        all_line_members.extend(same_type_list)
                    last_tile_type = tile_type
                    same_type_list = [(x, y)]

        # 删除重复
        all_line_members = list(set(all_line_members))
        return all_line_members

    def on_mouse_press(self, x, y):
        if self.game_state == WAITING_PLAYER_MOVEMENT:
            self.swap_start_pos = self.to_model_pos((x, y))
            self.game_state = PLAYER_DOING_MOVEMENT

    def on_mouse_drag(self, x, y):
        if self.game_state != PLAYER_DOING_MOVEMENT:
            return

        start_x, start_y = self.swap_start_pos
        self.swap_end_pos = new_x, new_y = self.to_model_pos((x, y))

        distance = abs(new_x - start_x) + abs(new_y - start_y)  # 水平+垂直网格步长

        # 忽略移动，如果不在第1步离开初始位置
        if new_x < 0 or new_y < 0 or distance != 1:
            return

        # 为两个对象启动交换动画
        tile_type, sprite = self.tile_grid[self.swap_start_pos]
        sprite.do(MoveTo(self.to_display(self.swap_end_pos), 0.4))
        tile_type, sprite = self.tile_grid[self.swap_end_pos]
        sprite.do(MoveTo(self.to_display(self.swap_start_pos), 0.4) +
            CallFunc(self.on_tiles_swap_completed))

        # 在数据网格中交换元素
        self.swap_elements(self.swap_start_pos, self.swap_end_pos)
        self.game_state = SWAPPING_TILES

    def dump_table(self):
        """
        :return: 打印播放表，进行调试
        """
        for y in range(ROWS_COUNT - 1, -1, -1):
            line_str = ''
            for x in range(COLS_COUNT):
                line_str += str(self.tile_grid[x, y][0])
            print(line_str)


GameModel.register_event_type('on_update_objectives')
GameModel.register_event_type('on_update_time')
GameModel.register_event_type('on_game_over')
GameModel.register_event_type('on_level_completed')
