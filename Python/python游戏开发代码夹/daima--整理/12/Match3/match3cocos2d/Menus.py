from cocos.menu import *
from cocos.director import director
from cocos.scenes.transitions import *
import pyglet


class MainMenu(Menu):
    def __init__(self):
        super(MainMenu, self).__init__('Match3')

        # 可以重写标题和项目所使用的字体
        # 也可以重写字体大小和颜色
        self.font_title['font_name'] = 'SimHei'
        self.font_title['font_size'] = 72
        self.font_title['color'] = (204, 164, 164, 255)

        self.font_item['font_name'] = 'SimHei',
        self.font_item['color'] = (32, 16, 32, 255)
        self.font_item['font_size'] = 32
        self.font_item_selected['font_name'] = 'SimHei'
        self.font_item_selected['color'] = (32, 100, 32, 255)
        self.font_item_selected['font_size'] = 46

        # 例如菜单可以垂直对齐和水平对齐
        self.menu_anchor_y = CENTER
        self.menu_anchor_x = CENTER
        items = []
        items.append(MenuItem('New Game', self.on_new_game))
        items.append(MenuItem('Quit', self.on_quit))
        self.create_menu(items, shake(), shake_back())
    def on_new_game(self):
        import GameView

        director.push(FlipAngular3DTransition(
            GameView.get_newgame(), 1.5))

    def on_options(self):
        self.parent.switch_to(1)

    def on_scores(self):
        self.parent.switch_to(2)

    def on_quit(self):
        pyglet.app.exit()
