'''
题目：[Python, OOP] 简单工厂模式
题目描述：
描述：工厂模式，顾名思义就是我们可以通过一个指定的“工厂”获得需要的“产品”，在设计模式中主要用于抽象对象的创建过程，让用户可以指定自己想要的对象而不必关心对象的实例化过程。
这样做的好处是用户只需通过固定的接口而不是直接去调用类的实例化方法来获得一个对象的实例，隐藏了实例创建过程的复杂度，解耦了生产实例和使用实例的代码，降低了维护的复杂性。
我们需完成以下功能：
1. 定义一个员工的抽象基类：初始化员工的信息，定义一个work()的抽象基类方法（已实现好）。
2. 定义不同的【角色类】【继承】抽象基类，【重写】抽象基类方法work()，完成不同功能。
3. 定义产生员工的【工厂类】：定义一个工厂方法接受参数，返回【不同的员工实例对象】。（返回的是一个对象！！！）


样例输入：
engineer = EmployeeFactory.create('engineer', '张三', 30, '男')
print(engineer)
print(isinstance(engineer, Employee))
print(isinstance(engineer, Engineer))
print(engineer.work(1, 2, 3))
exit()
样例输出：
Engineer: 张三, 30 years old 男
True
True
6
'''

from abc import abstractmethod, ABC


# 工厂模式
class Employee(ABC):
    """员工抽象基类，无需修改"""
    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender
    @abstractmethod#函数装饰器，注入了abstractmethod的函数功能
    def work(self, *args):
        pass
    def __str__(self):
        return f"{self.__class__.__name__}: {self.name}, {self.age} years old {self.gender}"


class Engineer(Employee):#/////如果一个对象是Engineer或者Enployee的实例对象的话，isinstance都会返回True的！.父类的父类仍然是父类
    #用父类的初始化函数，不需要自己再去写一个啦
    def work(self,*args):#//////如果这个地方写成了sum，就没有在这个对象之中创建专门属于这个对象的数据成员，只是在函数运行过程中产生了一个临时变量
                        #//////在local frame中产生的变量，对象函数调用完之后这个sum自动消失，外部没有办法通过self.sum进行访问
        self.sum=0
        for i in args:
            self.sum=self.sum+i
        return self.sum
    """继承抽象基类"""
    # 填写代码，重写抽象方法: work(), 完成args求和


class Accountant(Employee):
    """继承抽象基类"""
    def work(self,*args):
        return max(args)
    # 填写代码，重写抽象方法: work(), 完成求args最大值


class Admin(Employee):
    """继承抽象基类"""
    def work(self,*args):
        return min(args)
    # 填写代码，重写抽象方法: work(), 完成求args最小值


class EmployeeFactory:
    """定义员工工厂类"""

    @classmethod
    def create(cls, sub_class_name, *args):
        """生成员工实例的工厂方法"""
        # 填写代码
        # 当sub_class_name == 'engineer'时 返回Engineer对象。返回的过程中应该完成返回对象的初始化参数传入
        # 当sub_class_name == 'accountant'时 返回Accountant对象
        # 当sub_class_name == 'admin'时 返回Admin对象
        if sub_class_name == 'engineer':
            return Engineer(*args)
        elif sub_class_name == 'accountant':
            return Accountant(*args)
        else:
            return Admin(*args)
        pass


while True:
    exec(input())