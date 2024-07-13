from math import pi, sin, cos
from direct.showbase.ShowBase import ShowBase
from direct.task import Task

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        #加载场景模型
        self.scene = self.loader.loadModel("models/environment")
        # 重新绘制要渲染的模型
        self.scene.reparentTo(self.render)
        # 在模型上使用缩放和位置变换操作
        self.scene.setScale(0.25, 0.25, 0.25)
        self.scene.setPos(-8, 42, 0)

        # 将通知任务管理器调用SpinCameraTask控制相机
        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")

    # 设置相机的移动过程
    def spinCameraTask(self, task):
        angleDegrees = task.time * 6.0
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(20 * sin(angleRadians), -20 * cos(angleRadians), 3)
        self.camera.setHpr(angleDegrees, 0, 0)
        return Task.cont

app = MyApp()
app.run()