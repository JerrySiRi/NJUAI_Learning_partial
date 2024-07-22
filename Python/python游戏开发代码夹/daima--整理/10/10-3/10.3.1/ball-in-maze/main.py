#!/usr/bin/env python

# 这个教程展示了如何检测和响应碰撞。它使用在代码中创建的实体和鸡蛋文件，如何设置碰撞掩码，遍历器，和处理器，
# 如何检测碰撞，以及如何根据碰撞来调度功能。所有这些都是用来模拟迷宫式游戏的。

from direct.showbase.ShowBase import ShowBase
from panda3d.core import CollisionTraverser, CollisionNode
from panda3d.core import CollisionHandlerQueue, CollisionRay
from panda3d.core import Material, LRotationf, NodePath
from panda3d.core import AmbientLight, DirectionalLight
from panda3d.core import TextNode
from panda3d.core import LVector3, BitMask32
from direct.gui.OnscreenText import OnscreenText
from direct.interval.MetaInterval import Sequence, Parallel
from direct.interval.LerpInterval import LerpFunc
from direct.interval.FunctionInterval import Func, Wait
from direct.task.Task import Task
import sys

# 常量
ACCEL = 70         # 加速度
MAX_SPEED = 5      # 最大速度
MAX_SPEED_SQ = MAX_SPEED ** 2  # 平方
# Instead of length


