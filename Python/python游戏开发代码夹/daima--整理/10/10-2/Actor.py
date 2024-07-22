from direct.showbase.ShowBase import ShowBase  # 基本显示模块
from math import pi, sin, cos
from direct.task import Task  # 任务模块
from direct.actor.Actor import Actor  # 动态模块

class MyApp(ShowBase):
    def __init__(self):  # 场景初始化
        ShowBase.__init__(self)
        self.environ = self.loader.loadModel(r'models/environment')
        self.environ.reparentTo(self.render)  # self.render 渲染树根节点，设置之后才能对所有玄素进行渲染
        self.environ.setScale(0.25, 0.25, 0.25)
        self.environ.setPos(-8, 42, 0)
        self.taskMgr.add(self.spinCameraTask, 'SpinCameraTask')  # 调用任务spinCameraTask()
        self.panda()

    def spinCameraTask(self, task):  # 摄像机设置
        angleDegrees = task.time * 6
        angleRadians = angleDegrees * (pi / 180)
        self.camera.setPos(20 * sin(angleRadians), -20 * cos(angleRadians), 3)
        self.camera.setHpr(angleDegrees, 0, 0)
        return Task.cont

    def panda(self):  # 实现动态的熊猫
        self.pandaActor = Actor('models/panda-model', {'walk': 'models/panda-walk4'})
        self.pandaActor.setScale(0.005, 0.005, 0.005)
        self.pandaActor.reparentTo(self.render)  # self.render 渲染树根节点，设置以后才能对所有元素进行渲染
        self.pandaActor.loop('walk')

    def box(self):
        pass

app = MyApp()
app.run()