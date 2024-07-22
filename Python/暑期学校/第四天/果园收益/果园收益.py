'''
一片果园有 n 个坑位，每个坑位都可以种植A，B，C三种果树中的一种，但由于品种冲突，【相邻坑位不能种植同一种果树。】
由于不同坑位的土质不同，种植不同果树的最终收益也不同。每个坑位种植不同果树的收益用一个 n x 3 的正整数矩阵 payoff 来表示。
例如，payoff[0][0] 表示第 0 号坑位种植A果树的收益；payoff[1][2] 表示第 1 号坑位种植C果树的收益，以此类推。

请计算出种完这片果园后能获得的最大收益。

输入格式：
一共一行，n × 3矩阵表示的每个坑位种植不同果树的收益。1<=n<=1e4
输出格式：
能取得的最大收益。

输入示例：
[[1,2,3],[1,2,3],[4,5,6]]
输出示例：
11

'''
payoff=eval(input())
n=len(payoff)
avail=[]
def cultivate(type_tree,profit,current_hang):#当前种植的树木,当前的收益，当前的行数
    if current_hang==n:
        avail.append(profit)
    else:
        if type_tree==0:#种植A树
            cultivate(1,profit+payoff[current_hang][1],current_hang+1)#把下一轮种植的利润给加上
            cultivate(2,profit+payoff[current_hang][2],current_hang+1)
        if type_tree==1:
            cultivate(0, profit + payoff[current_hang][0], current_hang + 1)
            cultivate(2, profit + payoff[current_hang][2], current_hang + 1)
        if type_tree==2:
            cultivate(0, profit + payoff[current_hang][0], current_hang + 1)
            cultivate(1, profit + payoff[current_hang][1], current_hang + 1)
cultivate(0,payoff[0][0],1)
cultivate(1,payoff[0][1],1)
cultivate(2,payoff[0][2],1)
print(max(avail))
