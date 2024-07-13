import pygame

#写一个函数判断一个点是否在指定范围内
def is_rect(pos,rect):
    x,y =pos
    rx,ry,rw,rh = rect
    if (rx <= x <=rx+rw)and(ry <= y <= ry +rh):
        return True
    return False

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((600,600))
    screen.fill((255,255,255))
    pygame.display.set_caption('图片拖拽')
    #显示一张图片
    image = pygame.image.load('123.jpg')
    image_x=100
    image_y=100
    screen.blit(image,(image_x,image_y))
    pygame.display.flip()
    # 用来存储图片是否可以移动
    is_move =False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            # 鼠标按下，让状态变成可以移动
            if event.type == pygame.MOUSEBUTTONDOWN:
                w,h = image.get_size()
                if is_rect(event.pos,(image_x,image_y,w,h)):
                    is_move =True

            #鼠标弹起，让状态变成不可以移动
            if event.type == pygame.MOUSEBUTTONUP:
                is_move =False

            #鼠标移动事件
            if event.type ==pygame.MOUSEMOTION:
                if is_move:
                    screen.fill((255,255,255))
                    x,y = event.pos
                    image_w,image_h=image.get_size()
                    #保证鼠标在图片的中心
                    image_x=x-image_h/2
                    image_y=y-image_w/2
                    screen.blit(image,(image_x,image_y))
                    pygame.display.update()
