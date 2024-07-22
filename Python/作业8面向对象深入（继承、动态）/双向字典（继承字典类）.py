'''
题目：[Python,继承] 双向字典
题目描述：
描述：有时我们在使用字典数据结构时希望同时设置 d[k]=v和d[v]=k，例如分类任务中需分别构造id2name和name2id（类别名称与对应序号）的两个映射。
有没有一种方法使得字典自动构建这种双向映射呢？
下面我们将【继承python内置的dict类型】，实现【自定义的双向字典SymmetryDict】，满足：
1. [可通过传入一个普通dict进行初始化。]!!!
2. 支持del 删除操作，同时删除k,v 和v,k两对数据。如del aInfo[k]。两者同时删除了k和v为键的键值对了！！！
3. 支持[] 访问操作，获取和修改k,v对。如aInfo[k]=v.aInfo[v]=k。两者同时修改

提示：
1.可查看built-in dict 具有的方法，并重写，包括__setitem__, __delitem__方法，探索如何调用父类方法。
2.注意需设计[__init__--局部运用父类的init（）方法哦]方法，以支持使用普通dict进行初始化。【传入一个普通字典（构造函数的参数），生成一个双向字典（类的对象）！！】
3.******注意k,v相同的情况。
4.访问和删除操作保证k在字典中。


样例输入：
d = SymmetryDict({'cat':0, 'dog':1,'python':2})
print(d)
del d['dog']
print(d)
d[0]='python'
print(d['python'])
d[1]=1
print(d)
exit()
样例输出：
{'cat': 0, 0: 'cat', 'dog': 1, 1: 'dog'}
{'cat': 0, 0: 'cat'}
0
{0: 'python', 'python': 0, 1: 1}
'''
#以下为题目补充
'''
dir():
dir()用来查询一个[类]或者[对象]所有属性。（不给出具体方法）
help():
help()函数帮助我们了解[模块]、[类型]、[对象]、[方法]、[属性]的详细信息（给出具体方法）
'''

'''
使用---help(dict.__delitem__)
本题不需要这些函数具体如何实现，只需要调用这些函数就可以啦
dict中的内建函数:
【1】初始化函数
__init__(self, /, *args, **kwargs)
    Initialize self.  See help(type(self)) for accurate signature.
***[具体解释：在/之前的是位置参数，如果没有/，这个函数是不接受位置参数传递的。]
【2】依据传入键和值，在字典之中创建键-值得对应关系
__setitem__(self, key, value, /)
    Set self[key] to value.
【3】依据传入的键，在字典（self）之中删除这个键值对
__delitem__(self, key, /)
    Delete self[key].
'''
class SymmetryDict(dict):
    def __init__(self, items):
        a=items.items()#返回键值对元祖所构成的一个大列表
        c={}
        for i,j in a:
            c[i]=j
            c[j]=i
        dict.__init__(self,c)#super().__init__(c)

        # 填写代码
        pass

    def __setitem__(self, key, value):#加入新元素=对原来的键值对、值键对进行修改
        a=self.items()
        for i in a:
            if i[1]==value:
                b=i[0]#要把b作为键的元素删掉
        #要把key作为键的元素删掉
        if key in self.keys():#要删掉key作为键的，key的值作为键的！
            x=self[key]
            dict.__delitem__(self, key)
            dict.__delitem__(self,x)#如果写成self[key]就不对了！
#/////错误！#这种写法会报错的，因为在操作第一次删除之后就已经把key作为键的键值对删除了！
        #就找不到self[key]了！
        if value in self.keys():#如果前面传入了一毛一样的，现在就不进入if语句判断啦！
            dict.__delitem__(self,value)
            dict.__delitem__(self,b)
        dict.__setitem__(self,key,value)
        dict.__setitem__(self,value,key)
        # 填写代码
        pass

    def __delitem__(self,key):
        a=self[key]
        if a!=key:
            dict.__delitem__(self, key)
            dict.__delitem__(self, a)
        else:
            dict.__delitem__(self, key)


        # 填写代码
        pass
while True:
    exec(input())
'''
def __setitem__(self, key, value)做出以下修改的原因：
如果输入为：
d = SymmetryDict({'cat':0, 'dog':1,'python':2})
print(d)
del d['dog']
print(d)
d[0]='python'
print(d['python'])
d[1]=1
print(d)
exit()

输出应该为：
{'cat': 0, 0: 'cat', 'dog': 1, 1: 'dog', 'python': 2, 2: 'python'}
{'cat': 0, 0: 'cat', 'python': 2, 2: 'python'}
0
{0: 'python', 'python': 0, 1: 1}

但是一开始的代码，保留了cat作为键以及python作为键的情况。》》少考虑了两种情况！
'''
'''
def __delitem__(self,key)做出改变的原因：
如果删除的键值对之中的键和值相同，如果重复删除的话，没得可删了！
nzec是没有输出！一般都会出现在没有元素的时候进行操作
1、在没有元素的迭代器之中进行查找
2、在没有元素的迭代器之中进行元素的删除！

'''