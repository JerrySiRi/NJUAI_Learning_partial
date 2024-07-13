from cocos.sprite import Sprite
from cocos.tiles import load
from cocos.mapcolliders import RectMapCollider
from cocos.layer import ScrollingManager, ScrollableLayer, ColorLayer
from cocos.director import director
from cocos.scene import Scene
from cocos.actions import Action
from pyglet.window import key


#对于这个场景，我们将使用一个高矩形块的地图，我们不希望玩家能够通过，首先从初始化 director控制器开始写代码

director.init(width=700, height=500, autoscale=False, resizable=True)
#设置了键盘和滚动管理器
scroller = ScrollingManager()
keyboard = key.KeyStateHandler()

#将Cocos的处理程序推送到keyboard对象
director.window.push_handlers(keyboard)

# 加载tilemap地图
map_layer = load("assets/platformer_map.xml")['map0']
# 使用Cocos的XML规范来创建这个映射，创建一个扩展action类和新的RectMapCollider的操作
# RectMapCollider让我们与rectmap碰撞
class GameAction(Action, RectMapCollider):
    # 将添加一个函数用于设置何时开始，由于Action父类的结构方式，我使用了start函数而不是一个 __init__函数
    def start(self):
        # 将目标精灵的速度设置为零
        self.target.velocity = 0, 0

        # 告诉游戏我们的精灵开始在地面上
        self.on_ground = True
    def on_bump_handler(self, vx, vy):
        return (vx, vy)

    # 更新step函数
    def step(self, dt):
        # 首先，我们通过获取目标速度的方式来获得dx和dy值
        dx = self.target.velocity[0]
        dy = self.target.velocity[1]

        #现在让 x值等于它们告诉精灵向左或向右移动的量
        dx = (keyboard[key.RIGHT] - keyboard[key.LEFT]) * 250 * dt
        # 合并了左和右的值并放大

        # 如果player在地面上，如果按下了空格键则会跳起来。跳到空中的量相当于地心引力的作用
        if self.on_ground and keyboard[key.SPACE]:
            # 跳到空中的量相当于地心引力的作用
            dy = 1500

        # 对目标起着重力的作用
        dy -= 1500 * dt
        # 从delta y减去一个数字，在这个例子中我选择了1500，目的是使它回到地图的地面
        # 下面是目标碰撞的所有代码
        last_rect = self.target.get_rect()

        # 这是目标碰撞的所有代码，当我们把它复制到一个新的边界矩形中，我们可以改变它的值来匹配我们的数学运算
        new_rect = last_rect.copy()

        # 将新的X值加到旧的X值上（如果它向左移动，它就会减去）
        new_rect.x += dx

        # 把新的Y值加在旧的Y值上
        new_rect.y += dy * dt

        # 现在我们需要实际检查碰撞
        self.target.velocity = self.collide_map(map_layer, last_rect, new_rect, dy, dx)
        # 这行代码的作用是从RectMapCollider运行collide_map函数来计算新的dx和dy值，然后它将目标的速度设置为新的dx和dy值

        #我们通过查看之前的边界矩形y和当前的边界矩形y来检查它是否在地面上，如果它们都是一样的，我们就会知道目标没有离开地面！
        self.on_ground = bool(new_rect.y == last_rect.y)

        # 现在我们需要将目标的位置锚定在边界矩形的中间（否则目标不会移动）
        self.target.position = new_rect.center

        # 最后，我们将滚动条的焦点设置在播放器的中心（矩形的中心）
        scroller.set_focus(*new_rect.center) # The * sets the argument passed in as all of the required parameters


# 为精灵的图层创建另一个类SpriteLayer，注意住它必须是一个可滚动层
class SpriteLayer(ScrollableLayer):
    def __init__(self):
        super(SpriteLayer, self).__init__()

        # 就像上一个类一样，我们制作我们的精灵，让它做我们定义的动作
        self.sprite = Sprite("assets/img/grossini.png")
        self.add(self.sprite)
        self.sprite.do(GameAction())

# 在“main”代码中做的第一件事就是创建我们刚刚定义的层
sprite_layer = SpriteLayer()

# 要找到我标记为玩家开始的单元格，并将精灵设置为从那里开始。首先找到我标记的那个单元格，这需要检查地图映射的源代码
start = map_layer.find_cells(player_start=True)[0]

# 然后得到了有界矩形
rect = sprite_layer.sprite.get_rect()

# 设置精灵的有界矩形的中间底部等于起始单元格的中间底部
rect.midbottom = start.midbottom

# 最后我把精灵的位置设置在矩形的中心
sprite_layer.sprite.position = rect.center

#添加贴图，并将“z”设置为0
scroller.add(map_layer, z=0)
# 因为z是垂直轴，最高的z值层将始终显示在其他层的顶部

# 然后添加精灵，并将z设置为1，以便它显示在贴图层的顶部
scroller.add(sprite_layer, z=1)

# 然后做了一个颜色层，目的是给背景增添一点情趣（目前只是透明的）
bg_color = ColorLayer(52, 152, 219, 1000)

scene = Scene()
# And I add the scroller to it and put it on top of the stack of layers
scene.add(scroller, z=1)

# 添加了背景色（不需要定义z，因为默认值是0）
scene.add(bg_color)

director.run(scene)
