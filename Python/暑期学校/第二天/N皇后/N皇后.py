'''
八皇后问题是一个以国际象棋为背景的问题：如何能够在8×8的国际象棋棋盘上放置八个皇后，使得任何两个皇后不能相互攻击？
备注： 若两个皇后处于同一条水平线、垂直线或斜线上时，她们会相互攻击。
我们将该问题，扩充为N皇后问题，输入数字N， 判断N皇后问题有几种可行的摆放方式。 【棋盘N*N.一共有N个皇后】
输入： N
输出： N皇后问题的可行解个数
'''
#任意的两个白皇后都不在同一行、同一列或同一条对角线上.>>【每一行上有且只有一个皇后，同理每一列！】
#皇后的攻击范围（需要每次循环处理）
'''
递归思路：当一条路可以前进时就一直前进，行不通则退回上一步。

当选择（1，1）作为起始皇后的位置时，1那么第二排就有两个位置可以选择（2，3）、（2，4）
step1 选择（2，3）时，第三排就无法继续了
step2 现在退回去选择（2，4），在第三排hi有一种选择（3，2），在选择了这一点之后，发现第四排已经无法继续了，而且也无法再向第三排后退
》》说明（1，1）这一点无法作为皇后的位置

发现（1，2）和（1，3）两个点可以作为皇后的起点。

'''
q_range=[[0,-1],[-1,-1],[-1,0],[-1,1],[0,1],[1,1],[1,0],[1,-1]]#分别是左、左上、上、右上、右、右下、下、左下

def gen_board(n, queens):#n*n的棋盘，queens是皇后的所在列的位置(下标+1是这个皇后所在的行)
    result = []
    for i in range(n):
        rows = ['0'] * n
        rows[queens[i]] = "queen"
        result.append(rows)
    return result


def back(line_num, n, queens, solutions, columns, diazuo, diayou):#首先假定所有皇后不在同一行》》只需要存储这些皇后的列数即可！！！
    if line_num == n:#递归结束，当前已经判断到了最后一行（存在最后一行的某一列，让所有的皇后都放的下！）
        result = gen_board(n, queens)
        solutions.append(result)
    for i in range(n):#进行同一行各个位置的判断【此时皇后位置相当于是(line_num,i)】
        if (i in columns) or (line_num - i in diazuo) or (line_num + i in diayou):#queen的坐标保证了不在同一行，以下保证不在同一列！！！
            continue
        #把所有的左、右对角线（不能放皇后的）以数字存储在集合之中！
        #左对角线：在3*3的方阵之中，有5条左对角线。如果用这一对角线上所有元素的【（横坐标）-（纵坐标）】（同一条对角线上信息一样）
        #右对角线：同理【（横坐标）-（纵坐标）】
        #不在同一列、同一左对角线、同一右对角线！！！！！
        queens[line_num] = i#当前皇后的列数

        columns.add(i)#当前列不能再放任何皇后
        diazuo.add(line_num - i)#这个左对角线不能再放任何皇后
        diayou.add(line_num + i)#这个左对角线不能再放任何皇后
        back(line_num + 1, n, queens, solutions, columns, diazuo, diayou)
        #以上是上一次放置位置的情况。下一次循环在同一行中，故需要消除上一次的影响

        columns.remove(i)
        diazuo.remove(line_num - i)
        diayou.remove(line_num + i)


def solve(n):
    solutions = []
    queens = [0] * n
    # 判断是否在一列
    columns = set()
    d1 = set();d2 = set()#左对角线和右对角线
    back(0, n, queens, solutions, columns, d1, d2)
    return solutions

x=int(input())
a = solve(x)
print(len(a))#所有解决方法的个数


