'''
【有tle和wa的BUG】
描述：给定一个 m×n 的二维01数组，其中0表示道路，1表示障碍。
可以在道路单元格中上、下、左、右移动，不能超出边界。【但肯定不走回头路的是最短的，就设置成不走回头路的程序吧，也顺便可以不出现死循环】
假设最多可以消除 k 个障碍物，请给出从左上角 (0, 0) 到右下角 (m-1, n-1) 的最短路径，并打印通过该路径所需的步数。
如果不存在这样的路径，打印-1 。(无法从左上角到达右下角。比如有两行全部被占满了，但是最多只可能消除一个障碍物)

输入格式：
总共两行，第一行表示二维01数组；第二行表示最多可以消除的障碍物数量。
输出格式：
最短路径的大小，或者-1。

示例输入：
[[0, 0, 0], [1, 1, 0], [0, 0, 0], [0, 1, 1], [0, 0, 0]]
1
示例输出：
6

[[0,0],[0,1],[0,0]]
1

[[0,0],[1,1],[1,1],[0,0]]
1

[[0,1],[1,0],[0,0],[0,0]]
1
'''
from copy import deepcopy
step=[[0,-1],[-1,0],[0,1],[1,0]]#左、上、右、下
mapp=eval(input())#当前地图
eli=int(input())#最多可以消除的次数
n=len(mapp)
m=len(mapp[0])#一共是n*m的map
#递归
# 如果可以从左上角到达右下角，把移动次数，存放在列表中。（最后如果列表为空，就返回-1.否则返回列表的最小值）
'''
递归结束条件：
①到达了右下角
②已经用掉了所有可以清除障碍的机会，但是仍然无路可走了（把-1加到列表之中）

递归传递--把下一步的坐标传给move函数
'''

avail=[]
step=[[0,-1],[-1,0],[0,1],[1,0]]#左、上、右、下
def can(i,j,el):#在当前位置(没到终点)是否能动.1、没到终点时的可以动 2、没到终点时的不能动
    biao=False
    for k in step:
        if 0<=i+k[0]<n and 0<=j+k[1]<m:
            if mapp[i+k[0]][j+k[1]]==0:#没有障碍，且没有越界
                biao=True
                break
            if mapp[i+k[0]][j+k[1]]==1 and el!=0:#有障碍，但是可以使用一次清除障碍
                biao=True
                break
    return biao

def move(i,j,count,el):#当前坐标i,j,count为当前第几次步骤
    global mapp
    mapp[i][j]='has'#走到了当前位置肯定得是has呀！
    mapping=deepcopy(mapp)#【存档】
    elii=el#【存档】
    if i==n-1 and j==m-1:#把可行步骤得加进来！
        avail.append(count)
    elif not can(i,j,el):#没有到终点而且不能动
        avail.append(0)
    else:#没到终点而且可以动
        for k in step:
            if 0<=i+k[0]<n and 0<=j+k[1]<m:
                if mapp[i + k[0]][j + k[1]] == 0 :#没有遇到障碍
                    mapp[i + k[0]][j + k[1]]='has'#已经走过了
                    move(i + k[0],j + k[1],count+1,el)
                    mapp=mapping
                if mapp[i+k[0]][j+k[1]]==1 and el!=0:#遇到了障碍但是el不为0
                    mapp[i + k[0]][j + k[1]]='has'#已经走过了
                    move(i+k[0],j+k[1],count+1,el-1)
                    #受N皇后的启发，因为需要多轮操作当前步骤的二维数组，所以需要在上一轮操作完成之后进行“还原“！
                    mapp=mapping
                    el=elii
mapp[0][0]='has'
move(0,0,0,eli)
if avail==[0]*len(avail):
    print(-1)
else:
    count=avail.count(0)
    for i in range(count):
        avail.remove(0)
    print(min(avail))
