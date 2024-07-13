import pygame,sys
from random import *
pygame.init()
class Car(pygame.sprite.Sprite):
    def __init__(self,filename,initial_position,speed):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load(filename)
        self.rect=self.image.get_rect()
        self.rect.topleft=initial_position
        self.speed=speed
    def move(self):
        self.rect=self.rect.move(self.speed)
        if self.rect.bottom < 0:   #当小车底部到达窗口顶部时，让小车从下面出来
            self.rect.top=480
screen=pygame.display.set_mode([640,480])
screen.fill([255,255,255])
fi='ok1.jpg'
locationgroup=([150,200],[350,300],[250,200])
Cargroup=pygame.sprite.Group()
for lo in locationgroup:
    speed=[0,choice([-10,-1])]
    Cargroup.add(Car(fi,lo,speed))

while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            sys.exit()
    pygame.time.delay(20)
    screen.fill([255,255,255])
    for carlist in Cargroup.sprites():
        carlist.move()
        screen.blit(carlist.image,carlist.rect)
    pygame.display.update()