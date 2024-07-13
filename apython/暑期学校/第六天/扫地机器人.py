'''
题目：扫地机器人
题目描述：
扫地机器人具有自动充电的机制，在电量较低时，可以自己回到充电位置进行充电。
这就需要记录自己到充电位置的距离。我们假设扫地机器人位于一个无限大小的 XY 网格平面，起点为 (0, 0) ，面向北方。
该扫地机器人接收到一系列的指令 commands。
其中，每个指令的含义为：
-2 ：向左转 90 度
-1 ：向右转 90 度
1 <= x <= 9 ：向前移动 x 个单位长度

在网格上有一些障碍物 obstacles 。第i个障碍物位于网格点obstacles[i] = (xi, yi) 。
当执行【指令的过程中】遇到障碍物时，扫地机器人会停在障碍物前的一个方格上，跳过该指令，然后继续执行后续的指令。

已知机器人接收到的指令序列和所有障碍物信息，请问，机器人经过的所有路径点中（坐标为整数），离原点的距离最远是多少？
为了便于检查，我们对欧式距离向下取整，返回整数部分。

输入格式：
两行，第一行为commands[列表]的str形式，第二行为obstacles[列表]的str形式。
输出格式：
输出一个整数，为最大的欧式距离。

建议读取方式：
commands = eval(input())
obstacles = eval(input())
建议输出方式:
print(int(math.sqrt(square)))， 其中square是欧式距离的平方

[-2,4,-2,4]
[(-4,0)]
'''
import math
commands = eval(input())#指令,已经变成了整数啦
obstacles = eval(input())#障碍物
orientation_zuo=['north','west','south','east']#左转的方向顺序
orientation_you=['north','east','south','west']#右转的方向顺序
orientation_moving=[[0,1],[1,0],[0,-1],[-1,0]]#不同朝向，每次向前移动的次数【按照右转90度的顺序来写的】
def action(i,j,chaoxiang,instruction):
    #参数：当前位置，当前朝向，当前指令，返回：执行或者不执行之后的坐标,当前朝向
    if instruction==-2:#左转
        if not(chaoxiang=='east'):
            return i, j, orientation_zuo[orientation_zuo.index(chaoxiang) + 1]
        else:
            return i,j,'north'
    elif instruction==-1:#右转
        if not(chaoxiang=='west'):
            return i, j, orientation_you[orientation_you.index(chaoxiang) + 1]
        else:
            return i,j,'north'
    else:#当前朝向往前走x个单位
        xiabiao=orientation_you.index(chaoxiang)#当前移动的下标变化
        for k in range(instruction):
            if [i+orientation_moving[xiabiao][0],j+orientation_moving[xiabiao][1]] not in obstacles:#当前下一步往前走没有遇到障碍
                i+=orientation_moving[xiabiao][0]
                j+=orientation_moving[xiabiao][1]
            else:#遇到了障碍，直接
                break
        return i,j,chaoxiang

chaoxiang='north'
i=j=0
maxing=0
for each in commands:#每一个指令分别取出来
    i,j,chaoxiang=action(i,j,chaoxiang,each)
    temp=i**2+j**2
    if temp>maxing:
        maxing=temp
print(int(math.sqrt(maxing)))


'''

样例输入

[5, -2, 4, 7]
[[4, 0], [4, 2], [0, 2], [0, 2]]

样例输出

11

解析：

接收指令5， 机器人走到(0, 1)处，(0, 2)处有障碍，因此终止该指令的执行；

接受指令-2，向左转；

接受指令4， 机器人移动到(-4, 1)处；

接受指令7，机器人移动到(-11, 1)处；

最大欧式距离为int(sqrt(11^2 + 1^2)) = 11
'''