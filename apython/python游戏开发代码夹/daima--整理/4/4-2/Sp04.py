import pygame,sys
pygame.init()
class Car(pygame.sprite.Sprite):
    def __init__(self,filename,initial_position):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load(filename)
        self.rect=self.image.get_rect()
        self.rect.bottomright=initial_position
screen=pygame.display.set_mode([640,480])
screen.fill([255,255,255])
fi='ok1.jpg'
locationgroup=([150,200],[350,360],[250,280])
Cargroup=pygame.sprite.Group()
for lo in locationgroup:
    Cargroup.add(Car(fi,lo))

for carlist in Cargroup.sprites():
    screen.blit(carlist.image,carlist.rect)
pygame.display.update()
while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            sys.exit()