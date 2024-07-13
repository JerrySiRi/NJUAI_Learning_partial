'''
矩形的面积由长和宽共同决定，给定一个整数数组array，有n个元素，表示n条垂线段。
其中，第i条线段的两个端点分别是(i, 0)和(i, array[i])。
第i条线段和第j条线段组成的面积为(|j - i|) * min(array[i], array[j])，min表示两个数中的较小值。

现给出n条垂线段，请从中选择两条，使得它们与x轴构成的矩形面积最大，输出最大的矩形面积。

输入格式：
一行，n个非负整数，以空格分开，表示n条垂线段的长度。

输出格式：
最大的矩形面积。

样例输入：
2 3 5 3 2 4
样例输出：
12

5 4 1 6

5 4 1 6 5 3 5


读取输入方式：
array = [int(x) for x in input().split()]


'''

#找到每一个位置作为“边界”的最大值。（尽量让另外一侧作为边界的）
#ex：定在左侧，如果右侧找到了一个比他大的。这一定是左侧作为“边界”的面积最大值了（再往里边缩，两边界的最小值也最大是原来那个，宽度还变窄了）
array = [int(x) for x in input().split()]

def mian(li):#优化：让两轮的循环每一次从左往右搜索》》一轮循环，两侧往中间搜索
    left=0
    right=len(li)-1
    maxx=0
    current=0
    while left<right:
        if li[left] <= li[right]:
            current=li[left]*(right-left)#左侧小，按照左侧的乘
            left+=1
        else:
            current=li[right]*(right-left)#右侧小，按照右侧的乘
            right-=1
        if maxx < current:
            maxx=current
    return maxx

print(mian(array))


