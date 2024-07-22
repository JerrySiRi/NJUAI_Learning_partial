'''
大作业：生成100000个在(0,1)区间上均匀分布的随机数，并以此生成
伯努利分布、二项分布、泊松分布、几何分布、指数分布、正态分布的随机数
【需要将各种分布的参数作为输入变量，最后查资料验证方法的正确性】

---查资料
---可用matplotlib画出生成的100000个点的图像，对比分布函数或者概率密度函数

'''

'''
task1:生成(0,1)上均匀分布的100000个随机数
根据线性同余法的计算公式，该算法最多只能产生m个不同的 随机数，
实际上对于特定的种子，很多数无法取到，循环周期基本达不到m。
如果 进行多次操作，得到的随机数序列会进入循环周期。
因此，一个好的线性同余随机数生成器，
要让其循环周期尽可能接近m，这就需要精心选择合适的乘法因子a和模数m（需要利用代数和群理论）
具体实现中有多种不同的版本，例如gcc中采用 的glibc版本
其中
m=2**31-1\\\\a=1103515245\\\\c=12345
满足m足够大，c和m互质，常数a-1可以被m的因子整除
'''

a = 46341
c = 498325315
m = 2 ** 31
from datetime import datetime  # 未来使用时间戳作为seed
import time
import numpy as np
import math
import sympy
import matplotlib.pyplot as plt
from scipy.special import comb


# 【BUG】通过pip下载matplotlib的时候只能下载到自己在本地装的python，而不是vscode自动下的
# 所以用pip装了之后，应该ctrl shift p转换成本地的解释器才可以呢！

def uni_dis():
    seed = (datetime.now()).timestamp()  # 当前时间的时间戳
    uni = []  # 存放100000个均匀分布的随机数
    target_temp = 0
    for i in range(0, 100000):
        target_temp = (a * seed + c) % m
        uni.append(target_temp / m)
        seed = target_temp
    '''
    uni_np=np.array(uni)
    plt.hist(uni_np,bins=100,edgecolor="black")
    plt.title("U(0,1)")
    plt.xlabel("随机数范围")
    plt.ylabel("数量")
    plt.show()
    '''

    return uni


def Ber_dis(uni_distri, p):  # 【产生100000个符合伯努利分布的数据】
    Ber_dis = []
    Ber_dis_test = []
    num0 = 0
    num1 = 0
    for i in range(100000):
        if 0 < uni_distri[i] < 1 - eval(p):
            # Ber_dis_test.append((uni_distri[i],0))#当前x，以及所对应的“随机数”
            Ber_dis.append(0)
            num0 = num0 + 1
        else:
            # Ber_dis_test.append((uni_distri[i],1))
            Ber_dis.append(1)
            num1 = num1 + 1
    # print("num0=",num0,"\n","num1=",num1) #期望的角度来看的呢！
    Ber_dis_np = np.array(Ber_dis)
    plt.hist(Ber_dis_np, bins=100)  # edgecolor="black"
    plt.title("Ber(p)")
    plt.xlabel("随机数范围")
    plt.ylabel("数量")
    plt.show()
    return Ber_dis


def B_dis(uni_distri_B, n, p):  # 【产生100000个符合二项分布的数据】
    '''
    X~B(n,p),X的所有可能取值是0,1,2,...,n,共n+1个！！！
    '''
    temp = []
    # print(comb(n,1,exact=True)) 使用scipy的comb的时候，默认返回的是ndarray！
    for i in range(n + 1):
        temp.append(comb(n, i, exact=True) * (p ** i) * ((1 - p) ** (n - i)))
    # temp.sort(key = lambda x:x[1])
    l_F = [0 for i in range(n + 1)]
    l_F[0] = temp[0]
    for i in range(1, n + 1):
        l_F[i] = l_F[i - 1] + temp[i]

    Er_xiang = []
    for i in range(100000):
        for j in range(1, n + 1):
            if 0 <= uni_distri_B[i] <= l_F[1]:
                Er_xiang.append(0)
                break
            if l_F[j - 1] < uni_distri_B[i] <= l_F[j]:
                Er_xiang.append(j)
                break
    Er_xiang_np = np.array(Er_xiang)
    plt.hist(Er_xiang_np, bins=100)  # edgecolor="black"
    plt.title("B(n,p)")
    plt.xlabel("随机数范围")
    plt.ylabel("数量")
    plt.show()
    # 测试 n=20 p=0.6（ppt中的例子）
    return Er_xiang


