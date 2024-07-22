import pygame
import sys
from pygame.locals import *

background_image_filename = 'bg.jpg'
pygame.mixer.init()
pygame.mixer.music.load("fade.ogg")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play()  # 开始播放
bird_sound = pygame.mixer.Sound("loser.wav")
bird_sound.set_volume(0.2)
dog_sound = pygame.mixer.Sound("winner.wav")
dog_sound.set_volume(0.2)
bg_size = width, height = 710, 506
screen = pygame.display.set_mode(bg_size)
background = pygame.image.load(background_image_filename).convert()
pygame.display.set_caption("MusicPlayDemo")
pause = False

pause_image = pygame.image.load("play.png").convert_alpha()
unpause_image = pygame.image.load("stop.png").convert_alpha()
pause_rect = pause_image.get_rect()
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()

        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                # 鼠标按左键播放一种声
                dog_sound.play()
            if event.button == 3:
                # 鼠标按右键播放一种声
                bird_sound.play()
    screen.fill((255, 255, 255))
    screen.blit(background, (0, 0))
    if pause:
        screen.blit(pause_image, pause_rect)
        pygame.mixer.music.pause()
    else:
        screen.blit(unpause_image, pause_rect)
        pygame.mixer.music.unpause()

    pygame.display.flip()

    clock.tick(30)
