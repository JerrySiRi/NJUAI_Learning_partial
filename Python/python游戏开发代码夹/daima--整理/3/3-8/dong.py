background_image_filename = 'bg.jpg'
import pygame, sys
from pygame.locals import *

pygame.init()

FPS = 30 # 设置每秒帧数
fpsClock = pygame.time.Clock()

#设置窗体
DISPLAYSURF = pygame.display.set_mode((714, 300), 0, 32)
pygame.display.set_caption('Animation')
background = pygame.image.load(background_image_filename).convert()

WHITE = (255, 255, 255)
catImg = pygame.image.load('cat.png')
catx = 10
caty = 10
direction = 'right'

while True: # the main game loop
    DISPLAYSURF.blit(background, (0, 0))
    if direction == 'right':
        catx += 5
        if catx == 280:
            direction = 'down'
    elif direction == 'down':
        caty += 5
        if caty == 220:
            direction = 'left'
    elif direction == 'left':
        catx -= 5
        if catx == 10:
            direction = 'up'
    elif direction == 'up':
        caty -= 5
        if caty == 10:
            direction = 'right'

    DISPLAYSURF.blit(catImg, (catx, caty))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    fpsClock.tick(FPS)
