'''
描述：设定两个类，一个能处理整数的叫IntValue，一个能处理矩阵的叫Matrix。
IntValue类初始化时,要接受整数x，Matrix要接受二维（MxN）的列表x。
在两个类里设定一个接受y的成员函数add()，它要接受参数y并要返回x+y。

另外，设定一个单独的函数叫adder()，本函数要【接受IntValue或者Matrix类的一个[对象]】以及【要加的元素（整数或者MxN列表）】
【在adder()函数里要调用本类的add()函数并返回答案。】

提示：

样例输入：
matrix = Matrix([[1,2],[3,4]])
print(adder(matrix, [[3,3],[4,2]]))
exit()

样例输出：
[[4, 5], [7, 6]]

'''
class IntValue:
    def __init__(self,x):
        self.x=x
    # 在此处填写代码
    def add(self,y):
        return self.x+y


class Matrix:
    def __init__(self,x):
        self.x=x
    def add(self,y):
        for i in range(0,len(self.x)):
            for j in range(0,len(self.x[0])):
                y[i][j]=y[i][j]+self.x[i][j]
        return y
    # 在此处填写代码


def adder(element_type, value_to_add):#可以用上duck tying的思想，直接调用！！！不需要再次判断他的类型是matrix还是int！
    return element_type.add(value_to_add)

    # 在此处填写代码


while True:
    exec(input())
