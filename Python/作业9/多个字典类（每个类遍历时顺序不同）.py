'''
如果实现多个字典类，每个类遍历时的顺序并不相同（比如，key从小到大、key从大到小，value从小到大、value从大到小等）
如何设计可以尽可能的提升代码复用，减少重复开发。
'''

'''
错误1
class A():
    print("a类")
class B(A):
    print("b类")
class C(B, A):
    print("c类")

test = C()
由于c的父类B也继承了A,导致出现了重复继承，所以无法创建一致的方法：Cannot create a consistent method resolution

'''
'''
错误2
eval函数的参数必须为字符串，否则将报错
eval()的参数形式为字符串或字符串变量，在程序中可以将字符串形式的输入值转化为数字进行计算。
'''
'''
错误3
通过字典的键访问值的时候，[]中需要是一个string类型，或者是一个返回值是string类型的函数。

》》所以只能通过类似函数调用的方式，让self.strr在dict2[]之中呢！
'''

class keymin(dict):
    def __init__(self,dict1):
        self.dictt=dict1#这个对象的字典
        self.strr='kmin'
    def sorting(self):
        dict2={'kmin':list(sorted(self.dictt.keys())),'kmax':list(reversed(sorted(self.dictt.keys()))),
               'vmin':list(sorted(self.dictt.values())),'vmax':list(reversed(sorted(self.dictt.values())))}
        return dict2[self.strr]

    def ranging(self):
        c=self.sorting()#返回的是一个列表
        d={}
        for i in c:
            d[i]=self.dictt[i]
        print(d)

class keymax(keymin):
    def __init__(self, dict1):
        keymin.__init__(self,dict1)  # 这个对象的字典，通过父类来进行初始化！
        self.strr = 'kmax'

class valuemin(keymin):
    def __init__(self, dict1):
        self.dictt = dict1  # 这个对象的字典
        self.strr = 'vmin'

    def ranging(self):
        c = self.sorting()  # 返回的是一个列表,是值从小到大的排列
        d = {}
        for i in c:
            for j in self.dictt.keys():
                if self.dictt[j]==i:
                    d[j]=i
        print(d)

class valuemax(valuemin):
    def __init__(self, dict1):
        self.dictt = dict1  # 这个对象的字典
        self.strr = 'vmax'

a={1:2,6:5,3:14,8:3}
key1=keymin(a)
key1.ranging()

key2=keymax(a)
key2.ranging()

key3=valuemin(a)
key3.ranging()

key4=valuemax(a)
key4.ranging()

