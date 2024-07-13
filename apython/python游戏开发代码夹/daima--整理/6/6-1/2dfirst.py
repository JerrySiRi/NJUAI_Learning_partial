import cocos

#自定义一个层
class HelloWorld(cocos.layer.Layer):
    def __init__(self):
        super( HelloWorld, self ).__init__()

        #新建文字标签用于显示Hello World
        label = cocos.text.Label('Hello, world',
                             #如果要显示中文,需要使用支持中文的字体,比如"微软雅黑"
                             font_name = 'Times New Roman',
                             font_size=32,
                             #设置锚点为正中间
                             anchor_x='center', anchor_y='center')
        #设置文字标签在层的位置.由于锚点为正中间,即"用手捏"标签的正中间,放到(320,240)的位置
        label.position = 320,240
        #把文字标签添加到层
        self.add( label )


#"导演诞生",即建一个窗口,默认是640*480,不可调整大小
cocos.director.director.init()

#建一个"场景",场景里只有一个hello_layer层,层里已自带文字
main_scene = cocos.scene.Scene( HelloWorld() )
#"导演说Action",让场景工作
cocos.director.director.run(main_scene)