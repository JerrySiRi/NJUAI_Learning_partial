from direct.showbase.ShowBase import ShowBase

class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        # 创建窗口模式窗口并加载场景
        self.scene = self.loader.loadModel("models/environment")
        #重新绘制要渲染的模型
        self.scene.reparentTo(self.render)
        # 在模型上使用缩放和位置变换操作
        self.scene.setScale(0.25, 0.25, 0.25)
        self.scene.setPos(-8, 42, 0)

app = MyApp()
app.run()