from cocos import scene
from cocos.layer import Layer
from cocos.director import director
from cocos.audio.pygame.mixer import Sound
from cocos.audio.pygame import mixer

# 首先需要为SDL Sound类创建一个包装器
# 我们通过创建自己的对象来实现这一点，该对象使用传入的文件名初始化父对象
class Audio(Sound):
    def __init__(self, audio_file):
        #们用传入的音频文件初始化super类
        super(Audio, self).__init__(audio_file)

# 在这里创建层
class AudioLayer(Layer):
    def __init__(self):
        super(AudioLayer, self).__init__()
        # 在层中从上面描述的类创建一个音频对象,设置使用音频文件“LatinIndustries.ogg”
        song = Audio("assets/sound/LatinIndustries.ogg")
        # 在初始化层时播放音频
        song.play(-1)  # 将参数设置为-1，表示无限期循环播放这个音频文件

director.init()
# 初始化mixer
mixer.init()
# 运行程序
director.run(scene.Scene(AudioLayer()))