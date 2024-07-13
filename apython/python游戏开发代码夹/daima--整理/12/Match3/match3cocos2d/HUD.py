from cocos.layer import *

from cocos.text import *
from cocos.actions import *
from ProgressBar import ProgressBar
from status import status


class BackgroundLayer(Layer):
    def __init__(self):
        super(BackgroundLayer, self).__init__()
        # self.img = pyglet.resource.image('background.png')

    def draw(self):
        pass


class ScoreLayer(Layer):
    objectives = []

    def __init__(self):
        w, h = director.get_window_size()
        super(ScoreLayer, self).__init__()

        # 透明层
        self.add(ColorLayer(100, 100, 200, 100, width=w, height=48), z=-1)

        self.position = (0, h - 48)

        progress_bar = self.progress_bar = ProgressBar(width=200, height=20)
        progress_bar.position = 20, 15
        self.add(progress_bar)
        self.score = Label('Score:', font_size=36,
                           font_name='Edit Undo Line BRK',
                           color=(255, 255, 255, 255),
                           anchor_x='left',
                           anchor_y='bottom')
        self.score.position = (0, 0)
        # self.add(self.score)
        self.lvl = Label('Lvl:', font_size=36,
                         font_name='Edit Undo Line BRK',
                         color=(255, 255, 255, 255),
                         anchor_x='left',
                         anchor_y='bottom')

        self.lvl.position = (450, 0)
        # self.add(self.lvl)
        self.objectives_list = []
        self.objectives_labels = []

    def set_objectives(self, objectives):
        w, h = director.get_window_size()
        # 清除任何预先设定的目标
        for tile_type, sprite, count in self.objectives:
            self.remove(sprite)
        for count_label in self.objectives_labels:
            self.remove(count_label)
        self.objectives = objectives
        self.objectives_labels = []
        x = w / 2 - 150 / 2
        for tile_type, sprite, count in objectives:
            text_w = len(str(count)) * 7
            count_label = Label(str(count), font_size=14,
                                font_name='Edit Undo Line BRK',
                                color=(255, 255, 255, 255), bold=True,
                                anchor_x='left', anchor_y='bottom')
            count_label.position = x - text_w, 7
            self.add(count_label, z=2)
            self.objectives_labels.append(count_label)
            count_label = Label(str(count), font_size=16,
                                font_name='Edit Undo Line BRK',
                                color=(0, 0, 0, 255), bold=True,
                                anchor_x='left', anchor_y='bottom')
            count_label.position = x - text_w - 1, 8
            self.add(count_label, z=1)
            self.objectives_labels.append(count_label)
            sprite.position = x, 24
            sprite.scale = 0.5
            x += 50
            self.add(sprite)

    def draw(self):
        super(ScoreLayer, self).draw()
        self.score.element.text = 'Score:%d' % status.score

        lvl = status.level_idx or 0
        self.lvl.element.text = 'Lvl:%d' % lvl


class MessageLayer(Layer):
    def show_message(self, msg, callback=None, msg_duration=1):
        w, h = director.get_window_size()

        self.msg = Label(msg,
                         font_size=52,
                         font_name='Edit Undo Line BRK',
                         anchor_y='center',
                         anchor_x='center')
        self.msg.position = (w // 2.0, h)

        self.add(self.msg)

        actions = Accelerate(MoveBy((0, -h / 2.0), duration=msg_duration / 2))
        actions += \
            Delay(1) + \
            Accelerate(MoveBy((0, -h / 2.0), duration=msg_duration / 2)) + \
            Hide()

        if callback:
            actions += CallFunc(callback)

        self.msg.do(actions)


class HUD(Layer):
    def __init__(self):
        super(HUD, self).__init__()
        self.score_layer = ScoreLayer()
        self.add(self.score_layer)
        self.add(MessageLayer(), name='msg')

    def show_message(self, msg, callback=None, msg_duration=1):
        self.get('msg').show_message(msg, callback, msg_duration)

    def set_objectives(self, objectives):
        self.score_layer.set_objectives(objectives)

    def update_time(self, time_percent):
        self.score_layer.progress_bar.set_progress(time_percent)
