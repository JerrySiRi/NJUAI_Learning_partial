#!/usr/bin/env python

# #在本课程中，我们将使用间隔模拟旋转木马。
#
# #旋转木马将使用hprInterval旋转，而4只熊猫将代表传统旋转木马上的马。这4只大熊猫将随着旋转木马旋转，并在它们的两极上下移动，间隔时间为LerpFunc。
#
# #最后，旋转木马的外缘也会有灯光
#
# #将通过按顺序按间隔切换纹理来打开和关闭
#
# #平行的

from direct.showbase.ShowBase import ShowBase
from panda3d.core import AmbientLight, DirectionalLight, LightAttrib
from panda3d.core import NodePath
from panda3d.core import LVector3
from direct.interval.IntervalGlobal import *  # Needed to use Intervals
from direct.gui.DirectGui import *

# Importing math constants and functions
from math import pi, sin


class CarouselDemo(ShowBase):

    def __init__(self):
        # 初始化我们从中继承的ShowBase类，它将创建一个窗口并设置呈现到其中所需的一切.
        ShowBase.__init__(self)

        # 创建屏幕标题
        self.title = OnscreenText(text="Panda3D: Tutorial - Carousel",
                                  parent=base.a2dBottomCenter,
                                  fg=(1, 1, 1, 1), shadow=(0, 0, 0, .5),
                                  pos=(0, .1), scale=.1)

        base.disableMouse()  # 允许手动定位摄像机
        camera.setPosHpr(0, -8, 2.5, 0, -9, 0)  # 设置摄像机的位置和方向

        self.loadModels()  # 加载添加一些基本照明和定位我们的模型
        self.setupLights()  #添加一些基本照明功能
        self.startCarousel()  # 创建所需的间隔，并使旋转木马进入运动状态

    def loadModels(self):
        # 加载传送带底座
        self.carousel = loader.loadModel("models/carousel_base")
        self.carousel.reparentTo(render)  # Attach it to render

        # 加载位于旋转木马外边缘上的建模灯光
        # （不是熊猫灯）
        # #有两组灯。在任何给定的时间，一组将具有“on”纹理，另一组将具有“off”纹理。
        self.lights1 = loader.loadModel("models/carousel_lights")
        self.lights1.reparentTo(self.carousel)

        # 装载第二组灯
        self.lights2 = loader.loadModel("models/carousel_lights")
        # 旋转第二组，这样它就不会和第一组重叠了
        self.lights2.setH(36)
        self.lights2.reparentTo(self.carousel)

        # 加载灯光的纹理。一种纹理用于“开”状态，另一种用于“关”状态。
        self.lightOffTex = loader.loadTexture("models/carousel_lights_off.jpg")
        self.lightOnTex = loader.loadTexture("models/carousel_lights_on.jpg")

        #创建列表self.pandas，在旋转木马上填充了4个虚拟节点
        self.pandas = [self.carousel.attachNewNode("panda" + str(i))
                       for i in range(4)]
        self.models = [loader.loadModel("models/carousel_panda")
                       for i in range(4)]
        self.moves = [0] * 4

        for i in range(4):
            # 设置第i个panda节点的位置和方向我们刚刚创建的位置的Z值将是熊猫的基准高度。
            # 标题乘以i，将每个熊猫放在旋转木马周围各自的位置
            self.pandas[i].setPosHpr(0, 0, 1.3, i * 90, 0, 0)

            #加载实际的panda模型，并将其作为其虚拟节点的父级
            self.models[i].reparentTo(self.pandas[i])
            # 设置距中心的距离。此距离基于在Maya中对旋转木马进行建模的方式
            self.models[i].setY(.85)

        # 加载环境（天空球体和地平面）
        self.env = loader.loadModel("models/env")
        self.env.reparentTo(render)
        self.env.setScale(7)

    # 熊猫照明光纤
    def setupLights(self):
        #创建一些灯光并将其添加到场景中。通过将灯光设置为“渲染”（render），它们会影响整个场景
        ambientLight = AmbientLight("ambientLight")
        ambientLight.setColor((.4, .4, .35, 1))
        directionalLight = DirectionalLight("directionalLight")
        directionalLight.setDirection(LVector3(0, 8, -2.5))
        directionalLight.setColor((0.9, 0.8, 0.9, 1))
        render.setLight(render.attachNewNode(directionalLight))
        render.setLight(render.attachNewNode(ambientLight))

        # 显式地将环境设置为不亮
        self.env.setLightOff()

    def startCarousel(self):
        # 在这里我们实际上创建了移动旋转木马的间隔
        #
        # #我们使用的第一种类型的间隔是直接从节点路径创建的
        #
        # #这个间隔告诉NodePath在20秒内将其方向（hpr）从当前值（0,0,0）更改为（360,0,0）。
        self.carouselSpin = self.carousel.hprInterval(20, LVector3(360, 0, 0))
        #一旦创建了一个间隔，我们需要告诉它实际移动。

        #使用 start() 播放间隔，使用loop（）让间隔重复。为了使旋转木马保持转动，我们使用loop（）
        self.carouselSpin.loop()

        # 开始使用LerpFunc间隔，在给定的时间内将线性插值（又名Lerp）传递给一个函数。

        # #在这种情况下，旋转木马上的马不会继续向上移动，而是突然停止，然后又继续向下移动。
        # 相反，他们开始的很慢，中间快，顶部慢。这个运动接近正弦波。
        # 这个LerpFunc调用函数scrativepanda（我们将在下面创建），它根据传入值的sin更改panda的高度。
        # 通过这种方式，通过线性改变函数的输入来实现非线性运动
        for i in range(4):
            self.moves[i] = LerpFunc(
                self.oscillatePanda,  #要调用的函数
                duration=3,  #3秒持续时间
                fromData=0,  # 起始值（弧度）
                toData=2 * pi,  # 结束值（2pi弧度=360度）
                # 传递给self.oscialtePanda的其他信息

                extraArgs=[self.models[i], pi * (i % 2)]
            )
            # 循序按运行间隔
            self.moves[i].loop()

        # 结合Sequence、Parallel、Func和Wait interval，在灯光上实现纹理变换以模拟灯光的打开和关闭。
        # 等待当前间隔结束后再播放下一个间隔。
        # 并行间隔播放一组在同一时间的间隔等待间隔，只是在给定的时间内什么都不做
        # Func interval只需进行一次函数调用，它们几乎不需要时间，所以不会引起序列等待。

        self.lightBlink = Sequence(
            # 在我们的序列的第一步中，我们将在一个灯光上设置“on”纹理，同时在另一个灯光上设置“off”纹理
            Parallel(
                Func(self.lights1.setTexture, self.lightOnTex, 1),
                Func(self.lights2.setTexture, self.lightOffTex, 1)),
            Wait(1),  # 等待1秒后，将同时切换纹理
            Parallel(
                Func(self.lights1.setTexture, self.lightOffTex, 1),
                Func(self.lights2.setTexture, self.lightOnTex, 1)),
            Wait(1)  # 我们再等一秒钟
        )

        self.lightBlink.loop()  # 连续循环此序列

    def oscillatePanda(self, rad, panda, offset):
        # 这是前面提到的振荡函数。它接受度值、设置高度的节点路径和偏移量。
        # 偏移量在那里，这样不同的熊猫就可以相对运动。.2是振幅，所以熊猫的高度在-.2到.2之间变化
        panda.setZ(sin(rad + offset) * .2)

demo = CarouselDemo()
demo.run()
