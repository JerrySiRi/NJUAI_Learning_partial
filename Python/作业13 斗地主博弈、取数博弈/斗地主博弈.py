'''
题目描述：
描述：在某牌类游戏中，牌的大小关系根据牌的数码表示如下：3<4<5<6<7<8<9<10<J<Q<K<A<2<小王<大王，而花色并不对牌的大小产生影响。
每一局游戏中，一副手牌由 n 张牌组成。游戏者每次可以根据规定的牌型进行出牌，首先打光自己的手牌一方取得游戏的胜利。
现设计对手牌的分析程序，对给定手牌的出牌方式进行分析。
为简化游戏规则，现不考虑2、小王、大王这三种牌码，即只保留 3<4<5<6<7<8<9<10<J<Q<K<A 这12种牌码
【每种牌码的牌最多4张】，【手牌数量区间为[1,8]。】

符合出牌规则的牌型如下：
1. 单张：单张牌，如一张A。
2. 对子：两张数码相同牌，如AA。
3. 三连：三张数码相同牌，如AAA。
4. 炸弹：四张同数码牌，如AAAA。
5. 单顺子：五张或更多数码连续的单牌，如：34567, 8910JQKA

基于以上规则，请完成以下功能：
1. 设计Poker类，用以手牌的表示和分析。初始化函数接受一个字符串类型参数，用空格分隔每张牌。并提供以下手牌分析函数。
2. 完成check_count()函数，输入参数count，返回bool值。功能为：检查手牌中是否有单张、对子、三连、炸弹。
3. 完成check_straight()函数，不接受额外参数，返回bool值。功能为：检查手牌中是否有单顺子。
4. 完成cal_all_ways()函数，不接受额外参数，返回int值。功能为：搜索一共有多少种不同的出牌组合方式（忽略花色的影响）。
例如：手牌为A A A A，出牌方式有如下5种（AAA,A与A,AAA是相同组合）：
    1. A,A,A,A
    2. AA,AA
    3. A,AAA
    4. AAAA
    5. AA,A,A

输入样例：
1.
输入：
poker = Poker("A A A A")
print(poker.check_count(3))
exit()
输出：
True

2.
输入：
poker = Poker("10 J Q K A")
print(poker.check_straight())
exit()
输出：
False

3.
输入：
poker = Poker("3 3 3 3")
print(poker.cal_all_ways())
exit()
输出：
5

4.
输入：
poker = Poker("3 3 4 5 6 7")
print(poker.cal_all_ways())
exit()
输出：
3


'''
def sorting(a):
    if a=='1':
        return 10
    if a=='J':
        return 11
    if a=='Q':
        return 12
    if a=='K':
        return 13
    if a== 'A':
        return 14
    if 3<=int(a)<=9:#字符串的判断应该在整数的前面。不然int（str）会报错的！
        return int(a)