class BallInMazeDemo(ShowBase):

    def __init__(self):
        # 初始化我们继承的SkyBASE类，它将创建一个窗口并设置我们所需要的渲染到其中的所有内容。
        ShowBase.__init__(self)

        # 将标题和指令文本置于屏幕上。
        self.title = \
            OnscreenText(text="Panda3D: Ball",
                         parent=base.a2dBottomRight, align=TextNode.ARight,
                         fg=(1, 1, 1, 1), pos=(-0.1, 0.1), scale=.08,
                         shadow=(0, 0, 0, 0.5))
        self.instructions = \
            OnscreenText(text="shubiao",
                         parent=base.a2dTopLeft, align=TextNode.ALeft,
                         pos=(0.05, -0.08), fg=(1, 1, 1, 1), scale=.06,
                         shadow=(0, 0, 0, 0.5))

        self.accept("escape", sys.exit)  #离开程序

        #禁用默认的基于鼠标的相机控制。这是我们继承的SkyBASE类的一种方法。.
        self.disableMouse()
        camera.setPosHpr(0, 0, 25, 0, -90, 0)  # Place the camera

        # 加载迷宫并将其放置在场景中
        self.maze = loader.loadModel("models/maze")
        self.maze.reparentTo(render)

        # 大多数时候，你希望通过不可见的几何形状来测试碰撞，而不是测试每个多边形。
        # 这是因为对场景中的每一个多边形的测试通常都太慢。固体可以简化或近似几何，仍然可以得到良好的结果。

        # 查找名为Walth-CulrDE的碰撞节点
        self.walls = self.maze.find("**/wall_collide")

        #使用位图对冲突对象进行排序，将使我们想要的球与包含比特0碰撞
        self.walls.node().setIntoCollideMask(BitMask32.bit(0))
        # 碰撞节点通常是看不见的，但可以显示出来。现在会找到孔的触发器并将它们的面具设置为0。
        # 我们也设置他们的名字，使他们更容易识别碰撞


        self.loseTriggers = []
        for i in range(6):
            trigger = self.maze.find("**/hole_collide" + str(i))
            trigger.node().setIntoCollideMask(BitMask32.bit(0))
            trigger.node().setName("loseTrigger")
            self.loseTriggers.append(trigger)


        #地面碰撞是与迷宫中的地面相同的平面上的一个多边形。我们将用一个射线来与它碰撞，
        # 这样我们就能准确地知道在每一个帧上放置什么高度。
        # 因为这不是我们希望球本身碰撞的东西，它有一个不同的位掩码。
        self.mazeGround = self.maze.find("**/ground_collide")
        self.mazeGround.node().setIntoCollideMask(BitMask32.bit(1))

        # 加载球并将它附加到场景上，它是在根虚拟节点上，这样我们就可以旋转球本身而不旋转将附着在它上的光线。
        self.ballRoot = render.attachNewNode("ballRoot")
        self.ball = loader.loadModel("models/ball")
        self.ball.reparentTo(self.ballRoot)

        # 找到碰撞球，这是在egg文件中创建的，它有一个来自0位的碰撞掩码，
        # 一个是无位碰撞掩码。这意味着球只能引起碰撞，不能碰撞。
        self.ballSphere = self.ball.find("**/ball")
        self.ballSphere.node().setFromCollideMask(BitMask32.bit(0))
        self.ballSphere.node().setIntoCollideMask(BitMask32.allOff())

        # 创建了一个光线，从球上面开始向下投射。这是为了确定球的高度和地板的角度。
        self.ballGroundRay = CollisionRay()     # 创建光线
        self.ballGroundRay.setOrigin(0, 0, 10)    # 设置原点
        self.ballGroundRay.setDirection(0, 0, -1)  # 设置方向
        # 碰撞实体进入碰撞节点创建并命名节点
        self.ballGroundCol = CollisionNode('groundRay')
        self.ballGroundCol.addSolid(self.ballGroundRay)  # 添加光线
        self.ballGroundCol.setFromCollideMask(
            BitMask32.bit(1))  # 设置口罩
        self.ballGroundCol.setIntoCollideMask(BitMask32.allOff())
        # 将球连接到球底部，使光线与球相对应（它总是在球上10英尺，向下点）。
        self.ballGroundColNp = self.ballRoot.attachNewNode(self.ballGroundCol)

        self.cTrav = CollisionTraverser()

        self.cHandler = CollisionHandlerQueue()
        #现在我们添加碰撞节点，这些冲突节点可以向遍历器创建冲突。
        # 遍历器将将这些与场景中的所有其他节点进行比较。
        self.cTrav.addCollider(self.ballSphere, self.cHandler)
        self.cTrav.addCollider(self.ballGroundColNp, self.cHandler)

        # 碰撞穿越器有一个内置的工具来帮助可视化碰撞
        ambientLight = AmbientLight("ambientLight")
        ambientLight.setColor((.55, .55, .55, 1))
        directionalLight = DirectionalLight("directionalLight")
        directionalLight.setDirection(LVector3(0, 0, -1))
        directionalLight.setColor((0.375, 0.375, 0.375, 1))
        directionalLight.setSpecularColor((1, 1, 1, 1))
        self.ballRoot.setLight(render.attachNewNode(ambientLight))
        self.ballRoot.setLight(render.attachNewNode(directionalLight))

        # 增加一个镜面高亮度的球，使它看起来有光泽。通常，这是在.egg文件中指定的。
        m = Material()
        m.setSpecular((1, 1, 1, 1))
        m.setShininess(96)
        self.ball.setMaterial(m, 1)

        #调用start以进行初始化
        self.start()

    def start(self):
        # 迷宫模型中也有一个定位器，用于在哪里启动球来访问它，我们使用find命令。
        startPos = self.maze.find("**/start").getPos()
        #把球放在起始位置
        self.ballRoot.setPos(startPos)
        self.ballV = LVector3(0, 0, 0)         # 初始速度为 0
        self.accelV = LVector3(0, 0, 0)        # 初始加速度为 0

        # 创建移动任务，但首先确保它尚未运行
        taskMgr.remove("rollTask")
        self.mainLoop = taskMgr.add(self.rollTask, "rollTask")

    # 处理光线与地面之间的碰撞
    def groundCollideHandler(self, colEntry):
        # 将球设置到适当的Z值，以使其准确地位于地面上。
        newZ = colEntry.getSurfacePoint(render).getZ()
        self.ballRoot.setZ(newZ + .4)

        # 求加速度方向。首先将表面法线与上矢相交，得到垂直于斜率的矢量。
        norm = colEntry.getSurfaceNormal(render)
        accelSide = norm.cross(LVector3.up())
        # 矢量与曲面法线相交，得到一个指向斜坡的矢量。
        # 通过在3D中获得加速度，而不是在2D中，我们减少了每帧的误差量，减少抖动。
        self.accelV = norm.cross(accelSide)

    # 处理球与墙之间的碰撞。
    def wallCollideHandler(self, colEntry):
        # 首先我们计算一些数字，需要做一个反射。
        norm = colEntry.getSurfaceNormal(render) * -1  # 墙面标准线
        curSpeed = self.ballV.length()                # 当前速度
        inVec = self.ballV / curSpeed                 # 运动方向
        velAngle = norm.dot(inVec)                    # 角度
        hitDir = colEntry.getSurfacePoint(render) - self.ballRoot.getPos()
        hitDir.normalize()
        # 球与墙标准线线之间的夹角
        hitAngle = norm.dot(hitDir)

        # 如果球已经从墙上移开，如果碰撞没有死亡（避免在拐角处被抓住），就忽略碰撞。
        if velAngle > 0 and hitAngle > .995:
            # 标准反射方程
            reflectVec = (norm * norm.dot(inVec * -1) * 2) + inVec

            self.ballV = reflectVec * (curSpeed * (((1 - velAngle) * .5) + .5))
            # 因为我们有一个碰撞，球已经有点埋在墙壁。这就计算了移动它所需要的向量。正好接触墙壁
            disp = (colEntry.getSurfacePoint(render) -
                    colEntry.getInteriorPoint(render))
            newPos = self.ballRoot.getPos() + disp
            self.ballRoot.setPos(newPos)

    # 这是处理一切滚动的任务
    def rollTask(self, task):
        #查找上次帧后的时间量的标准技术
        dt = globalClock.getDt()

        #如果这个函数运行，就会使球离开场景，所以忽略框架。
        if dt > .2:
            return Task.cont

        # 碰撞处理程序收集碰撞。我们根据碰撞的名称来调度处理碰撞的功能。
        for i in range(self.cHandler.getNumEntries()):
            entry = self.cHandler.getEntry(i)
            name = entry.getIntoNode().getName()
            if name == "wall_collide":
                self.wallCollideHandler(entry)
            elif name == "ground_collide":
                self.groundCollideHandler(entry)
            elif name == "loseTrigger":
                self.loseGame(entry)

        # 读取鼠标位置并相应地倾斜迷宫
        if base.mouseWatcherNode.hasMouse():
            mpos = base.mouseWatcherNode.getMouse()  # 获取鼠标位置
            self.maze.setP(mpos.getY() * -10)
            self.maze.setR(mpos.getX() * 10)

        # 移动小球
        # 基于加速度的速度更新
        self.ballV += self.accelV * dt * ACCEL
        # 将速度加速到最大速度
        if self.ballV.lengthSquared() > MAX_SPEED_SQ:
            self.ballV.normalize()
            self.ballV *= MAX_SPEED
        #基于速度更新位置
        self.ballRoot.setPos(self.ballRoot.getPos() + (self.ballV * dt))

        # 旋转球。它使用一个叫做四元数的物体来绕任意轴旋转球。
        # 该轴垂直于球的旋转，并且旋转量与球的大小有关，这是乘以上一次的旋转来间接地旋转它。
        prevRot = LRotationf(self.ball.getQuat())
        axis = LVector3.up().cross(self.ballV)
        newRot = LRotationf(axis, 45.5 * dt * self.ballV.length())
        self.ball.setQuat(prevRot * newRot)

        return Task.cont       # 无限期地完成任务

    # 如果球击中了一个洞触发，那么它应该落在洞里。
    def loseGame(self, entry):
        # 触发器被设置成使得球的中心应该移动到洞中的碰撞点
        toPos = entry.getInteriorPoint(render)
        taskMgr.remove('rollTask')  # Stop the maze task

        # 在很短的时间内把球移到洞里。然后等待一秒钟并开始重启游戏
        Sequence(
            Parallel(
                LerpFunc(self.ballRoot.setX, fromData=self.ballRoot.getX(),
                         toData=toPos.getX(), duration=.1),
                LerpFunc(self.ballRoot.setY, fromData=self.ballRoot.getY(),
                         toData=toPos.getY(), duration=.1),
                LerpFunc(self.ballRoot.setZ, fromData=self.ballRoot.getZ(),
                         toData=self.ballRoot.getZ() - .9, duration=.2)),
            Wait(1),
            Func(self.start)).start()

#最后，创建类的实例并开始3D渲染
demo = BallInMazeDemo()
demo.run()
