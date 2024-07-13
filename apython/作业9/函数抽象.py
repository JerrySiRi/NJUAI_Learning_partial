'''
题目：[Python,面向对象] 函数抽象设计
题目描述：
描述：完成两个任务：
1、给定若干备选物品，每个物品都有各自重量。现有一个背包，具有给定的容量，判断能否用备选物品[刚好装满背包]，[每个物品可以使用0/1次。]
2、给定若干候选字符串。现有一个目标字符串，判断能否[选择一些候选字符串]拼接成[目标字符串]（注意，只能拼接，不能插入）。每个字符串可以使用0/1次。
现有搜索子集和搜索全排列的通用函数实现（函数1和2），请调用这些函数实现可以完成上述任务的函数（函数3和4），如有需要也可以自行定义函数实现一些辅助功能。

函数1：def subset_search(item_list, condition, current_result=[], current_index=0)（无需实现）
    功能：遍历item_list的所有子集，并判断是否有子集满足condition函数的要求（使得condition函数返回True）。有满足就返回True，否则返回False。
    item_list:对背包任务是int型list，对字符串任务是str型list。
    condition：条件判断函数。
    current_result:list，搜索辅助变量，默认值为[]，调用时可直接使用默认值。
    current_index:int，搜索辅助变量，默认值为0，调用时可直接使用默认值。

函数2：def permutation_search(item_list, condition, current_result=[])（无需实现）
    功能：遍历item_list中元素的全排列，并判断是否有排列满足condition函数的要求（使得condition函数返回True）。有满足就返回True，否则返回False。
    item_list:对背包任务是int型list，对字符串任务是str型list。
    condition：条件判断函数。
    current_result:list，搜索辅助变量，默认值为[]，调用时可直接使用默认值。

函数3：def zero_one_bag(item_list, target)
    功能：求解背包问题，如果能刚好装满则返回True，否则返回False。
    item_list：[整型list]，存储每个备选物品的重量，10>=len(item_list)>=1，100>=item_list[i]>=0。
    target：int数，背包的容量，100>=target>=0。

函数4：def string_composion(item_list, target)
    功能：求解字符串拼接问题，能拼成返回True，否则返回False。
    item_list：str型list，候选字符串的集合，10>=len(item_list)>=1,20>=len(item_list[i])>=1
    target：str，目标字符串。100>=len(target)>=0

'''
'''
item_list = [1, 2, 3, 4, 5]
target = 10
print(zero_one_bag(item_list, 10))
item_list = ['ab', 'abc', 'grth', 'th', 'd']
target = 'grthabcd'
print(string_composion(item_list, target))
exit()
样例输出：
True
True
'''

def subset_search(item_list, condition, current_result=[], current_index=0):
    '''This function searches all subsets of item_list and check whether there is one or more subset satisfies the condition.'''
    if current_index == len(item_list):
        return condition(current_result)

    # case1: include the current item
    result1 = subset_search(item_list, condition, current_result, current_index + 1)

    # case2: does not include the current item
    new_result = current_result.copy()
    new_result.append(item_list[current_index])

    result2 = subset_search(item_list, condition, new_result, current_index + 1)

    return result1 or result2


def permutation_search(item_list, condition, current_result=[]):
    '''This function searches all permutation of item_list and check whether there is one or more permutation satisfies the condition.'''
    if len(item_list) == 0:
        return condition(current_result)

    result = False
    for item in item_list:
        remaining_items = item_list.copy()
        new_result = current_result.copy()
        new_result.append(item)
        remaining_items.remove(item)
        result = permutation_search(remaining_items, condition, new_result) or result
    return result


def zero_one_bag(item_list, target):
    def condition1(a):
        sum=0
        for i in a:
            sum=sum+i
        if sum==target:
            return True
        else:
            return False
    return subset_search(item_list,condition1)

    # 在此处填写代码
    pass

def string_composion(item_list, target):
    def condition(l):
        s=''.join(l)
        if s==target:
            return True
        else:
            return False
    def condition1(a):
        return permutation_search(a,condition)
    return subset_search(item_list,condition1)



while True:
    exec(input())