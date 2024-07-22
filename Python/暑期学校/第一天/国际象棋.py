'''

国际象棋的安全区域描述：
在一个n*m的国际象棋棋盘上(n,m>0)，有后，马，兵三种棋子，这里规定【兵】作为占位棋子不能移动，【后】和【马】走法同国际象棋的规则，
不熟悉规则的同学见备注摆放i个后，j个马，k个兵(i,j,k >= 0)，
求该棋盘上有多少格子没被占用而且是安全的(安全指的是如图中绿圈所示，不会被后和马攻击到的位置）

输入输出：
输入包括四行：
第一行有两个数N M，表示棋盘大小
第二行有 (2i+1) 个数，第一个数为 i，表示有几个后，后面有2i个数分别代表这几个后的位置(位置以1为起点，从左到右递增，从上到下递增，如图中后的位置为1 4）
第三行有(2j+1)个数，第一个数为j，表示有几个马，后面有2j个数，代表这几个马的位置
第四行有(2k+1)个数，第一个数为k，表示有几个兵，后面有2k个数，代表这几个兵的位置

输出一个数，表示该棋盘的安全区域的个数（注意，只需要考虑马和后的攻击范围，兵是占位棋子不能移动）

备注：下方图1,2,3,4中红色区域代表了后或马的攻击范围。
在国际象棋中，【后】可以走如图1所示的直线和斜线（上下左右，左上，左下，右上，右下），但路径中若有其他本方棋子(其他任意的兵，马或后）会被阻挡，如图2。
马走“日”字，具体地，如图3，是走2*3矩形的对角线方向，国际象棋中没有“蹩马腿”的规则，因此即使路途中有其他棋子，如图4，也不影响马的攻击范围

'''

'''
国际象棋规则：
后（Q）：横、直、斜都可以走，步数不受限制，但不能越子。
车（R）：横、竖均可以走，步数不受限制，不能斜走。除王车易位外不能越子。
马（N）：走的2*3的“日”字型
'''

'''
#测试
2 3
1 1 1
0
2 1 2 2 2

3 4
1 2 3
1 2 2
2 1 4 3 3
'''
a1=input().split()
N=int(a1[0]);M=int(a1[1])#是一个N*M的棋盘
a2=input().split()
a3=input().split()
a4=input().split()
N_hou=int(a2[0])#N_开头的参数分别是后、马、兵的数量
N_ma=int(a3[0])
N_bing=int(a4[0])
L_hou=[]#L_开头的参数分别是后、马、并的位置
L_ma=[]
L_bing=[]
for i in range(1,len(a2),2):
    L_hou.append((int(a2[i])-1,int(a2[i+1])-1))#让所有的位置都和python的下标保持一致
for i in range(1,len(a3),2):
    L_ma.append((int(a3[i])-1,int(a3[i+1])-1))
for i in range(1,len(a4),2):
    L_bing.append((int(a4[i])-1,int(a4[i+1])-1))

#创建地图N*M
map=[[0 for j in range(0,M)] for i in range(0,N)]
#step1:把所有兵的位置都占上
for i in L_bing:
    map[i[0]][i[1]]='bing'
#step2:标出来所有的【后】和【马】的位置
for i in L_hou:
    map[i[0]][i[1]]='hou'
for i in L_ma:
    map[i[0]][i[1]] = 'ma'
#step3:对马所有可以走的位置进行标位
for i in range(0,N):
    for j in range(0,M):
        if map[i][j]=='ma':
            if i-1>=0 and j-2>=0 and map[i-1][j-2]==0:
                map[i-1][j-2]='danger'
            if i-2>=0 and j-1>=0 and map[i-2][j-1]==0:
                map[i - 2][j - 1] ='danger'
            if i-2>=0 and j+1<M and map[i-2][j+1]==0:
                map[i-2][j+1]='danger'
            if i-1>=0 and j+2<M and map[i-1][j+2]==0:
                map[i - 1][j + 2] ='danger'
            if i+1<N and j+2<M and map[i+1][j+2]==0:
                map[i+1][j+2]='danger'
            if i+2<N and j+1<M and map[i+2][j+1]==0:
                map[i+2][j+1]='danger'
            if i+2<N and j-1>=0 and map[i+2][j-1]==0:
                map[i+2][j-1]='danger'
            if i+1<N and j-2>=0 and map[i+1][j-2]==0:
                map[i+1][j-2]='danger'
        #对后所有可以走的位置进行标记
        #【bug】多个循环，相互之间会互相影响！（其中一个会对另外一个产生副作用！！！）
        elif map[i][j]=='hou':
            #左a1 b1
            a1,a2,a3,a4,a5,a6,a7,a8=[i]*8
            b1,b2,b3,b4,b5,b6,b7,b8=[j]*8
            while b1-1>=0:
                if map[a1][b1-1]==0:
                    map[a1][b1-1]='danger'
                elif map[a1][b1-1] != 'danger':
                    break#碰到了障碍
                b1=b1-1
            #右a2 b2
            while b2+1<M:
                if map[a2][b2+1]==0:
                    map[a2][b2+1]='danger'
                elif map[a2][b2+1] != 'danger':
                    break#碰到了障碍
                b2=b2+1
            #上a3 b3
            while a3-1>=0:
                if map[a3-1][b3]==0:
                    map[a3-1][b3]='danger'
                elif map[a3-1][b3] != 'danger':
                    break#碰到了障碍
                a3=a3-1
            #下a4 b4
            while a4+1<N:
                if map[a4+1][b4]==0:
                    map[a4+1][b4]='danger'
                elif map[a4+1][b4] != 'danger':
                    break#碰到了障碍
                a4=a4+1
            #左下a5 b5
            while a5+1<N and b5-1>=0:
                if map[a5+1][b5-1]==0:
                    map[a5+1][b5-1]='danger'
                elif map[a5+1][b5-1] != 'danger':
                    break
                a5=a5+1;b5=b5-1
            #右上a6 b6
            while a6-1>=0 and b6+1<M:
                if map[a6-1][b6+1]==0:
                    map[a6-1][b6+1]='danger'
                elif map[a6-1][b6+1] != 'danger':
                    break
                a6=a6-1;b6=b6+1
            #左上a7 b7
            while a7-1>=0 and b7-1>=0:
                if map[a7-1][b7-1]==0:
                    map[a7-1][b7-1]='danger'
                elif map[a7-1][b7-1] != 'danger':
                    break
                a7=a7-1;b7=b7-1
            #右下a8 b8
            while a8+1<N and b8+1<M:
                if map[a8+1][b8+1]==0:
                    map[a8+1][b8+1]='danger'
                elif map[a8+1][b8+1] != 'danger':
                    break
                a8+=1;b8+=1
count=0
for i in range(0,N):
    for j in range(0,M):
        if map[i][j]==0:
            count+=1
print(count)



