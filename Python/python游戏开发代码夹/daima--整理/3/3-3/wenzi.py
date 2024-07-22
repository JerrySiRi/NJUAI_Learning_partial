import pygame
from random import randint

def static_page(screen):
    # 页面上显示静态内容
    # 静态文字
    font = pygame.font.SysFont('stxihei',40)
    title = font.render('开发游戏',True,(0,0,0))
    screen.blit(title,(200,200))

def animation_title(screen):
    # 字体颜色变化
    font = pygame.font.SysFont('Time', 40)
    title = font.render('happy birthday', True, (randint(0,255), randint(0,255), randint(0,255)))
    screen.blit(title, (100, 100))

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((600,600))
    screen.fill((255,255,255))

    static_page(screen)

    pygame.display.flip()

    while True:

        # for里面的代码只有事件发生后才会执行
        for event in pygame.event.get():
            if event.type ==pygame.QUIT:
                exit()

        # 在下面写每一针要显示的内容
        """
        程序执行到这个位置，CPU休息一会再执行，就是阻塞一段时间
        单位：毫秒 （1000ms == 1s）
        """
        pygame.time.delay(150)
        screen.fill((255,255,255))
        static_page(screen)
        animation_title(screen)

        # 内容占上市到完成后，更新到屏幕上
        pygame.display.update()
