import pyglet


class Sound():
    def __init__(self):
        # 加载游戏背景音乐
        self.player1 = pyglet.media.Player()
        bgm = pyglet.media.load('res\\BGM.wav')
        self.player1.queue(bgm)

    def BGM_play(self, play=False):
        if play: # True则播放
            self.player1.play()
        else:    # False则暂停播放
            self.player1.pause()
    def gameover(self):
        self.player1.pause()
        pyglet.media.load('res\\gameover.wav').play()
    def getfood(self):
        pyglet.media.load('res\\getfood.wav').play()
