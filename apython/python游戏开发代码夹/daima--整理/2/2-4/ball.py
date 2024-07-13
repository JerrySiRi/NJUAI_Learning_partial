import sys
import pygame
from pygame.locals import *

def control_ball(event):
    speed = [x, y] = [0, 0]  # 设置相对位移
    speed_offset = 1  # 小球的速度

    # 如果事件的类型是 键盘输入，就根据方向键来求出速度的方向（默认是从左往右为1，从上往下为1）
    if event.type == KEYDOWN:
        if event.key == pygame.K_LEFT:
            speed[0] -= speed_offset
            print
            event.key

        if event.key == pygame.K_RIGHT:
            speed[0] = speed_offset
            print
            event.key

        if event.key == pygame.K_UP:
            speed[1] -= speed_offset
            print
            event.key

        if event.key == pygame.K_DOWN:
            speed[1] = speed_offset
            print
            event.key
    # 如果没有方向键的输入，则速度为0，小球不动
    if event.type in (pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN):
        speed = [0, 0]

    return speed


# 主函数
def play_ball():
    pygame.init()  # 初始化
    window_size = Rect(0, 0, 684, 322)  # 设置窗口的大小

    screen = pygame.display.set_mode(window_size.size)  # 设置窗口模式
    pygame.display.set_caption('hello')  # 设置窗口标题
    ball_image = pygame.image.load('ball.jpg')  # 载入小球图片
    back_image = pygame.image.load('123.jpg')  # 载入背景图片
    ball_rect = ball_image.get_rect()  # 获取小球图片所在的区域

    while True:
        # 退出事件的处理
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()

        control_speed = control_ball(event)  # 获取到小球的方向
        ball_rect = ball_rect.move(control_speed).clamp(window_size)  # 小球按照方向移动，并且不会移出窗口。

        screen.blit(back_image, (0, 0))  # 设置窗口背景，位于（0,0）处，窗口左上角。
        screen.blit(ball_image, ball_rect)  # 把小球绘制到背景surface上。

        pygame.display.flip()  # 更新窗口内容


if __name__ == '__main__':
    play_ball()
