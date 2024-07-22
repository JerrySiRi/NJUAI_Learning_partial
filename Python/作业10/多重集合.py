'''
知识补充：用定义__str__来完成对self对象的输出！
Help on wrapper_descriptor:

__str__(self, /)
    Return str(self).

一、 object类内置方法__str__和函数str
类的内置方法__str__和内置函数str实际上实现的是同一功能，实际上str调用的就是__str__方法，只是调用方式不同，二者的调用语法如下：
实例对象. str()
str(对象)

返回值为一个字符串对象，该字符串对象类似一种非正式的字符串表示，为什么说是” 非正式”呢，这是因为Python对这个返回值没有特殊要求，只要求是对用户信息好理解。 此方法因此通常被用于与最终用户交互时的显示信息，str 的意义是得到便于人们阅读的信息，因此需要尽可能确保其包含的信息便于理解。

二、 __str __方法和函数str方法的使用
由于object类定义了__str__方法，因此所有类都会继承该方法，除非有自定义类重写了该方法。
什么情况下会触发__str__方法呢？主要有如下情况会触发__str__的调用：

在交互环境下直接输入str(对象名)查看对象内容；
print(对象)查看对象内容时
直接调用“对象.str()”方法；
由于列表以及字典等容器总是会使用 repr 方法，即使调用__str__方法访问输出的还是__repr__访问内容。

在调用的时候可以用
法一：：：print(str(self))来完成调用！【相当于把这个对象（在函数定义中有self）进行部分内容的输出（可以使一部分的成员变量呢！）】
法二：：：print(self.__str__())
法三：：：print(self)可以直接对这个类中定义的__str__中return的值进行调用并且输出的呢！
'''

'''

小技巧：
1、直接在注释行的底下写代码，最后再把注释删掉，合成一个总代码
'''


'''
题目：[Python,类设计] 多重集合
题目描述：
描述：有时我们在使用集合数据结构时希望集合中的一个元素可以【出现多次】，并且集合之间仍然可以进行并集、差集、交集、补集等集合运算。
要求自定义实现多重集合类MultiSet，类似于常规的集合set，一个多重集合至少需要实现以下功能：

***1. 使用元素list或者None来初始化多重集合对象
2. 可以使用print函数来打印多重集合对象（用__str__可以完成对这个对象的输出）
3. 可以使用len函数获得其中元素的总个数
4. 可以使用in操作符判断一个元素是否在当前对象中
5. 可以在该对象中添加一个元素add
6. 可以在该对象中删除一个元素remove
7. 可以获得该对象中某个元素的个数 （该功能不存在于常规的set中）-----【1.可以考虑使用dict记录每个元素的出现次数】
8. 多重集合对象之间可以进行并、差、交、补等集合运算（该题中只要求实现并集运算）

样例输入：
ms1 = MultiSet([3,1,2])
print(ms1.count(0))
ms2 = MultiSet([5,2,3,2])
print(1 in ms1)
print(4 in ms1)
print(ms1)
print(ms2)
print(len(ms1), len(ms2))
ms1.add(3)
print(ms1)
ms1.remove(1)
print(1 in ms1)
print(ms1)
print(ms1.count(3))
ms3 = ms1.union(ms2)
print(ms3)
exit()

样例输出：
True
False
{1, 2, 3}
{2, 2, 3, 5}
3 4
{1, 2, 3, 3}
False
{2, 3, 3}
2
{2, 2, 3, 3, 5}
小心这个样例输出有空格的！
'''


