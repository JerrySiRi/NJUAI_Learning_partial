'''

几何王国准备为数学探险者建造一个几何雕塑，该雕塑有M层，总体积为Nπ，每一层都是一个圆柱体
设从下往上数第i(1<=i<=M)层是半径为Ri, 高度为Hi的圆柱。
该雕塑每一层的半径和高度都比上面一层要大，也就是说当i<M时，要求Ri>Ri+1且Hi>Hi+1。

由于要在雕塑上粉刷油漆，国王为尽可能节约经费，希望雕塑外表面（最底层的下底面除外）的面积Q最小。

令（外表面面积）Q = Sπ，请编程实现，对给定的的N和M，输出该雕塑外表面面积Q 最小时的S。 （除Q外，M、N、R、H、S均为正整数）

输入
有两行，第一行为N(0<N<=1000),表示待建造的雕塑的体积为Nπ
       第二行为M(0<M<=20),表示雕塑的层数为M

输出
若有解，输出正整数S，若无解则输出0

'''
'''

有以下限制条件：
①R1>R2>R3>.....>Rm    H1>H2>H3>...>Hm
②R1*R1*H1+...+Rm*Rm*Hm==N
③求Smin=2R1*H1+2R2*H2+...+2Rm*Hm+R1*R1

'''
def min_area(volume, min_radius, min_height, remaining_num):#返回的是最小表面积。参数分别为：总体积、最小半径、最小高度、剩余层数
    if remaining_num == 0 and volume != 0:#0层，体积却不为0
        return 2 ** 20
    if remaining_num == 0 and volume == 0:#0层，体积为0
        return 0
    area_list = []
    #以下都是通过pai*R*R*H=V来计算的
    max_radius = int((volume / min_height) ** (1/2))#最大半径（高度全部为1（实际上是取不到的））
    for radius in range(min_radius, max_radius + 1):#遍历所有可能的半径--最大半径
        max_height = int(volume / radius ** 2)#最大高度
        for height in range(min_height, max_height + 1):#遍历所有可能的高度
            area_list.append(min_area(volume - (radius ** 2) * height, radius + 1, height + 1, remaining_num - 1)#每次只对一层的体积进行计算！
                             + radius ** 2 - (min_radius - 1) ** 2 + 2 * radius * height)
    if not area_list:#空列表
        return 2 ** 20
    else:
        return min(area_list)


if __name__ == '__main__':
    total_volume = int(input())
    num = int(input())
    area = min_area(total_volume, 1, 1, num)
    if area > 2 ** 10:
        print(0)
    else:
        print(area)








