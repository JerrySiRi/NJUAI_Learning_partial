import pygame, sys
pygame.init()

class Car(pygame.sprite.Sprite):
    def __init__(self, filename, initial_position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename)
        self.rect = self.image.get_rect()
        # self.rect.topleft=initial_position
        self.rect.bottomright = initial_position
        print(self.rect.right)

screen = pygame.display.set_mode([640, 480])
screen.fill([255, 255, 255])
fi = 'bg.jpg'
b = Car(fi, [150, 100])
screen.blit(b.image, b.rect)
pygame.display.update()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()