class Poker:#设计Poker类，用以手牌的表示和分析。【手牌的数量1-8！】
    def __init__(self, cards):#初始化函数接受一个字符串类型参数，用空格分隔每张牌。并提供以下手牌分析函数。
        self.card=cards.split(' ')#牌被存在一个列表之中了
        if '10' in self.card:
            a=self.card.count('10')
            for i in range(0,a):
                self.card.remove('10')#把其中的10全部去掉，之后全部以1来替代！
            for i in range(0,a):
                self.card.append('1')
        self.card.sort(key=sorting)#对这个列表完成了排序

    def check_count(self, count):#完成check_count()函数，输入参数count，返回bool值。功能为：检查手牌中是否有单张、对子、三连、炸弹。
        """
        检查手牌中是否有单张、对子、三连、炸弹
        count 为 1 时，检查单张
        count 为 2 时，检查对子
        count 为 3 时，检查三连
        count 为 4 时，检查炸弹
        有，返回True；否则，返回False
        """
        if count == 1:
            if len(self.card)!=0:
                return True
            else:
                return False
        if count == 2:
            for i in range(0,len(self.card)-1):
                if self.card[i]==self.card[i+1]:
                    return True
            return False
        if count == 3:
            for i in self.card:
                if self.card.count(i)>=3:#有一个牌有三张就可以啦
                    return True
            return False
        if count == 4:
            for i in self.card:
                if self.card.count(i)>=4:#有一个牌有三张就可以啦
                    return True
            return False
        '''
        【【bug1】】：有四张牌一样的时候，也得判断他有三张一样是对的呢
        '''
    def check_straight(self):#完成check_straight()函数，不接受额外参数，返回bool值。功能为：检查手牌中是否有单顺子。
        """
        检查手牌中是否有顺子
        有，返回True；否则，返回False
        【单顺子：五张或更多数码连续的单牌，如：34567, 8910JQKA】！！！有字母的呢！
        """
        '''
        之后的计算出牌方式的函数之中一定要调用这个！！
        '''
        #可否转化为子字符串出现的次数》=1.且这个子字符串的len要大于5.单顺子小心！如果有两张一样的牌也是可以的呢【需要去重】。大于5个的顺子只需要考虑5个！
        card=list(set(self.card))#去重之后的牌
        card.sort(key=sorting)
        cards=''.join(card)#把去重+排序之后的牌转化为没有空格的字符串
        target='34567891JQKA'#排好顺序的
        for i in range(0,len(target)-4):
            t=target[i:i+5]
            if cards.find(t,0,len(cards))!=-1:#看看子串t在不在cards之中，如果在，返回下标。如果不在，返回-1
                return True
        return False


    '''
    递归整体思路：
    
    1%递归结束条件：
    1.1牌出完了（最后一步没有出单张）》len(x)==0            
    1.2牌要出完，最后一些步出的单张！！！（之后的优先级保证了只要你这步出了单张，之后就只能出单张了！）
    
    2%每次往下递归的原则：
    2.1先后出牌顺序不能记录重复。如先出3333，后出44和先出44和3333是一样的》》》
    》》【方法】：设定出牌的优先级！合二为一（只能先从多的开始出）、顺子也得从8顺子开始出，直到5顺子
    2.2.如果本次出牌出最高级的牌型，把最高级的牌型全都出完了之后才可以出之后的牌型。
        如果本次不出最高级的牌型，但如果不出，之后就甭想出了!
          如344555666678这种牌型，所有情况都有。本次如果出了55，之后就不可以出345678等顺子了。因为先出345678、后出55和一开始的情况一样！
    》》每次选中了在这种牌型的牌之后
    ①出本级牌型（顺子和炸弹、三连等分开考虑--顺子有相互包含的关系） 
        tips：出本级的牌型得时候也会有顺序的问题，如33 44.先33后44和先44后33，是一样的出牌方式
        【方法】：设定出牌的优先级！（和整体思路异曲同工）如果这一次出的牌出的和上次牌型一样，且比上次要小》》记录在内
    ②不出本级牌型，直接不动传入的参入，调用函数进入下一级

    
    '''

    '''
    【【bug2】】实例对象用'='直接赋值的结果还是（对实例对象）地址直接引用！！！！（他的一些属性都保存在了这个地址之中的）
    但如果使用之前对象的init函数的参数创建一个新的实例对象之后，就不是对地址的引用了。在一个新的地址创建了这个对象
    '''

    def cal_all_ways(self) -> int:#完成cal_all_ways()函数，不接受额外参数，返回int值。功能为：搜索一共有多少种不同的出牌组合方式（忽略花色的影响）
        """
        计算共有多少种不同的打光手牌的出牌组合，并返回该值。
        """
        def delete(x,y):#从y之中逐步删除掉x
            for i in range(0,len(x)):
                y.remove(x[i])
        #用来存储之前有没有出过这个牌炸弹和三张都不会有重复的

        def sz(x, fangshi, previous_list=None):  # 第一次先传入self.card之后再传入新的copy副本，并且得创建新的poker对象
                                  # 都已经排好序啦！#传的两个参数，第一个是即将操作的对象！，第二个是本次操作的方式
            if len(x.card)==0:
                return 1
                #每次成功出完牌之后，返回1.程序不断回溯之后直到第一次return这些结果的加和
            elif fangshi=='shunzi':#找到顺子是哪些数字，remove这些数字就可以啦！
                if x.check_straight()==True:#Q:如果连续两次出顺子，出的顺子不一样的话，应该是算一次的。但是这种算法是算两次的
                    count = 0
                    target = '34567891JQKA'
                    #可以出的顺子有5、6、7、8四种情况！
                    #以下的四种情况可以用一个for循环类解决
                    cho=[3,2,1,0]
                    for div in cho:#这个来决定是几顺子。是底下所有情况的整合。从大往小来看。先从8顺子开始计算，不断让出牌的数量越来越少》》可以避免重复！
                        for i in range(0,len(target)-div-4):#8顺子是到-7.7顺子是到-6
                            xxx=list(set(x.card.copy()))
                            xxx.sort(key=sorting)
                            yyy=''.join(xxx)#没有重复元素的x.card》来判断去掉的顺子
                            a=yyy.find(target[i:i+5+div])
                            if a!=-1:#现在是5+div顺子了，出牌可能的选择8\7\6\5
                                new_list = x.card.copy()
                                new_str = ' '.join(new_list)
                                newpoker = Poker(new_str)
                                delete(target[i:i+5+div],newpoker.card)
                                #得到了删除了出过的顺子的newpoker
                                count += sz(newpoker,'shunzi')#【本次有顺子，出顺子的情况】用count来记录所有顺子的出牌情况并出完之后减去
                    count += sz(x, 'zhadan')#【本次有顺子，但不出顺子的情况】
                    return count
                else:
                    return sz(x,'zhadan')#本次没有顺子，直接进入zhadan级别的情况
                    #此时无法进行操作
                #count的作用
                #1、出当前级别的牌，有多少种出法都记录在内
                #2、不出当前级别的牌，直接进入下一种出法
                #》》就相当是一个容器，储存了所有会返回的情况。
                #》》不让本级别的情况还没遍历完了就return了！


            elif fangshi=='zhadan':#
                if x.check_count(4)==True:#有炸弹可以出
                                            # Q:如果连续两次出炸弹，出的炸弹不一样的话，应该是算一次的。但是这种算法是算两次的
                    count = 0
                    previous = None
                    for i in range(0,len(x.card)-3):
                        if x.card[i:i+4]==[x.card[i]]*4 and [x.card[i]]*4!=previous:#找到了炸弹的开始，下标为i
                            if previous_list == None or [x.card[i]]*4 <= previous_list:
                                new_list = x.card.copy()
                                new_str = ' '.join(new_list)
                                newpoker = Poker(new_str)
                                for j in range(0, 4):
                                    newpoker.card.remove(x.card[i])
                                count += sz(newpoker, 'zhadan', [x.card[i]]*4)
                                previous = [x.card[i]]*4
                    count += sz(x, 'sanlian')
                    return count
                else:
                    return sz(x,'sanlian')
                    #没有炸弹可以出

            elif fangshi == 'sanlian':#
                if x.check_count(3) == True:  # 有炸弹可以出
                    count = 0
                    previous = None
                    for i in range(0, len(x.card) - 2):
                        if x.card[i:i+3] == [x.card[i]]*3 and [x.card[i]]*3!=previous:  # 找到了炸弹的开始，下标为i
                            if previous_list == None or [x.card[i]]*3 <= previous_list:
                                new_list = x.card.copy()
                                new_str = ' '.join(new_list)
                                newpoker = Poker(new_str)
                                for j in range(0, 3):
                                    newpoker.card.remove(x.card[i])
                                count += sz(newpoker, 'sanlian', [x.card[i]]*3)
                                previous = [x.card[i]]*3
                    count += sz(x, 'duizi')
                    return count
                else:
                    return sz(x, 'duizi')
            elif fangshi=='duizi':#
                if x.check_count(2)==True:
                    count = 0
                    previous = None
                    for i in range(0,len(x.card)-1):
                        if x.card[i:i+2]==[x.card[i]]*2 and [x.card[i]]*2!=previous:
                            if previous_list == None or [x.card[i]]*2 <= previous_list:#precious_list==None的时候，应该是上一次没出对子
                                                                                        # 从更高级的牌直接下来的
                                new_list=x.card.copy()
                                new_str=' '.join(new_list)
                                newpoker=Poker(new_str)
                                newpoker.card.remove(x.card[i]);newpoker.card.remove(x.card[i])
                                count += sz(newpoker, 'duizi', [x.card[i]]*2)
                                previous = [x.card[i]]*2
                    count += sz(x, 'danzhang')
                    return count
                else:
                    return sz(x, 'danzhang')
            elif fangshi=='danzhang':#此时一定可以出的，len（x）==0在之前就已经被return了！
                return 1
        p=sz(self,'shunzi')
        return p
while True:
    exec(input())
'''
例如：手牌为A A A A，出牌方式有如下5种（AAA,A与A,AAA是相同组合）：
    1. A,A,A,A
    2. AA,AA
    3. A,AAA
    4. AAAA
    5. AA,A,A
'''