def P_dis(uni_distri_P, labm):  # 【产生1000个属于泊松分布的数据，只产生了100个泊松分布的数据点】
    temp = []
    for i in range(100):  # 让k只能取0-99中的数字吧，不然乘100000太大了
        temp.append((labm ** i) / math.factorial(i) * sympy.exp(-labm))
    l_p = [0 for x in range(100)]
    l_p[0] = temp[0]  # 【分布列】
    for i in range(1, 100):
        l_p[i] = l_p[i - 1] + temp[i]

    Bo_song = []
    for i in range(1000):
        for j in range(1, 100):
            if 0 <= uni_distri_P[i] <= l_p[1]:
                Bo_song.append(0)
                break
            if l_p[j - 1] < uni_distri_P[i] <= l_p[j]:
                Bo_song.append(j)
                break
    Bo_song_np = np.array(Bo_song)
    plt.hist(Bo_song_np, bins=100)  # edgecolor="black"
    plt.title("P(lambda)")
    plt.xlabel("随机数范围")
    plt.ylabel("数量")
    plt.show()
    # 测试  ppt中的例子：lambda=10
    return Bo_song


def G_dis(uni_distri_G, p):
    temp = []  # X的所有可能取值为1,2,...,100
    for i in range(1, 101):  # 让k只能取0-99中的数字吧，不然乘100000太大了
        temp.append(((1 - p) ** (i - 1)) * p)
    l_g = [0 for x in range(100)]
    l_g[0] = temp[0]  # 【分布列】
    for i in range(1, 100):
        l_g[i] = l_g[i - 1] + temp[i]

    Ji_he = []
    for i in range(1000):
        for j in range(1, 100):
            if 0 <= uni_distri_G[i] <= l_g[1]:
                Ji_he.append(0)
                break
            if l_g[j - 1] < uni_distri_G[i] <= l_g[j]:
                Ji_he.append(j)
                break
    # print(Ji_he)
    Ji_he_np = np.array(Ji_he)
    plt.hist(Ji_he_np, bins=100)  # edgecolor="black"
    plt.title("G(p)")
    plt.xlabel("随机数范围")
    plt.ylabel("数量")
    plt.show()
    # 测试 p=0.2
    return Ji_he


def e_dis(uni_distri, lamb):
    Zhi_shu = []
    for i in range(1000):
        temp = float(-sympy.log(sympy.E, (1 - uni_distri[i])) / lamb)
        Zhi_shu.append(temp)
        # print(temp)

    Zhi_shu_np = np.array(Zhi_shu)
    plt.hist(Zhi_shu_np, bins=10000, edgecolor="black")  #
    plt.title("e(lambda)")
    plt.xlabel("随机数范围")
    plt.ylabel("数量")
    plt.xlim(0, 800)  # 在lambda=0.1的时候的数据分布比较直观
    plt.show()
    return Zhi_shu


#a = 1103515245
    #c = 12345
    #m = 2 ** 31

    #a=46343
    #b=498325313
    #m=2**31-1
    #更换了一组产生线性同余随机数的参数呢！

