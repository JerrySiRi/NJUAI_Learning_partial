from sys import exit
import pygame
import random
import math
background_image_filename = 'bg.jpg'
def random_color ():
    return (random.randint(0,255),random.randint(0,255),random.randint(0,255))

ball_x = 100
ball_y = 100
x_spead = 2
y_spead = 0

ball_x += x_spead
ball_y += y_spead

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((701,287))
    background = pygame.image.load(background_image_filename).convert()

    pygame.display.flip()
    all_balls = [
        {'r':random.randint(10,20),
         'pos':(100,100),
         'color': random_color(),
         'x_apeed':random.randint(-3,3),
         'y_apeed': random.randint(-3, 3)
         },
        {'r': random.randint(10, 20),
         'pos': (300, 300),
         'color': random_color(),
         'x_apeed': random.randint(-3, 3),
         'y_apeed': random.randint(-3, 3)
         }
]
    while True:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                #点一下鼠标创建一个球
                ball = {
                    'r':random.randint(10,25),
                     'pos':event.pos,
                    'color': random_color(),
                    'x_apeed':random.randint(-3,3),
                    'y_apeed': random.randint(-3, 3)
                }
            # 保存球
                all_balls.append(ball)

        screen.fill((255,255,255))
        screen.blit(background, (0, 0))
        for ball_dict in all_balls:
            #取出球原来的坐标和速度
            x,y=ball_dict['pos']
            x_speed = ball_dict['x_apeed']
            y_speed = ball_dict['y_apeed']
            x += x_speed
            y += y_speed
            if ball_x + 20 >= 600:
                ball_x = 600 - 20
                x_spead *= -1
            if ball_x + 20 <= 0:
                ball_x = 0
                x_spead *= -1
            if ball_y + 20 >= 400:
                ball_y = 400 - 20
                y_spead *= -1
            if ball_y + 20 <= 0:
                ball_y = 0
                y_spead *= -1

            pygame.draw.circle(screen,ball_dict['color'],(x,y),ball_dict['r'])
            #更新球的对应坐标
            ball_dict['pos'] = x,y

        pygame.display.update()
