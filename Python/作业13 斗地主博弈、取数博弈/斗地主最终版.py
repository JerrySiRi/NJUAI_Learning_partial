'''

题目：[Python,模拟] 斗地主博弈

题目描述：

描述：在某牌类游戏中，牌的大小关系根据牌的数码表示如下：3<4<5<6<7<8<9<10<J<Q<K<A<2<小王<大王，而花色并不对牌的大小产生影响。
每一局游戏中，一副手牌由 n 张牌组成。游戏者每次可以根据规定的牌型进行出牌，首先打光自己的手牌一方取得游戏的胜利。现设计对手牌的分析程序，对给定手牌的出牌方式进行分析。
为简化游戏规则，现不考虑2、小王、大王这三种牌码，即只保留 3<4<5<6<7<8<9<10<J<Q<K<A 这12种牌码，每种牌码的牌最多4张，手牌数量区间为[1,8]。

符合规则的牌型如下：
1. 单张：单张牌，如一张A。
2. 对子：两张数码相同牌，如AA。
3. 三连：三张数码相同牌，如AAA。
4. 炸弹：四张同数码牌，如AAAA。
5. 单顺子：五张或更多数码连续的单牌，如：34567, 8910JQKA
6. pass: 不出牌（如果上一轮对手出了牌，这一轮可以选择pass）

在第11周的上机测试中我们已经完成了【Poker类的设计】和【cal_all_ways()函数】的编写。假设现有A和B两位玩家在玩该牌类游戏，A先手且双方均明牌，请编写程序完成如下功能：

1. is_bigger(poker1: str, poker2: str) -> bool 函数，接受参数为两个牌型poker1和poker2（牌型符合规则，但不包含pass牌型）
    poker1和poker2可分别被视为【一个回合中--可以出相同类型的，也可以出不同类型的】的【先手牌】和【后手牌】
    要求判断后出的poker2是否比poker1大，是 返回 True；否则 返回 False。
    比较大小的规则如下：
    1. #同种牌型，比较点数, 点数大的胜，如：A A > 3 3; 4 4 4 4 > 3 3 3 3。（此时炸弹考虑相同牌型）
    2. #顺子牌型需在【张数相同】的情况下比较，不同长度的顺子是不同的牌型，如: 4 5 6 7 8 > 3 4 5 6 7。
    2. #炸弹大过其他牌型，（此时炸弹考虑不同牌型不同牌型）如：3 3 3 3 > A A。
    3. 牌型不同，直接返回False（即不能出牌型不同的牌）。

2. is_winner(A: str, B: str) -> bool 函数，接受参数为A和B的手牌表示
    要求判断A是否有必胜的策略，有则返回True；否则返回False。

提示：
代码框架中给了牌型枚举，对实现过程可能有帮助。

输入样例：
1.
输入：
print(is_bigger('3', '4'))
print(is_bigger('4', '4'))
print(is_bigger('3 4 5 6 7', '3 3 3 3'))
print(is_bigger('3 4 5 6 7', '3 4 5 6 7 8'))
exit()
输出：
True
False
True
False

2.
输入：
print(is_winner("3", "A"))
print(is_winner("3 4 5 6 7", "5 5 5 5"))
print(is_winner("3 3 7 7", "5 5 6 6"))
exit()
输出：
True
True
True


'''

# 牌型枚举
class CombType:
    PASS, SINGLE, PAIR, TRIPLE, STRIGHT, BOMB = range(6)


