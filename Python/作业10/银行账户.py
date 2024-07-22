'''
小技巧：
1、直接在注释行的底下写代码，最后再把注释删掉，合成一个总代码
2、

'''
'''
题目：[Python,继承] 银行账户
题目描述：
描述：我们希望创建银行账户，并且账户能够实现还贷的功能，不同账户之间能够进行交易（港币和人民币的汇率为1:0.8）。
要求实现以下类：

---港币个人账户类：HKD_Personal_Account；

---人民币公司账户类：RMB_Company_Account。

并实现以下功能：
1、账户类保存账户基本信息；
2、通过取款、存款成员函数withdraw、deposit：实现账户的取款和存款功能；
3、偿还贷款成员函数repay_the_loan：实现账户的贷款偿还功能；
4、资金转出贷款成员函数transfer_out：实现账户将资金从当前账户转入另一账户。
提示：【可以定义基类并继承，】从而更简洁地完成以上要求。

注：所有打印的数字均保留小数点后两位，需要print的格式推荐从介绍/样例输出中直接复制，以防符号格式不吻合。

结构介绍：

class HKD_Personal_Account():



##########################

###########################

样例输入：(print('数字')为了方便大家debug时定位print不同case对应的功能)

NJU = RMB_Company_Account(cash=500, loan=-300, account='NJU', sales=0)

SEU = RMB_Company_Account(cash=500, loan=-300, account='SEU', sales=0)

AI = HKD_Personal_Account(cash=30, loan=-20, account='AI')

CS = HKD_Personal_Account(cash=10, loan=-10, account='CS')

print('0')

print(AI)

print('1')

print(NJU)

print('2')

AI.deposit(20)

print('3')

AI.withdraw(10)

print('4')

AI.withdraw(100)

print('5')

NJU.deposit(20)

print('6')

NJU.withdraw(100)

print('7')

NJU.withdraw(1000)

print('8')

AI.transfer_out(NJU, 20)

print('9')

AI.transfer_out(NJU, 200)

print('10')

NJU.transfer_out(AI, 50)

print('11')

NJU.transfer_out(AI, 5000)

print('12')

AI.transfer_out(CS, 10)

print('13')

NJU.transfer_out(SEU, 100)

print('14')

NJU.transfer_out(SEU, 1000)

print('15')

AI.repay_the_loan(20)

print('16')

AI.repay_the_loan(200)

print('17')

NJU.repay_the_loan(100)

print('18')

NJU.repay_the_loan(1000)

exit()

样例输出：

0
AI账户余额：30.00HK$；账户贷款：-20.00HK$
1
NJU账户余额：500.00￥；账户贷款：-300.00￥；营业额为：0.00￥
2
AI账户余额：50.00HK$；账户贷款：-20.00HK$
3
AI账户余额：40.00HK$；账户贷款：-20.00HK$
4
余额不足，操作失败
AI账户余额：40.00HK$；账户贷款：-20.00HK$
5
NJU账户余额：520.00￥；账户贷款：-300.00￥；营业额为：0.00￥
6
NJU账户余额：420.00￥；账户贷款：-300.00￥；营业额为：0.00￥
7
余额不足，操作失败
NJU账户余额：420.00￥；账户贷款：-300.00￥；营业额为：0.00￥
8
转账成功
AI账户余额：20.00HK$；账户贷款：-20.00HK$
NJU账户余额：436.00￥；账户贷款：-300.00￥；营业额为：16.00￥
9
余额不足，操作失败
AI账户余额：20.00HK$；账户贷款：-20.00HK$
10
转账成功
NJU账户余额：386.00￥；账户贷款：-300.00￥；营业额为：16.00￥
AI账户余额：82.50HK$；账户贷款：-20.00HK$
11
余额不足，操作失败
NJU账户余额：386.00￥；账户贷款：-300.00￥；营业额为：16.00￥
12
转账成功
AI账户余额：72.50HK$；账户贷款：-20.00HK$
CS账户余额：20.00HK$；账户贷款：-10.00HK$
13
转账成功
NJU账户余额：286.00￥；账户贷款：-300.00￥；营业额为：16.00￥
SEU账户余额：600.00￥；账户贷款：-300.00￥；营业额为：100.00￥
14
余额不足，操作失败
NJU账户余额：286.00￥；账户贷款：-300.00￥；营业额为：16.00￥
15
还款成功
AI账户余额：52.50HK$；账户贷款：0.00HK$
16
余额不足，操作失败
AI账户余额：52.50HK$；账户贷款：0.00HK$
17
还款成功
NJU账户余额：186.00￥；账户贷款：-200.00￥；营业额为：16.00￥
18
余额不足，操作失败
NJU账户余额：186.00￥；账户贷款：-200.00￥；营业额为：16.00￥


'''

'''

'''
class HKD_Personal_Account():
    def __init__(self, cash=0, loan=0, account=None):
        self.cash=float(cash)
        self.loan=float(loan)
        self.account=account
        self.type='HKD_Personal_Account'
    #编写代码

    def withdraw(self, money):
        if money>self.cash:
            print('余额不足，操作失败')
            print(self)
        else:
            self.cash=self.cash-money
            print(self)
        #编写代码

    def deposit(self, money):
        #编写代码
        self.cash=self.cash+money
        print(self)

    def transfer_out(self, other, money):
        #编写代码
        if money>self.cash:#不可以转账
            print('余额不足，操作失败')
            print(self)
        else:
            print('转账成功')
            self.cash=self.cash-money
            print(self)
            if other.type=='RMB_Company_Account':
                other.cash=other.cash+0.8*money
                other.sales=other.sales+0.8*money
            else:
                other.cash = other.cash + money
            print(other)

    def __str__(self):
        return '{0}账户余额：{1:.2f}HK$；账户贷款：{2:.2f}HK$'.format(self.account,self.cash,self.loan)


    def repay_the_loan(self, money):
        #编写代码
        if money>self.cash:
            print('余额不足，操作失败')
            print(self)
        else:
            print('{0}还款成功'.format(self.account))
            self.loan=self.loan+money
            self.cash = self.cash - money
            print('账户余额：{0}HK$；账户贷款：{1}HK$'.format(self.cash, self.loan))



class RMB_Company_Account(HKD_Personal_Account):
    def __init__(self, cash=0, loan=0, account=None ,sales=0):
        #编写代码
        HKD_Personal_Account.__init__(self, cash, loan, account)
        self.sales=float(sales)
        self.type='RMB_Company_Account'
    def withdraw(self, money):
        #编写代码
        if money>self.cash:
            print('余额不足，操作失败')
            print(self)
        else:
            self.cash=self.cash-money
            print(self)

    def deposit(self, money):
        #编写代码
        self.cash = self.cash + money
        print(self)

    def transfer_out(self, other, money):
        #编写代码
        if money>self.cash:#不可以转账
            print('余额不足，操作失败')
            print(self)
        else:
            print('转账成功')
            self.cash = self.cash - money
            print(self)
            if other.type=='HKD_Personal_Account':
                other.cash=other.cash+1.25*money
            else:
                other.cash = other.cash + money
                other.sales = other.sales + money
            print(other)
    def repay_the_loan(self, money):
        #编写代码
        if money>self.cash:
            print('余额不足，操作失败')
            print(self)
        else:
            print('{0}还款成功'.format(self.account))
            self.loan = self.loan + money
            self.cash=self.cash-money
            print(self.__str__())

    def __str__(self):
        return '{0}账户余额：{1:.2f}￥；账户贷款：{2:.2f}￥；营业额为：{3:.2f}￥'.format(self.account,self.cash,self.loan,self.sales)
while True:
    exec(input())