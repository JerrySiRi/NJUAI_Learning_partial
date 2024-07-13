'''
森林中有n个孔雀，n未知。
提问其中【若干只】（并不是全部都问了）孔雀： "森林里还有多少只孔雀与你（指被提问的孔雀）颜色相同?"
我们将答案收集到一个整数数组array中，其中array[i]是第 i 只孔雀的回答。

给你数组array，请问：n至少是多少？

输入格式：
一行，若干个非负整数，以空格分开，表示被提问孔雀们的回答。

输出格式：
一个整数，表示n在所有可能中的最小值。

样例输入 ：
1 2 2

样例输出：
5

'''

answer=[int(x) for x in input().split()]
answer_single=list(set(answer))#集合可是去重好帮手呢！！！
sum=len(answer)
for i in answer_single:#去重之后集合中的元素
    a=answer.count(i)#原来有多少个
    if i+1-a>=0:
        sum+=(i+1-a)
    if i+1-a<0:
        zu=a%(i+1)#按照i+1进行分组
        if zu!=0:
            sum+=i+1-zu
print(sum)








