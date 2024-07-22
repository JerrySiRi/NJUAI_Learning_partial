import pygame# 导入pygame库
from pygame.locals import *
from random import randint       				#导入随机绘制模块
from sys import exit					# 向sys模块借一个exit函数用来退出程序
pygame.init()                  				#初始化pygame,为使用硬件做准备
  #下面一行用于创建一个窗口
screen = pygame.display.set_mode((640, 480), 0, 32)
while True:# 游戏主循环
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()# 接收到退出事件后退出程序
    #绘制随机点
    rand_col = (randint(0, 255), randint(0, 255), randint(0, 255))
    #screen.lock()
    for _ in range(100):                  			#遍历操作
        rand_pos = (randint(0, 639), randint(0, 479))
        screen.set_at(rand_pos, rand_col)   			#绘制一个点
    #screen.unlock()
    pygame.display.update()             			#刷新画面

