import pygame
from pygame.locals import *
from sys import exit
 
pygame.init()    					#初始化pygame,为使用硬件做准备
#下行代码创建了一个窗口
screen = pygame.display.set_mode((640, 480), 0, 32)
font = pygame.font.SysFont("stxihei", 40)		#设置字体和大小
#设置文本内容和颜色
text_surface = font.render(u"古城遗迹", True, (0, 0, 255))
x = 0                            		#设置显示文本的水平坐标
y = (480 - text_surface.get_height())/2 		 #设置显示文本的垂直坐标
background = pygame.image.load("bg.jpg").convert()  #加载并转换图像
while True:                      		#游戏主循环
    for event in pygame.event.get():
        if event.type == QUIT:      		#接收到退出事件后退出程序
            exit()
    screen.blit(background, (0, 0))   		#将背景图画上去
    x -= 1                   		#设置文字滚动速率，如果文字滚动太快，可以尝试更改这个数字
    if x < -text_surface.get_width():
        x = 640 - text_surface.get_width()
    screen.blit(text_surface, (x, y))
    pygame.display.update()