def N_dis():#test---运行这个
    '''
    要产生两个独立的在(0,1)上的均匀分布X1和X2
    '''
    seed = (datetime.now()).timestamp()
    seed1 = seed  # 当前时间戳
    seed2 = seed  # 另外的方法：当前时间戳的小数部分seed - seed1


    a = 46341
    c = 498325315
    m = 2 ** 31
    uni_seed1 = []  # X1---存放100000个均匀分布的随机数
    target_temp = 0
    for i in range(0, 100000):
        target_temp = (a * seed1 + c) % m
        uni_seed1.append(target_temp / m)
        seed1 = target_temp

    a = 1103515245#更换了一组线性同余法之后产生的随机数
    c = 12345
    m = 2 ** 31
    uni_seed2 = []  # X2---存放100000个均匀分布的随机数
    target_temp = 0
    for i in range(0, 100000):
        target_temp = (a * seed2 + c) % m
        uni_seed2.append(target_temp / m)
        seed2 = target_temp

    Zheng_tai = []
    sum=0
    for i in range(0, 100000):
        #temp_z=math.sqrt((-2) * math.log(uni_seed1[i]))  * (math.cos(2 * math.pi * uni_seed2[2]))
        #temp_z=math.sqrt((-2) * (float(sympy.log(sympy.E, uni_seed2[i]))))\
               #* (float(sympy.cos(2 * sympy.pi * uni_seed1[i])))
        #[BUG！]为什么没有加float的差距会这么大呢？？？
        temp_z = math.sqrt((-2) * (float(math.log( uni_seed2[i])))) \
                 * (float(math.cos(2 * math.pi * uni_seed1[i])))
        #使用sympy，尽管已经向量化编程了，但还是函数调用的代价会比math要高的！！！
        Zheng_tai.append(temp_z)
        sum=sum+1

    Zheng_tai_np = np.array(Zheng_tai)
    plt.hist(Zheng_tai_np, bins=100, edgecolor="black")
    plt.title("N(0,1) bins=100")
    plt.xlabel("随机数范围")
    plt.ylabel("数量")
    plt.xlim(-6, 6)  # 正态分布的3a原则,此时a=1
    plt.show()
    return Zheng_tai

if __name__ == '__main__':  # 在(0,1)上均匀分布的随机数
    uni_distribution = uni_dis()
    # plt.plot(range(100000),uni_dis)
    # plt.show()

    args = input("请输入当前分布\n").split()  # 输入的参数1：什么分布，都有哪些参数（不同分布的参数个数不一样呢！）

    if args[0] == "Ber":  # 【输入 Ber p】
        '''
        伯努利分布-参数就一个p
        随机变量所有可能取值就只有0和1
        '''
        args_Ber = input("伯努利分布 Ber(p)：请输入概率 p((0,1)之间)\n").split()
        Ber_distribution = Ber_dis(uni_distribution, args_Ber[0])

    elif args[0] == "B":  # 【输入 B n p】
        args_B = input("二项分布 B(n,p)：请输入试验总次数 n（正整数）以及概率p（(0,1)之间）（以空格分开）\n").split()
        B_distribution = B_dis(uni_distribution, eval(args_B[0]), eval(args_B[1]))

    elif args[0] == "X":  # 【输入 X lambda】
        args_P = input("泊松分布 P(lambda)：请输入参数 labmda（大于0的常数）\n").split()
        P_distribution = P_dis(uni_distribution, eval(args_P[0]))

    elif args[0] == "G":  # 【输入 G p】
        args_G = input("几何分布 G(p)：请输入概率 p((0,1)之间)\n").split()
        G_distribution = G_dis(uni_distribution, eval(args_G[0]))


    elif args[0] == "e":  # 【输入 e lambda】
        args_e = input("指数分布 e(lambda)：请输入参数 lambda(大于0的常数)\n").split()
        e_distribution = e_dis(uni_distribution, eval(args_e[0]))
    elif args[0] == "N":  # 【输入--好像什么都不用输入呢！】
        print("正态分布 N(0,1)：无需输入参数，最终得到的是标准正态分布\n")
        e_distribution = N_dis()#换线性同余法的参数





