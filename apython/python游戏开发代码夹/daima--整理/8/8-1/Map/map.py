#! /usr/bin/python
# -*- coding: utf-8 -*-
# 当加载一个地图时生成一个图层。
# 我们从初始化导演开始。这很重要，因为我们需要其他代码的主管来工作。
from cocos.tiles import load
from cocos.layer import ScrollingManager
from cocos.director import director
from cocos.scene import Scene
# 接下来开始加载地图，我们具体说明想加载什么层的地图
director.init()

MapLayer = load("assets/mapmaking.tmx")["map0"]
# 如果需要，检查资源件夹中的文件mapmaking.tmx ，看看我在哪里声明MAP0
# 否则，请确保您正确地将地图命名为平铺，并在加载函数之后引用括号中的名称。
# 这里有些新东西使用ScRunLink管理器对象来包含我的地图层
scroller = ScrollingManager()#ScrollingManager实现滚动功能
#从SCROLLIN管理器制作一个场景并在导演中运行它
scroller.add(MapLayer)
#运行图层
director.run(Scene(scroller))
