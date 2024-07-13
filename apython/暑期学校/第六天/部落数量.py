'''
题目：部落数量题目描述：给定一个 m×n 的二维01数组代表一个平原，平原上0的位置表示无人居住，1的位置有人居住。
现定义一个“部落”为水平或垂直方向相邻的1构成的一块区域，超出边界部分都认为无人居住。请算出给定数组表示的平原中部落的数量。

输入格式：
总共一行，表示二维01数组。
输出格式：
一个数字，代表部落数量。
示例输入：
[[1, 1, 1], [0, 1, 0], [0, 0, 1]]
示例输出：
2

[[1,1,0,1,1],[1,1,1,0,0],[1,1,0,0,1],[0,1,0,1,1]]
[[1,0,1],[0,0,0],[0,0,1]]
'''

option=[[-1,0],[0,1],[1,0],[0,-1]]#上、右、下、左
tu=eval(input())
heng=len(tu)
zong=len(tu[0])
#count=0
def cannot(i,j):#当前位置四周都没法走了
    for step in option:
        if 0<=i+step[0]<heng and 0<=j+step[1]<zong:
            if tu[i+step[0]][j+step[1]]==1:
                return False
    return True

def searching(i,j):#从当前位置往四个方向进行搜索【调用的条件，当前位置是1】
    tu[i][j]='has'
    if cannot(i,j):#当前位置四周都没有可以走的了
        return
    for step in option:
        if 0<=i+step[0]<heng and 0<=j+step[1]<zong:
            if tu[i+step[0]][j+step[1]]==1:
                tu[i+step[0]][j+step[1]]='has'
                searching(i+step[0],j+step[1])
count=0
for i in range(0,heng):
    for j in range(0,zong):
        if tu[i][j]==1:
            count+=1
            searching(i,j)
print(count)




