'''
题目：[Python,异常]自定义异常
题目描述：
描述：
继承Exception类，设计三个异常类。
设计函数根据要求【检查字符串输入】，【遇到不符合要求的地方抛出异常】。
设计函数对异常情况进行处理。
三种异常类型包括：
1. OverLengthException，异常信息为f"你输入名字长度为{input len}，最大长度为{max len}"
2. BelowLengthException，异常信息为f"你输入名字长度为{input len}，最小长度为{min len}"
3. UpperCaseException，异常信息为"你的输入包含大写的字母"

【1】name_test函数用于检测字符串是否合法。
接受三个参数(name, max_length, min_length)，分别是待检查的字符串、字符串的最大长度和最小长度。
按1、2、3的顺序检测异常，如有异常则【raise该异常。】

【2】input_name函数用于接受控制台输入的name，并进行检测。
其调用接受到的参数test_func(该函数对name_test进行了封装)对name进行检测，
具体为：若捕获到异常则打印异常信息；否则打印该name。

提示：
使用partial对name_test函数进行了封装，partial用法可参考：https://docs.python.org/3/library/functools.html?highlight=functools#functools.partial

输入样例1：
input_name(test_func)
k
输出样例1：
你输入名字长度为1，最小长度为4


输入样例2：
input_name(test_func)
hell1
输出样例2：
你的输入包含大写的字母
'''

'''
知识补充：
partial函数：
partial 接收函数 multiply 作为参数，固定 multiply 的参数 y=2，并返回一个新的函数给 double
这跟我们自己定义 double 函数的效果是一样的。
所以，简单而言，【partial 函数的功能就是：把一个函数的某些参数给固定住，返回一个新的函数。】
需要注意的是，我们上面是固定了 multiply 的关键字参数 y=2，如果直接使用：
double = partial(multiply, 2)
则 2 是赋给了 multiply 最左边的参数 x

ex：
产生一个有固定参数的函数double：
def double(x, y=2):
    return multiply(x, y)
以上功能可以使用partial函数来进行。
from functools import partial
double = partial(multiply, y=2)
返回了一个固定了参数y=2的具有multiply功能的函数double
'''


class OverLengthException(Exception):#OverLengthException，异常信息为f"你输入名字长度为{input len}，最大长度为{max len}"
    #不在这个位置判断。只是用于输出异常信息的！
    def __init__(self,inputlen,maxlen):
        self.inputlen=inputlen
        self.maxlen=maxlen



class BelowLengthException(Exception):#BelowLengthException，异常信息为f"你输入名字长度为{input len}，最小长度为{min len}"
    def __init__(self,inputlen,minlen):
        self.inputlen=inputlen
        self.minlen=minlen


class UpperCaseException(Exception):# UpperCaseException，异常信息为"你的输入包含大写的字母"
    #def __init__(self):
        #Exception.__init__(self, "你的输入包含大写的字母")
        pass


'''
【1】name_test函数用于检测字符串是否合法。
接受三个参数(name, max_length, min_length)，分别是待检查的字符串、字符串的最大长度和最小长度。
按1、2、3的顺序检测异常，如有异常则【raise该异常。】
'''
def name_test(name, max_length, min_length):
    a=len(name)
    if a>max_length:
        raise OverLengthException(a,max_length)
    elif a<min_length:
        raise BelowLengthException(a,min_length)
    p=name[:]#【【错误】】！！！变量直接赋值是直接对地址的引用！！！不可以直接赋值！得用切片！
    p=p.lower()#p.lower()是有返回值的函数，字符串不可以被直接修改！得有东西来接住他
    if p!=name:#可以直接比较p.lower()!=name
        raise UpperCaseException

'''
【2】input_name函数用于接受控制台输入的name，并进行检测。
其调用接受到的参数test_func(该函数对name_test进行了封装)对name进行检测，
具体为：若捕获到异常则打印异常信息；否则打印该name。
'''
def input_name(test_func):#已经封装了name_test了！即已经从控制台得到了name参数啦！这个参数是test_func。input_name应该是靠test_func来发挥作用的！
    # 捕获并处理异常
    try:
        x=input()
        test_func(x)
        print(x)
    except OverLengthException as err:
        print (f"你输入名字长度为{err.inputlen}，最大长度为{err.maxlen}")
    except BelowLengthException as err:
        print(f"你输入名字长度为{err.inputlen}，最小长度为{err.minlen}")
    except UpperCaseException :
        print("你的输入包含大写的字母")


from functools import partial
test_func = partial(name_test, max_length=6, min_length=4)
exec(input())

