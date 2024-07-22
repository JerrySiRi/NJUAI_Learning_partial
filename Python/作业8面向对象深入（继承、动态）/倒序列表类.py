'''
在list的基础上设计实现一个倒序列表类
提供【插入】、【删除】、【按序访问元素】的功能，[每次操作后保证列表是按照数据大小倒序顺序存储。]
考虑使用继承（is-a）和聚合（has-a）分别进行实现。
'''
#插入
'''
insert(self, index, object, /)
       Insert object before index.
'''
#删除
'''
 remove(self, value, /)
 |      Remove first occurrence of value.
'''
#按序（下标）访问元素
'''按照下标进行访问
 __getitem__(...)
 |      x.__getitem__(y) <==> x[y]
'''
class alist(list):
    def __init__(self,li):
        li.sort()
        li.reverse()
        list.__init__(self,li)#一开始就让他按照倒序来排列呢
    def insert(self,index,obj):
        list.insert(self,index,obj)
        self.sort()
        self.reverse()#不能再次初始化，没有东西可以接住初始化之后的东西啦！

a=[1,5,4,2,3]
alistt=alist(a)
print(alistt)
print(alistt[0])
print(alistt[1])
alistt.insert(1,10)
print(alistt)#有这样的输出结果是因为插入之后又排序啦！





