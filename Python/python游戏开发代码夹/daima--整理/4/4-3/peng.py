import pygame
import sys
import math
from pygame.locals import *
from random import *


# 面向对象的编程方法，定义一个球的类型
class Ball(pygame.sprite.Sprite):
    def __init__(self, image, position, speed, bg_size):
        # 初始化动画精灵
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        # 将小球放在指定位置
        self.rect.left, self.rect.top = position
        self.speed = speed
        self.width, self.height = bg_size[0], bg_size[1]

    # 定义一个移动的方法
    def move(self):
        self.rect = self.rect.move(self.speed)
        # 如果小球的左侧出了边界，那么将小球左侧的位置改为右侧的边界
        # 这样便实现了从左边进入，右边出来的效果
        if self.rect.right < 0:
            self.rect.left = self.width
        if self.rect.left > self.width:
            self.rect.right = 0
        if self.rect.bottom < 0:
            self.rect.top = self.height
        if self.rect.top > self.height:
            self.rect.bottom = 0


def collide_check(item, target):
    col_balls = []
    for each in target:
        distance = math.sqrt(
            math.pow((item.rect.center[0] - each.rect.center[0]), 2) +
            math.pow((item.rect.center[1] - each.rect.center[1]), 2))
        if distance <= (item.rect.width + each.rect.width) / 2:
            col_balls.append(each)

    return col_balls


def main():
    pygame.init()

    ball_image = 'ball.png'
    bg_image = 'background.png'
    running = True

    # 根据背景图片指定游戏界面尺寸
    bg_size = width, height = 1024, 500
    screen = pygame.display.set_mode(bg_size)
    pygame.display.set_caption('Collision Spheres')

    background = pygame.image.load(bg_image).convert_alpha()

    # 用来存放小球对象的列表
    balls = []

    # 创建6个位置随机，速度随机的小球
    BALL_NUM = 6
    for i in range(BALL_NUM):
        position = randint(0, width - 70), randint(0, height - 70)
        speed = [randint(1, 6), randint(1, 6)]
        ball = Ball(ball_image, position, speed, bg_size)
        while collide_check(ball, balls):
            ball.rect.left, ball.rect.top = randint(0, width - 70), randint(0, height - 70)

        balls.append(ball)

    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()

        screen.blit(background, (0, 0))

        for each in balls:
            each.move()
            screen.blit(each.image, each.rect)

        for i in range(BALL_NUM):
            item = balls.pop(i)

            if collide_check(item, balls):
                item.speed[0] = -item.speed[0]
                item.speed[1] = -item.speed[1]

            balls.insert(i, item)

        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()