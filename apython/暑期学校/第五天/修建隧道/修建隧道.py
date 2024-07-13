'''
另外的方法：
不需要明确找到两个城市的边框
直接从第一个城市的四周往外进行【广度优先搜索】，只要首先搜到了另外一座城市的影子，就可以结束搜索啦！这就是最短的路径



城市A和城市B之间被山阻隔，现在，我们需要修建一条隧道，连接两个城市。[就只有两个城市！]
我们用一个[二维的二进制数组]表示地图，其中，0表示山，1表示城镇，一个城市是由水平或垂直方向相邻（4连通）的城镇组成的一个区域，该区域被山包围。
请问，连接两个城市的隧道【最短有多长？】

[城市的每一个方块在和另外一个城市所处方位不同的时候，都有可能会是那个修建隧道的城镇！
[step1：找到两撮城市。step2：分别看两个城市各个点之间的距离？（水平+竖直距离）]
输入：
一行，一个二维list数组，用来表示城市的分布地图。
输出：
最短的隧道长度。

示例1:
输入： [[1,1,0,0],[1,1,0,0],[0,0,0,0],[0,0,0,1]]
输出： 3

示例2:
输入： [[1,0,1],[1,0,1], [0,0,1]]
输出：1

输入读取方式：
array = eval(input())
如图，红线部分为示例1的最短隧道（最短隧道的路径可能不唯一）：
'''


tu=eval(input())
hang=len(tu)
lie=len(tu[0])
option=[[0,-1],[-1,0],[0,1],[1,0]]#左、上、右、下
avail1=[]
avail2=[]
def notone(i,j):#下标为i，j的城市四周都没有和他相邻的啦
    for step in option:#四个方向遍历
        if 0<=i+step[0]<hang and 0<=j+step[1]<lie:#没有越界！
            if tu[i+step[0]][j+step[1]]==1:
                return False
    return True

def index_chengshi(i,j,avail):#从第一个是1的地方找到他所在的这个城市的所有坐标，并把tu中这个城市变成has，返回一个坐标的列表
    #递归寻找
    avail.append((i,j))
    tu[i][j]='has'
    if notone(i,j):
        return #结束寻找啦，四周都没有
    for step in option:#四个方向遍历
        if 0<=i+step[0]<hang and 0<=j+step[1]<lie:#没有越界！
            if tu[i+step[0]][j+step[1]]==1:#四周找到了一个1，没有被访问过
                avail.append((i+step[0],j+step[1]))#是在这个城市里边，加进来
                tu[i + step[0]][j + step[1]]='has'#访问过啦
                index_chengshi(i + step[0],j + step[1],avail)
biao=1
for i in range(0,hang):
    for j in range(0,lie):
        if tu[i][j]==1 and biao==1:
            index_chengshi(i,j,avail1)
            biao=2
        if tu[i][j]==1 and biao==2:
            index_chengshi(i,j,avail2)

avail1=list(set(avail1))
avail2=list(set(avail2))

fin=[]
for hang1,lie1 in avail1:
    for hang2,lie2 in avail2:
        fin.append(abs(hang1-hang2)+abs(lie1-lie2)-1)
print(min(fin))













