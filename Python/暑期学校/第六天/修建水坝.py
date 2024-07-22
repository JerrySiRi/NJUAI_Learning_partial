'''
题目：修建水坝
题目描述：
在一条长为 L（0<=L<=10000）的水渠上，有 N （2<=N<=1000)个可以修建防洪坝的点位，分布在水渠的不同位置，工程师打算修 M个防洪坝（2<=M<=N)，防洪坝只能修在点位上。
工程师希望防洪坝分散尽可能开，便可以最有效地抵挡洪水，具体地，他希望这些防洪坝[两两之间的最小距离尽可能的大]，[希望你能计算这个最小距离最大时是多少。]

输入包括两行：
第一行为两个数，N和M，分别表示可以修建防洪坝点位的个数N，和需要修建防洪坝的个数M。
第二行为一个长为N的一维列表，表示可以修建防洪坝的N个点位的位置。

输出：
两两防洪坝之间的最小距离最大时的值。
备注：第二行输入点位的位置可以是乱序的。(加一个sort就可以喽)



输入示例：至少修建两个水坝！排序之后收尾一定要占上的呢！
5 3
[1,2,8,4,9]

输出示例：
3

9 3
[1,2,9,50,60,80,90,95,100]
>>49

5 4
[1,4,5,6,9]
>>【错误！】此时4个距离最长的时候没有建立在3个最长的情况之下！4个最长的是1469 三个最长的是159【保存实力】
解释：
防洪坝分别修在1 4 9三个位置，此时最小距离为3，是所有可能修建方法的最大值。

'''
'''

distance的含义：所有最小的距离一定小于平均间隔。所以从平均间隔往下一次次递减
嵌套的第一个while：如果对当前的distance，后面剩余的水坝次数*distance，如果小于剩余的距离，那么这个distance一定不可以，直接-1
---如果不行，直接不搜了。相当于减枝了。
嵌套的第二个while：找到下一个可以安放水坝的最近的一个位置，放水坝

'''

dam_num = int(input().split()[1])#修建大坝的数量dam_num
locations = sorted(eval(input()))#可以修建大坝的位置
distance = (locations[-1] - locations[0]) // (dam_num - 1)#平均距离
while True:
    remaining_dam_num = dam_num - 1#【-1给到了上一次previous_index的位置去了】
    previous_index = 0#上一次的下标
    current_index = 1#这一次的下标
    while remaining_dam_num != 0:
        if locations[-1] - locations[previous_index] < remaining_dam_num * distance:
            #现在还剩水坝没有安置，但是比平均距离还小，那么最终的距离一定比当前distance要小
            #知道当前“可能“的最大距离（最后一个减去当前可能安置的位置）>= distance，才可以进行下去
            distance -= 1
            break#break出来，重新从distance-1重新搜索

        #以下while和else相互匹配
        while locations[current_index] - locations[previous_index] < distance:
            #当前位置不可以安置这个水坝，比平均距离都要小
            current_index += 1
        #else:
        previous_index, current_index = current_index, current_index + 1#可以暗访下一个水坝了，放在current_index的位置。下一次搜索水坝从当前位置往后边一个
        remaining_dam_num -= 1

    else:#循环正常结束才会执行else。如果上一层循环被break出来的，（distance-1了之后就不break出去，而是继续循环。）就不执行else，直到remaining_dam_num==0！
        break
print(distance)



'''

#核心思路：动态规划，是一个递推公式，下一步的最佳走法是在上一步达到了最佳的情况下走出来的！
#ex：4个的时候一定是在3个时候间距最大的基础之上进行产生！

x=input().split()
N_keyixiujian=int(x[0])
M_bashu=int(x[1])
L_weizhi=eval(input())
L_weizhi.sort()

#其实可以在列表中存选出来的下标！可以省去许多麻烦！
avail=[(0,len(L_weizhi)-1)]#存的是每一段
def construction():#至少修建3个水坝的时候调用这个函数，每次调用一次函数都会多修建一个水坝！
    maxx=0
    target_index=0
    removing=0
    for each_duan in avail:
        first,last=each_duan[0],each_duan[1]
        for i in range(first+1,last):
            temp=min(L_weizhi[i]-L_weizhi[first],L_weizhi[last]-L_weizhi[i])
            if temp>maxx:
                maxx=temp
                target_index=i
                removing=each_duan
    #现在就找到了最大距离的下标、应该去除掉的某一段
    avail.append((removing[0],target_index));avail.append((target_index,removing[1]))
    avail.remove(removing)

for k in range(M_bashu-2):
    if M_bashu==2:
        print(L_weizhi[-1]-L_weizhi[0])
    else:
        construction()
minning=L_weizhi[-1]-L_weizhi[0]
for i in avail:
    temp= L_weizhi[i[1]]-L_weizhi[i[0]]
    if temp<minning:
        minning=temp
print(minning)

'''