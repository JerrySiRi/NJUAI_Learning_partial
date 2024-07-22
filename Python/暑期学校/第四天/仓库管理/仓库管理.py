'''
题目：仓库管理
题目描述：
现在有两个仓库1和2，[每小时]都会有一批货物进入仓库1或者仓库2，仓库管理员Mike是这两个仓库唯一的管理员，刚开始在仓库1值班。
由于两仓库相距较远，Mike只能开车往返于仓库1和2。

现在规定，仓库进货时该仓库必须有人值班才能进行一次合法进货。
Mike车速很快，在两个车库之间移动的时间远小于1h，但Mike的车的汽油有限，[最多只能进行W次移动]
（从仓库1到仓库2 或 从仓库2到仓库1算一次移动）。

现在给定 t小时内进货的规划表，请编写程序计算Mike最多能进行多少次合法进货？ 备注：t为整数且1=<t<=1000 , W为整数且1<=W<=20

输入
输入包括两行，第一行有两个数，分别为总时间t小时和Mike车能进行的移动次数W
第二行包括t个数，为接下来每个小时需要进货的仓库编号。

输出
输出一个数，也就是Mike最多能进行合法进货的次数。

输入样例：
7 2
2 1 1 2 2 1 2
输出样例：
6
样例说明：
Mike在接下来的七次进货中只能进行两次移动，他刚开始在仓库1，则第一个小时他不需要移动，第二个小时他移动到仓库2，第三个小时不动，第四个小时移动到仓库1，这样就可以合法进货6次。

输入样例：#每一次进货的下一次进货都在当地，不需要移动喽
8 2
1 1 1 1 1 1 1 1
输出样例： 8

3 2
2 1 2

4 2
1 2 2 2

3 2
2 2 2

5 3
2 1 2 1 2
'''
a=input().split()
T_schedule=int(a[0])
W_move=int(a[1])
bianhao=[int(x) for x in input().split()]
avail=[]
def moving(move_remain,count,t_current,address):#address是当前在1号仓库还是2号仓库
    if t_current==T_schedule-1:#当前位置是进货的最后呢【可以此时没有用完移动的次数！】
        avail.append(count)
    else:#不是进货的最后
        if move_remain==0:#当前无法移动啦
            x=bianhao[t_current+1:]
            count+=x.count(address)#之后就只能在当地进行收货,从下一个位置开始，因为调用的时候已经把这次的位置收货给算上啦！
            avail.append(count)
        else:#可以移动而且可以没有到进货的最后
            if bianhao[t_current+1]==address:#当前时刻的下一个进货和所在位置一样，一定不动
                moving(move_remain,count+1,t_current+1,address)
            else:#当前时刻的下一个进货和所在位置不同，可以动也可以不动
                moving(move_remain,count,t_current+1,address)#不动，下一次无法完成进货，count不动
                address=((address-1)^1)+1
                moving(move_remain-1,count+1,t_current+1,address)#动，下一次可以进货，count+1
if bianhao[0]==1:
    moving(W_move,1,0,1)
else:#第一次收货地在2
    moving(W_move,0,0,1)#一开始不动
    moving(W_move-1,1,0,2)#一开始跑到了2号
print(max(avail))

#[BUG]:if一定要和一个else所对应的，如果没有对应关系，解释器把最近的if和else认为是一对。所以可能做完一个条件判断之后还会做另外一个（和预期不符！）