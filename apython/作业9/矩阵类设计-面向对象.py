'''
题目描述：
描述：实一个矩阵类叫Matrix，其中包括初始化函数和多个成员函数。
[1]初始化函数：__init__(self, value)
功能：初始化函数需要接受一个参数（存储矩阵所有元素的一个二维list）。
要求：按照接受的参数设定三个成员变量（row, col, value）分别代表矩阵的行数，列数和前面传入的二维list。
[2]成员函数1：matprint(self)
功能：将当前Matrix对象中的元素按照矩阵形式打印出来
要求：每行的元素之间间隔一个空格，并且每行尾部不能有空格
例子：一个2*3的全0矩阵需要将以下内容输出在控制台中
0 0 0

0 0 0
[3]成员函数2：add_(self, num_or_mat)
功能：将当前Matrix对象中所有的元素都加上一个相同的整数值(int) 或者 将当前Matrix与另一个Matrix对象按位相加
要求：该函数需要根据参数的类型来判断是加值还是加矩阵（该成员函数直接修改当前对象内部的成员变量，不需要返回值），如果要加的矩阵与当前矩阵的形状不同则不进行任何操作。
例子：
对于矩阵
0 1

2 3
如果加1则变成
1 2

3 4
如果这时再加上另一个矩阵
0 1

1 0
则会变成
1 3

4 4
如果再加上一个矩阵
0 1 2

3 4 5
则原矩阵保持不变仍为
1 3

4 4
[4]成员函数3：transpose_(self)
功能：将当前Matrix对象进行转置操作
要求：该成员函数直接修改当前对象内部的成员变量，不需要返回值
例子：
对于矩阵
0 1

2 3
调用该成员函数后变为
0 2

1 3

[5]成员函数4：matmul_(self, other_mat)
功能：将当前Matrix对象中另一个Matrix对象进行矩阵乘法，并将结果保存在当前Matrix对象中
要求：该成员函数直接修改当前对象内部的成员变量，不需要返回值，如果两个矩阵无法进行矩阵相乘，则不进行任何操作。
例子：
对于矩阵
1 1

1 1
如果与该矩阵进行矩阵乘法
1 1

1 1
则变为
2 2

2 2
如果再与该矩阵进行矩阵乘法
1 1

2 2

3 3
则保持不变仍为
2 2

2 2
提示：在python类的成员函数定义中，如果函数的功能为inplace修改（即直接修改当前对象内部的属性），则一般成员函数名一般需要以下划线 '_' 结尾
如果不以下划线结尾又要进行某些修改操作则一般需要返回一个新的对象，例如mat1.add_(5)就对应着mat1 = mat1.add(5)。
这是常用的一种命名规范，如果没有严格遵守也并不会引起程序运行出错。
'''
'''
输入样例：

mat1 = Matrix([[1,2,3],[24,5,16]])
mat1.matprint()
mat1.transpose_()
mat1.matprint()
exit()

输出样例：

1 2 3

24 5 16

-1 0 1

22 3 14
'''

'''
[5]成员函数4：matmul_(self, other_mat)
功能：将当前Matrix对象中另一个Matrix对象进行矩阵乘法，并将结果保存在当前Matrix对象中
要求：该成员函数直接修改当前对象内部的成员变量，不需要返回值，如果两个矩阵无法进行矩阵相乘，则不进行任何操作。
例子：
对于矩阵
1 1

1 1
如果与该矩阵进行矩阵乘法
1 1

1 1
则变为
2 2

2 2
如果再与该矩阵进行矩阵乘法
1 1

2 2

3 3
则保持不变仍为
2 2

2 2

'''
class Matrix:

    def __init__(self, value):
        self.value=value#成员变量是二维列表
        self.row=len(value)#行数
        self.col=len(value[0])#列数
        # 在此处填写代码

    def matprint(self):
        for i in range(self.row):
            for j in range(self.col):
                if j != self.col - 1:#最后一个输出不能输出空格！！
                    print(self.value[i][j], end=" ")
                else:
                    print(self.value[i][j])


        # 在此处填写代码

    def add_(self, num_or_mat):
        if type(num_or_mat)==int:#加数字
            for i in range(0,self.row):
                for j in range(0,self.col):
                    self.value[i][j]=self.value[i][j]+num_or_mat
        elif isinstance(num_or_mat,Matrix)==True:
            if len(num_or_mat.value)==self.row and len(num_or_mat.value[0])==self.col:#行数相同、列数相同
                for i in range(0,len(num_or_mat.value)):
                    for j in range(0,len(self.value[i])):
                        self.value[i][j]=self.value[i][j]+num_or_mat.value[i][j]
        #如果不相等，就什么都不做啦

        # 在此处填写代码

    def transpose_(self):
        a=list(zip(*self.value))
        b=[]
        for i in range(0,len(a)):
            b.append(list(a[i]))
        self.value=b
        self.row = len(self.value)  # 行数
        self.col = len(self.value[0])  # 列数
        # 在此处填写代码
    def matmul_(self, other_mat):
        if self.col==len(other_mat.value):
            self.value=[[sum(map(lambda a: a[0] * a[1], zip(l, s))) for l in zip(*other_mat.value)] for s in self.value]
            self.row = len(self.value)  # 行数
            self.col = len(self.value[0])  # 列数
        # 在此处填写代码

while True:
    exec(input())