class Poker:
    def __init__(self, cards: str):
        self.lst = cards.split()
        new_lst = self.lst.copy()
        self.dict = dict()
        for card in new_lst:
            if card not in self.dict.keys():
                self.dict[card] = self.lst.count(card)

    def check_count(self, count: int) -> bool:
        """
        检查手牌中是否有单张、对子、三连、炸弹
        count 为 1 时，检查单张
        count 为 2 时，检查对子
        count 为 3 时，检查三连
        count 为 4 时，检查炸弹
        有，返回True；否则，返回False
        """
        for i in self.dict.values():
            if i >= count:
                return True
        return False

    def check_straight(self) -> bool:
        """
        检查手牌中是否有顺子
        有，返回True；否则，返回False
        """
        order_lst = ['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        for i in range(8):
            my_set = set(order_lst[i : i + 5])
            if my_set.issubset(set(self.dict.keys())):
                return True
        return False

    def cal_all_ways(self, previous_straight = None) -> int:
        """
        计算共有多少种不同的打光手牌的出牌组合，并返回该值。
        """
        ways_without_straight = 1
        for value in self.dict.values():
            if value == 4:
                ways_without_straight *= 5
            else:
                ways_without_straight *= value
        #分类讨论。情况1：不能从手牌中打出顺子：
        if not self.check_straight():
            return ways_without_straight
        #情况2：可以从手牌中打出顺子：
        else:
            all_ways = ways_without_straight    #子情况1：可以从手牌中打出顺子，但实际上不打出顺子。
            all_straights = []#所有顺子构成的列表。其中每个元素都是表示顺子的列表。
            order_lst = ['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
            for straight_length in range(5, 13):
                for i in range(13 - straight_length):
                    my_set = set(order_lst[i : i + straight_length])
                    if my_set.issubset(set(self.dict.keys())):
                        all_straights.append(order_lst[i : i + straight_length])
            for straight in all_straights:  #子情况2：可以从手牌中打出顺子，且实际上打出顺子。
                if previous_straight is None or straight >= previous_straight:
                #若先前没有打出顺子，或本次打出的顺子不小于上次打出的顺子(按照Python对列表的比较规则)，则将其计数，否则不计数，以此去除重复情况。
                    remaining_lst = self.lst.copy()
                    for card in straight:
                        remaining_lst.remove(card)
                    remaining_str = ' '.join(remaining_lst)
                    remaining_poker = Poker(remaining_str)
                    all_ways += remaining_poker.cal_all_ways(straight)
            return all_ways


'''
1. is_bigger(poker1: str, poker2: str) -> bool 函数，接受参数为两个牌型poker1和poker2（牌型符合规则，但不包含pass牌型）
    poker1和poker2可分别被视为【一个回合中--可以出相同类型的，也可以出不同类型的】的【先手牌】和【后手牌】
    要求判断后出的poker2是否比poker1大，是 返回 True；否则 返回 False。
    比较大小的规则如下：
    1. #同种牌型，比较点数, 点数大的胜，如：A A > 3 3; 4 4 4 4 > 3 3 3 3。（此时炸弹考虑相同牌型）
    2. #顺子牌型需在【张数相同】的情况下比较，不同长度的顺子是不同的牌型，如: 4 5 6 7 8 > 3 4 5 6 7。
    2. 炸弹大过其他牌型，（此时炸弹考虑不同牌型不同牌型）如：3 3 3 3 > A A。
    3. 牌型不同，直接返回False（即不能出牌型不同的牌）。
    
###认为传进来的一定是合法的呢！
'''
'''
step1：要创建两个poker对象，好用上面的函数
step2：没有炸弹的牌型-数量不同，直接返回False
       有炸弹的牌型-一个炸弹、两个炸弹
'''
def is_bigger(poker1: str, poker2: str) -> bool:
    poker_1=Poker(poker1)
    poker_2=Poker(poker2)
    poker1=poker1.split()
    poker2=poker2.split()
    if len(poker1)!=len(poker2) and len(poker1)!=4 and len(poker2)!=4:#没有炸弹、牌的数量不同
        return False
    elif len(poker1)!=len(poker2) and len(poker1)!=4 and len(poker2)==4:#前手出炸弹，后手不出炸弹
        return True
    elif len(poker1)!=len(poker2) and len(poker1)==4 and len(poker2)!=4:#后手出炸弹，前手不出炸弹（一定打的过）
        return False
    elif len(poker1)==len(poker2):#张数相同，来进行同牌型的比较
        if poker_1.check_straight()==False:#没有顺子的情况
            if poker1 >= poker2:                            #前比后大，不行呢
                return False
            else:
                return True
        elif poker_1.check_straight()==True:#有顺子的情况，且张数相同，通过在这个列表之中的下标，进行比较呢！
            order_lst = ['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
            #poker_1的第一个元素在这个列表中的下标
            index1=0
            index2=0
            for i in range(0,len(order_lst)):
                if order_lst[i]==poker_1.lst[0]:
                    index1=i
                if order_lst[i]==poker_2.lst[0]:
                    index2=i
            if index2>index1:
                return True
            else:
                return False



'''
2. is_winner(A: str, B: str) -> bool 函数，接受参数为A和B的手牌表示
    要求判断A是否有必胜的策略，有则返回True；否则返回False。
    
①A可以一下子都出完了！那A一定赢。
    五张牌以上：纯顺子
    五张牌以下：选取最大张数的牌进行出牌
'''
def whole(A: str) ->bool:
    poker_A=Poker(A)
    A=A.split()#把A变成列表啦！
    if poker_A.check_straight()==False :#没有顺子的情况，但牌的数量大于5张》》一次出不完
        if len(A)>=5:
            return False
        else:#有一次出完的可能性
            if poker_A.check_count(len(A))==True:
                return True
            else:
                return False
    else:#有顺子的情况
        order_lst = ['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        A=set(A)
        order_lst=set(order_lst)
        if A.issubset(order_lst):
            return True
        else:
            return False



'''
必胜策略：
要用到cal_all_ways()函数！
出牌策略是可以pass的！

必胜：A有一种出牌方式，无论B出什么样的牌，A都是可以赢的

一定是递归思路：
和取数博弈应该产生联系。子问题是（乙先出、甲后出）
【递归不需要知道具体的步骤，只需要告诉程序整体的流程就行！】

1、递归结束的状态：
A没有牌了,B有牌（A赢了）

'''

#def playing(A:str,B :str) ->bool:#出牌函数

def is_winner(A: str, B: str) -> bool:
    if whole(A):#A可以保证一次性出完
        return True
    else:
        return False


while True:
    exec(input())

'''
看看有没有什么灵感？

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
'''
'''



'''