import cocos
import random
import pyglet
import sound

# import cocos.audio.pygame.music as music
# import cocos.audio.pygame.mixer as mixer

# 定义常量
MARGIN = 10  # 边框10像素
GRID = 20  # 默认单位格20像素, 用于放缩
PIXEL = 40  # 资源图片像素大小, 便于放缩和修改图片清晰度
NORTH = 0  # 北方
EAST = 1  # 东方
SOUTH = 2  # 南方
WEST = 3  # 西方

# 为res资源文件添加搜索路径
pyglet.resource.path = ["res"]
pyglet.resource.reindex()


class MainScene(cocos.layer.Layer):
    def __init__(self):  # 初始化主Scene
        super(MainScene, self).__init__()
        self.add(Grass())  # 载入Grass场景


class Grass(cocos.layer.Layer):
    is_event_handler = True  # 接收事件消息

    def __init__(self):  # 初始化Scene
        super(Grass, self).__init__()
        # 设置草地效果
        background = cocos.sprite.Sprite('background.jpg')
        background.position = 310, 220
        self.add(background)
        # 实例化一条蛇
        self.snake = Snake()
        self.add(self.snake)

    def on_key_press(self, key, modifiers):
        # print("KEYPRESSED")
        self.snake.key_pressed(key)


class Snake(cocos.cocosnode.CocosNode):
    # is_event_handler = True  # 为什么不可以在此接收时间消息?
    def __init__(self):
        super(Snake, self).__init__()
        # 初始化一些参数
        self.is_dead = False  # 控制死亡的flag
        self.speed = 0.2  # 1秒每帧
        # 初始化蛇的头部
        self.head = cocos.sprite.Sprite('head.png')
        self.head.scale = GRID / PIXEL
        self.head.direction_new = random.randint(0, 3)  # 随机取得初始方向
        self.head.rotation = (self.head.direction_new - 2) * 90
        self.head.direction_old = self.head.direction_new
        self.head.position = 10 * GRID + MARGIN + GRID / 2, 10 * GRID + MARGIN + GRID / 2
        self.add(self.head, z=1)
        # 初始化蛇身子
        self.body = []  # 创建一个list储存身子
        self.body.append(self.head)  # 把head对象的引用传进body, 便于访问
        # 预先添加三节身子
        for i in range(1, 4):
            a_body = cocos.sprite.Sprite('body.png')
            a_body.scale = GRID / PIXEL  # PIXEL为图片像素大小
            x = self.body[i - 1].position[0] + [0, -1, 0, 1][self.body[0].direction_new] * GRID
            y = self.body[i - 1].position[1] + [-1, 0, 1, 0][self.body[0].direction_new] * GRID
            a_body.position = x, y
            self.add(a_body)
            self.body.append(a_body)
        self.get_food = False  # 控制是否得到食物的flag
        # 放置食物
        self.food = cocos.sprite.Sprite('food.png')
        self.food.scale = GRID / PIXEL
        self.add(self.food)
        self.put_food()

        # 播放音乐
        self.music = sound.Sound()
        self.music.BGM_play(True)

        # 计分
        self.score = 0
        self.scoreLabel = cocos.text.Label('score: 0',
                                           font_name='Microsoft YaHei',
                                           font_size=9,
                                           color=(255, 215, 0, 255))
        self.scoreLabel.position = 15, 412
        self.add(self.scoreLabel)
        # 每隔SPEED 秒调用self.update()
        self.schedule_interval(self.update, self.speed)

    def put_food(self):
        # 随机放置食物
        while 1:
            position = (MARGIN + random.randint(0, 600 // GRID - 1) * GRID + GRID / 2,
                        MARGIN + random.randint(0, 400 // GRID - 1) * GRID + GRID / 2)
            if position not in [x.position for x in self.body]:  # 防止食物放到蛇身上
                break
        self.food.position = position

    def update(self, dt):
        # 刷新帧时的逻辑处理函数

        # 判断蛇头方向是否应该改变
        # NORTH=0, EAST=1, SOUTH=2, WEST=3
        if self.head.direction_old != self.head.direction_new:
            # 如果蛇头方向改变, 旋转蛇头图片
            self.head.rotation = (self.head.direction_new - 2) * 90  # 顺时针为正, 逆时针为负数, 用度衡量旋转角度
            self.head.direction_old = self.head.direction_new
        # 计算下一帧数的坐标 x,y
        x = self.head.position[0] + [0, 1, 0, -1][self.head.direction_new] * GRID
        y = self.head.position[1] - [-1, 0, 1, 0][self.head.direction_new] * GRID
        new_position = x, y
        # 判断是否将撞死
        if new_position[0] == MARGIN - GRID / 2 or new_position[1] == MARGIN - GRID / 2 or (
                        new_position[0] == MARGIN + GRID / 2 + 600 or new_position[
                    1] == MARGIN + GRID / 2 + 400):  # 检查是否撞墙
            self.crash()
            return
        for i in range(1, len(self.body) - 1):  # 检查是否撞到自己的身体
            if new_position == self.body[i].position:
                self.crash()
                return
        # 判断是否将得到食物, 是的话加一节蛇身子, 重新放置食物
        if new_position == self.food.position:
            self.gotfood()

        # 移动蛇
        # for i in range(len(self.body)-1, 0, -1):
        #    self.body[i].position=self.body[i-1].position
        # self.head.position=new_position
        # 改为只移动尾巴, 减少刷新次数, 可能会提高效率
        self.body[-1].position = self.head.position
        self.head.position = new_position
        self.body = [self.head] + self.body[-1:] + self.body[1:-1]

    def gotfood(self):
        # 添加boduy
        new_body = cocos.sprite.Sprite('body.png')
        new_body.position = self.body[-1].position
        new_body.scale = GRID / PIXEL
        self.add(new_body)
        self.body.append(new_body)
        # 随机放置食物
        self.put_food()
        # 加分
        self.score += 5
        self.scoreLabel.element.text = "score: " + str(self.score)
        # 播放吃到食物的音效
        self.music.getfood()
        # 提速, 加大游戏难度
        self.speed *= 0.95
        self.unschedule(self.update)
        self.schedule_interval(self.update, self.speed)

    def crash(self):
        # 撞死后的善后处理函数

        self.is_dead = True
        # 出现眩晕星星
        stars = cocos.sprite.Sprite("stars.png")
        stars.position = self.head.position
        stars.scale = GRID / PIXEL * 0.8
        stars.do(cocos.actions.Repeat(cocos.actions.Rotate(720, 2)))
        self.add(stars)
        # 背景音乐停止, 播放结束音
        self.music.gameover()
        # 卸载self.update()
        self.unschedule(self.update)

    def key_pressed(self, key):
        print("KEY PRESS")
        if key == 65361 and self.head.direction_old != EAST:  # 按下左方向键
            self.head.direction_new = WEST
        elif key == 65362 and self.head.direction_old != SOUTH:  # 按下上方向键
            self.head.direction_new = NORTH
        elif key == 65363 and self.head.direction_old != WEST:  # 按下右方向键
            self.head.direction_new = EAST
        elif key == 65364 and self.head.direction_old != NORTH:  # 下方向键
            self.head.direction_new = SOUTH


cocos.director.director.init(width=600 + MARGIN * 2, height=420 + MARGIN * 2, caption="Gluttonous snake")
cocos.director.director.run(cocos.scene.Scene(Grass()))
