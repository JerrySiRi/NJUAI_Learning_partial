'''
题目：[Python, 多继承] Mixins机制
题目描述：

民航飞机(CivilAircraft)、直升飞机(Helicopter)、轿车(Car)都是一个交通工具(Vehicle)
前两者都有一个功能是飞行fly，但是轿车没有，因此不能将飞行功能放到交通工具这个父类中。
我们可额外【定义一个FlyableMixin类，来完成Fly的功能】，让CivilAircraft和Helicopter【同时继承FlyableMixin和Vehicle】便完成了功能的添加。

通过继承的方式完成以下功能：
1. CivilAircraft 调用run()时，执行继承来的 run()和fly()**两个
2. Helicopter 调用run()时，执行继承来的 fly()**一个
3. Car 调用run()时，执行继承来的 run()**一个

提示：
python Mixin参考链接：https://zhuanlan.zhihu.com/p/95857866

样例输入：
CivilAircraft().run()
Car().run()
print(hasattr(CivilAircraft, "fly"))
print(Vehicle in CivilAircraft.__bases__)
exit()

样例输出：
CivilAircraft running
CivilAircraft flying
Car running
True
True

'''


class Vehicle:  # 交通工具
    def run(self):
        print(f"{self.__class__.__name__} running")


class FlyableMixin:
    def fly(self):
        '''
        复杂的飞行相关代码
        '''
        print(f"{self.__class__.__name__} flying")


# 在此处填写代码，补充完成各个类
# CivilAircraft, Helicopter, Car
class CivilAircraft(Vehicle, FlyableMixin):
    def run(self):
        Vehicle.run(self)
        FlyableMixin.fly(self)
class Helicopter(FlyableMixin,Vehicle):
    def run(self):
        FlyableMixin.fly(self)
class Car(Vehicle):
    def run(self):
        Vehicle.run(self)

# 测试用代码，请不要改动
while True:
    exec(input())