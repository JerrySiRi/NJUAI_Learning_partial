'''
#【有问题，先不做了。问题出现在多个正方形有重合（不是覆盖）的部分，如何应该减掉】
#【思路太复杂，再想简单的思路！！！】


小明家有一片黑白两色等大小正方形（边长为1）地砖铺的地面，小明想知道这块地面中到底有多少个由黑砖构成的正方形。
注：一个 3×3 正方形的地面中一共包含 9+4+1=14 个子正方形（1×1，2×2，3×3）输入格式：
一共一行，m×n 的二维数组，0表示白砖，1表示黑砖。1<=m,n <= 300
输出：
黑砖构成的正方形的个数。输入示例：
[[1,1,0,1],[1,1,0,0],[0,0,1,0],[1,0,0,1]]
输出示例：
9

[[1,1,1],[1,1,1],[1,1,1]]
[[1,1,0],[1,1,1],[1,1,1],[1,1,1]]

'''
def fang(n):
    count=0
    while n>=1:
        count+=n**2
        n-=1
    return count

def all(i,j,target):#一定不会越界
    for cur_heng in range(i,i+target):
        for cur_shu in range(j,j+target):
            if tu[cur_heng][cur_shu]==0:
                return False
    return True

def caozuo(i,j,target):
    for m in range(i,i+target):
        for n in range(j,j+target):
            tu[m][n]='has'

def notalready(i,j,target):#没有被访问过
    for m in range(i,i+target):
        for n in range(j,j+target):
            if tu[m][n]==1:
                return True
    return False

#思路：对每一个黑砖，四周寻找包含他的最大的正方形n*n，再调用fang函数
tu=eval(input())
shu=len(tu)
heng=len(tu[0])#这个tu是一个shu*heng的地图
sum=0
for i in range(0,shu):
    for j in range(0,heng):
        if tu[i][j]==1 or tu[i][j]=='has':#是一个黑砖(可以是已经被访问过的)
            #sum+=1
            target1=0
            target2=0
            for k in range(j,heng):#水平寻找最大的矩形范围
                if tu[i][k]==1 or tu[i][k]=='has':#是黑砖
                    target1+=1
                else:#不是黑砖
                    break
            for m in range(i,shu):
                if tu[m][j]==1 or tu[m][j]=='has':
                    target2+=1
                else:
                    break
            target=min(target2,target1)
            if all(i,j,target) and notalready(i,j,target):
                caozuo(i,j,target)
                sum+=fang(target)
print(sum)


