#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random

import cocos
from cocos.director import director

import pyglet
from cocos.layer import Layer


class KeyDisplay(cocos.layer.Layer):
    is_event_handler = True  #: 启动pyglet's事件

    def __init__(self):
        super(KeyDisplay, self).__init__()

        self.text = cocos.text.Label("", x=100, y=280)

        # 跟踪哪些键被按下:
        self.keys_pressed = set()
        self.update_text()
        self.add(self.text)
        self.ts = [[0, 0, 0, 0],
                   [0, 0, 0, 0],
                   [0, 0, 0, 0],
                   [0, 0, 0, 0]]
        self.init_tiles()

    def init_tiles(self):
        self.fill_tiles(10)

    def fill_tiles(self, num):
        spaces = avail(self.ts)
        random.shuffle(spaces)
        for row, col in spaces[:num]:
            self.ts[row][col] = random_num()
        draw(self.ts)

    def update_tiles(self):
        self.fill_tiles(2)

    def update_text(self):
        key_names = [pyglet.window.key.symbol_string(k) for k in self.keys_pressed]
        text = 'Keys: ' + ','.join(key_names)
        # Update self.text
        self.text.element.text = text
        if key_names.count('DOWN') > 0:
            self.ts = down(self.ts)
            self.update_tiles()
        if key_names.count('UP') > 0:
            self.ts = up(self.ts)
            self.update_tiles()
        if key_names.count('LEFT') > 0:
            self.ts = left(self.ts)
            self.update_tiles()
        if key_names.count('RIGHT') > 0:
            self.ts = right(self.ts)
            self.update_tiles()

    def on_key_press(self, key, modifiers):
        self.keys_pressed.add(key)
        self.update_text()

    def on_key_release(self, key, modifiers):
        self.keys_pressed.discard(key)
        self.update_text()


def random_num():
    seed = random.randint(0, 31);
    if seed < 16:
        return 2
    elif seed < 24:
        return 4
    elif seed < 28:
        return 8
    else:
        return 0


def draw(lines):
    print("step")
    print("|----|----|----|----|")
    for line in lines:
        print("|" + "|".join(map(lambda item: str(item).center(4), line)) + "|")
        print("|----|----|----|----|")


def avail(lines):
    avails = []
    for row, line in enumerate(lines):
        for col, item in enumerate(line):
            if item is 0:
                avails.append((row, col))
    return avails


def left(lines):
    new_lines = []
    for row, line in enumerate(lines):
        new_line = []
        for col, item in enumerate(line):
            if item != 0:
                new_line.append(item)
        last = None
        for col, item in enumerate(new_line):
            if item == last:
                new_line[col - 1] = item * 2
                for num in range(col, len(new_line) - 1):
                    new_line[num] = new_line[num + 1]
                new_line.pop(len(new_line) - 1)
                last = 0
            else:
                last = item
        for _ in range(len(new_line), 4):
            new_line.append(0)
        new_lines.append(new_line)
    return new_lines


def left_right_swap(lines):
    for row, line in enumerate(lines):
        line[0], line[1], line[2], line[3] = line[3], line[2], line[1], line[0]
    return lines


def up_down_swap(lines):
    return [lines[3], lines[2], lines[1], lines[0]]


def right(lines):
    lines = left_right_swap(lines)
    lines = left(lines)
    lines = left_right_swap(lines)
    return lines


def rotate90(lines):
    new_lines = row_col_swap(lines)
    new_lines = left_right_swap(new_lines)
    return new_lines


def row_col_swap(lines):
    new_lines = [[0, 0, 0, 0],
                 [0, 0, 0, 0],
                 [0, 0, 0, 0],
                 [0, 0, 0, 0]]
    for row in range(0, 4):
        for col in range(0, 4):
            new_lines[row][col] = lines[col][row]
    return new_lines


def rotate270(lines):
    new_lines = row_col_swap(lines)
    new_lines = up_down_swap(new_lines)
    return new_lines


def up(lines):
    lines = rotate270(lines)
    lines = left(lines)
    lines = rotate90(lines)
    return lines


def down(lines):
    lines = rotate90(lines)
    lines = left(lines)
    lines = rotate270(lines)
    return lines


class RectLayer(Layer):

    def __init__(self):
        super(RectLayer, self).__init__()

        g = cocos.draw.Segment



if __name__ == "__main__":
    director.init(resizable=True, width=10, height=10)
    #运行我们的事件演示程序场景:
    director.run(cocos.scene.Scene(KeyDisplay(),RectLayer()))
 

