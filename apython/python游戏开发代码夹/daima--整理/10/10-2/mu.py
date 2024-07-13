from math import pi, sin, cos
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # 禁用鼠标
        self.disableMouse()
        # 载入环境模型
        self.environ = self.loader.loadModel("models/environment")
        # 设置环境模型的父实例
        self.environ.reparentTo(self.render)
        # 对模型进行比例及位置调整
        self.environ.setScale(0.25, 0.25, 0.25)
        self.environ.setPos(-8, 42, 0)

        # 通知任务管理器调用SpinCameraTask控制相机
        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")

        # 载入熊猫角色
        self.pandaActor = Actor("models/panda-model",
        {"walk": "models/panda-walk4"})
        self.pandaActor.setScale(0.005, 0.005, 0.005)
        self.pandaActor.reparentTo(self.render)

        # 动画循环
        self.pandaActor.loop("walk")

        # 创建四幕
        PosInterval1 = self.pandaActor.posInterval(13,
        Point3(0, -10, 0),
        startPos=Point3(0, 10, 0))
        PosInterval2 = self.pandaActor.posInterval(13,
        Point3(0, 10, 0),
        startPos=Point3(0, -10, 0))
        HprInterval1 = self.pandaActor.hprInterval(3,
        Point3(180, 0, 0),
        startHpr=Point3(0, 0, 0))
        HprInterval2 = self.pandaActor.hprInterval(3,
        Point3(0, 0, 0),
        startHpr=Point3(180, 0, 0))

        # 创建情节并运行四幕
        self.pandaPace = Sequence(PosInterval1,
        HprInterval1,
        PosInterval2,
        HprInterval2,
        name="pandaPace")
        self.pandaPace.loop()

        # 定义旋转相机
    def spinCameraTask(self, task):
        angleDegrees = task.time * 6.0
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(20 * sin(angleRadians), -20.0 * cos(angleRadians), 3)
        self.camera.setHpr(angleDegrees, 0, 0)
        return Task.cont

app = MyApp()
app.run()