class MultiSet(list):   # 继承的效果一样呢，可以用list转换成列表之后用列表的函数，再用列表的函数》set函数
    def __init__(self, elements = None):
        #编写代码
        elements.sort()
        self.element=elements#是一个列表，会有重复元素的.【!!！sort()函数没有返回值！，需要单写一句！】

    def __str__(self):
        self.element.sort()#可能在加入元素之后改变了从小到大的顺序呢
        if self.element==None:
            print('None')

        else:#join函数！
            a='{'+str(self.element[0])
            for i in range(1,len(self.element)):
                a=a+', '+str(self.element[i])
            a=a+'}'
            return a
        '''
        1、其实可以不用None的判断的，在init函数之中已经对None进行了考虑了！如果是None的话，就直接输出None应该有的结果啦！
        2、字符串的输出
            如果格式相同，对原来列表中所有的元素进行统一的操作。优先考虑join函数[列表-字符串]！
            如果格式不同，优先考虑格式化输出。f-string或者format函数。（尽量不用%进行格式化输出哦）
        '''
    def __len__(self):
        return len(self.element)

    def __contains__(self, element):
        if self.element!=None:
            for i in self.element:
                if element==i:
                    return True
        return False
    '''
    这里的使用in的对象i，不是Multi的对象！（本质上是调用了i.__contains__函数呢！）而i不是Multi的对象，不会重复循环调用超过深度的捏！
    '''
    def add(self, element):
        self.element.append(element)

    def remove(self, element):
        #函数赋值的时候不需要写出来参数都是什么！
        self.element.remove(element)

    def count(self, element):
        if element not in self.element:
            return 0
        dict1 = dict()
        for i in self.element:
            if i not in dict1:
                dict1[i] = 1
            else:
                dict1[i] = dict1[i] + 1
        return dict1[element]
    '''
    1、创建字典的时候最好用dict()进行创建，如果用空的花括号创建的话{},解释器可能不知道这个是字典还是集合。（应该不会出现问题，但为了万无一失）
    2、如果字典是空的话，返回的dict.keys()也是空的，对if的判断以及in的运用都不会产生什么影响的！放心大胆用就好啦！
    
    '''
    def union(self, other_multi_set):#思路：先把两个列表进行合并，最后再删除多的元素呢！【更好的思路：用加法，而不是减法！】
        list1 = self.element + other_multi_set.element
        new_list = list(set(list1))
        for element in new_list:
            if element in self.element and element in other_multi_set.element:
                for i in range(min(self.count(element), other_multi_set.count(element))):
                    list1.remove(element)
        '''#已经移除过的元素记录
        aaa = ['z']
        for i in list1:
            a = b = 0
            if i in self.element:
                a = self.dict1[i]  # 为了防止没有这个元素之后被赋值。且为了书写简单
            if i in other_multi_set.element:
                b = other_multi_set.dict1[i]
            if (a != 0) and (b != 0) and (i not in aaa):  # 两个对象之中都有！
                c = min([self.dict1[i], other_multi_set.dict1[i]])
                aaa.append(i)
                for j in range(0, c):
                    list1.remove(i)'''
        '''
        以上代码的实现理由：
        1、不调用count函数，如果把dict定义在count之中，这个dict是没有办法进行创建的。
           需要放在init函数中进行初始化。而且得在count函数之中重新进行初始化。因为初始化只在一开始创建的时候进行调用，之后万一add函数修改了对象中某些元素
           而这个dict应该是随self.element的变化而变化的》》用dict的时候需要重新进行初始化（对dict进行更新）
           》》》》》》以后为了避免，【应该把dict写在一个函数之中，并实现一些功能，啥时候用的时候啥时候调用并且实现这个功能。甚至可以pass来单纯创建dict！！！******】
           【在上面没有被屏蔽掉的代码就是直接调用了count函数，对dict1进行创建】
        2、append会把列表的[]加进来呢！“+”只能用于两个类型相同的进行合并。而append可以让类型不同的进行合并。》》把一个列表整体作为元素给另外一个列表
        3、用set进行去重！！！！！可以省掉被屏蔽代码的aaa=['z']的部分。【判断这个东西有没有被判断过！】
        4、创建一个列表进行打补丁的时候可以在一个列表中给一个一定不会被访问到的作为初始化。》》可以作为可hash的对象进行访问（其中至少要有一个元素！）
        '''
        return MultiSet(list1)

while True:
    exec(input())
