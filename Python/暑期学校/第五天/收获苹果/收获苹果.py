'''
果园里有 n (1=<n<=1000)颗苹果树排成一列，每颗苹果树上结了数量不等的苹果，其中有的是正常的苹果，有的苹果坏掉了。
农民伯伯[根据苹果树上结果的情况]对每颗苹果树进行[打分]
对于一颗苹果树上的多个苹果，每有一个正常的苹果，则+1分，每有一个坏掉的苹果，则-1分
现在得到了农民伯伯对这一列每颗苹果树的打分，用一个一维数组来表示。

在打分完成后，农民伯伯用他的收割机来收获苹果，由于他的收割机体型比较大，他只能从这一列苹果树的某一颗开始，[连续地]推倒多颗苹果树(至少推倒一颗）。
收割的过程只进行一次，问农民伯伯可以获得的最大得分是多少。

[可以不全推倒，只选择推倒几个。]
备注：由于农民伯伯使用了太阳系外文明培育的苹果种子，每颗苹果树的苹果可以非常多，每颗苹果树的得分区间∈[-1000,1000]

输入为一个一维列表，代表苹果树的得分序列。
输出为一个数，代表农民伯伯可以获得的最大得分

[-11,10,8,5,20,5,-1,-5]
'''

#没有tle的情况，直接从前往后遍历就可以啦！
scores=eval(input())######
avail=[]
for current in range(0,len(scores)):
    for next in range(current+1,len(scores)):
        avail.append(sum(scores[current:next]))
print(max(avail))


















'''
initial=filter(lambda x:x>0,scores)#开始的选择，得分一定大于0


def qiepian_qian(index):#当前位置不断向前后进行切片
    #向前
    if index==0:
        return
    sum=0
    for i in range(0,index+1):#只要前面的都是整数，不用递归，直接加进来就可以
        if scores[i]>=0:
            sum+=scores[i]
        else:
            forall_qian.append(sum)
            qiepian_qian(i)


for first in range(0,len(scores)):
    if scores[first] > 0:
        forall_qian=[]
        qiepian_qian(first)
        forall_hou=[]
        qiepian_hou(first)
        forall=forall_hou+forall_qian
        print(max(forall))
'''







