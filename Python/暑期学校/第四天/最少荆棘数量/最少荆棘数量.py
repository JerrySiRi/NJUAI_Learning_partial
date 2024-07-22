'''
Bob从一个布满荆棘的山顶往下走，希望遇到最少数量的荆棘。但是Bob只能从山顶往下走，不能平移。
现在将整座山的荆棘数量存储在triangle数组中，triangle[i]表示第i层（从山顶开始数）的荆棘分布情况。
Bod下山路线的限制为，他只能从triangle[i][j]位置移动到triangle[i + 1][j] 或triangle[i+1][j+1]两个位置。
如下图所示，箭头表示可移动的方向。

输入： 荆棘数量triangle数组。

输出： Bob从山顶走到山底遇到的最少荆棘数目。

#每一层i都有（第0层）i+1个荆棘分布
样例输入： [[1],[1,2],[3,4,5],[7,6,3,2]]
样例输出： 9


解析： 最优路线为1->1->4->3

'''
#解法？每一层都走荆棘数目最少的？
block=eval(input())
block.append([0 for i in range(0,len(block[len(block)-1])+1)])
avail=[]
def thistles(current_hang,count,current_address):#当前所处的行数、荆棘总数、当前所处下标位置
        if current_hang==len(block)-1:#去掉最后一行全是0的情况（打的补丁）
            avail.append(count)
        else:
            thistles(current_hang+1,count+block[current_hang+1][current_address],current_address)
            thistles(current_hang+1,count+block[current_hang+1][current_address+1],current_address+1)
thistles(0,block[0][0],0)
print(min(avail))