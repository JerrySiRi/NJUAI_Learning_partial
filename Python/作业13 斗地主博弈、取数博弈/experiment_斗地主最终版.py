class Poker:
    def __init__(self, cards: str):
        self.lst = cards.split()
        new_lst = self.lst.copy()
        self.dict = dict()#这个地点记录了“所有的牌型”+“每种牌型所对应的张数”
        for card in new_lst:
            if card not in self.dict.keys():
                self.dict[card] = self.lst.count(card)

    def check_count(self, count: int) -> bool:
        for i in self.dict.values():
            if i >= count:
                return True
        return False

    def check_straight(self) -> bool:
        order_lst = ['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        for i in range(8):
            my_set = set(order_lst[i: i + 5])
            if my_set.issubset(set(self.dict.keys())):
                return True
        return False
#此时previous是别人出的、单次、合法的出牌方式！
    def cal_all_ways(self, previous=None) -> list:
        '''
        返回不同的响应打出手牌的方式构成的列表，列表的每个元素都是按牌序排列的字符串，各字符间以空格隔开。
        '''
        if previous is None:#这次是第一次出牌！
            ways_without_straight = []
            for card in self.dict.keys():#现在的”牌型：张数“所对应的字典
                ways_without_straight.append(' '.join([card] * self.dict[card]))
            if not self.check_straight():#检查-现在没有顺子了
                return ways_without_straight #没有顺子的情况下，所有的牌长得模样都是【’数值‘*个数】。所有出牌方式就是这些啦
            else:#检查，现在有顺子，上面的出牌方式只是其中的一部分。【所有的出牌方式】=【不出顺子的出牌方式--上面已经计算好了】+【出顺子的出牌方式】
                all_ways = ways_without_straight
                all_straights = []
                order_lst = ['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
                for straight_length in range(5, 13):
                    for i in range(13 - straight_length):
                        my_set = set(order_lst[i: i + straight_length])#循环完毕之后。是遍历了上面的order_list中所有大于五张的顺子
                        if my_set.issubset(set(self.dict.keys())):#现在的顺子，当前的牌型可以出出来
                            all_straights.append(' '.join(order_lst[i: i + straight_length]))
                all_ways += all_straights
                return all_ways#有顺子的情况下。【所有的出牌方式】=【不出顺子的出牌方式--上面已经计算好了】+【出顺子的出牌方式】-两部分都已经被计算啦！
        else:#前面一次有人出牌！现在是接他的牌的状态！要对前一个人出的牌作出相应。all_ways的牌应该是大过他的牌
            all_ways = []
            previous_class = 5
            previous_cards = Poker(previous)
            if len(previous) == 1:#前一次出的是’单张‘
                previous_class = 1
            else:
                for i in [4,3,2]:#前一次不只一张牌
                    if previous_cards.check_count(i):#看看前一次可不可以出除了单张之外的牌，如果可以出的话，就把previous_class变成最大的牌的数量
                        previous_class = i
                        break
            #以上的部分确定previous_class（前面人出的牌型）的数值
            #以下的部分来针对前面一个人出的牌型做出自己的策略
            if previous_class != 5:#前一个人出的4、3、2、1的牌型
                for card in self.dict.keys():
                    if is_bigger(previous, ' '.join([card] * self.dict[card])):#遍历自己和他数目相同的牌的种类
                        #如果牌型不匹配，且后者不是炸弹，就一定不行
                        #如果牌型不匹配，且后者是炸弹，可以
                        #如果牌型匹配，不管是不是炸弹，只要比前面的大，可以
                        all_ways.append(' '.join([card] * self.dict[card]))
                        #给is_bigger函数1、他的牌型。2、自己每种牌型*自己的数目。
                        #把比大小的任务都交给is_bigger函数！自己不再考虑如何去比大小！！！

            else:#前一个出’顺子‘，现在可以出’顺子‘或者’炸弹‘
                straight_length = len(previous.split())
                for card in self.dict.keys():
                    if self.dict[card] == 4:#自己的牌之中有炸弹，就一定打的过
                        all_ways.append(' '.join([card] * 4))

                order_lst = ['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
                for i in range(13 - straight_length):
                    my_set = set(order_lst[i: i + straight_length])#和前面一个人出的顺子个数一样的所有情况
                    straight = ' '.join(order_lst[i: i + straight_length])
                    if my_set.issubset(set(self.dict.keys())) and is_bigger(previous, straight):#这个顺子在其中 and 比前面的人出的牌要大
                        all_ways.append(straight)
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
    order_dict = dict(zip(('3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'), range(12)))
    cards1 = Poker(poker1)
    class1 = 5
    cards2 = Poker(poker2)
    class2 = 5
    if len(poker1) == 1:
        class1 = 1
    else:
        for i in range(4, 1, -1):
            if cards1.check_count(i):
                class1 = i
                break
    if len(poker2) == 1:
        class2 = 1
    else:
        for i in range(4, 1, -1):
            if cards2.check_count(i):
                class2 = i
                break
    if class1 != class2 and class2 != 4:
        return False
    elif class1 != class2 and class2 == 4:
        return True
    elif class1 == class2 and class1 == 5:
        if len(poker1) != len(poker2):
            return False
        else:
            return order_dict[poker2[0]] > order_dict[poker1[0]]
    else:
        return order_dict[poker2[0]] > order_dict[poker1[0]]





def is_winner(a: str, b: str, previous=None) -> bool:
    # 遍历a的所有出牌方式，若存在其中一种，使无论b如何响应，a都必胜，则a必胜。否则a非必胜。
    if not a:#a的牌是空的
        return True
    elif not b:#b的牌是空的
        return False
    cards_a = Poker(a)
    cards_b = Poker(b)
    #a对b的相应
    all_ways_of_a = cards_a.cal_all_ways(previous)#这次自己对前一次的出的牌一共有多少种响应方式（大过他的），返回每一种出牌的列表，每一种出牌方式以字符串存储下来！
    for cards in all_ways_of_a:#遍历a的所有出牌方式，cards是其中一种出牌方式
        remain_list_of_a = cards_a.lst.copy()
        for card in cards.split():#每一种出牌方式都变成了一个列表。（变成列表好运用列表中的remove函数）
            remain_list_of_a.remove(card)#删除了这种出牌方式cards
        remain_str_of_a = ' '.join(remain_list_of_a)
        #b对a的相应（在a作出对b上次的相应之后，b的不同相应）
        all_ways_of_b = cards_b.cal_all_ways(previous=cards)
        for cards_ in all_ways_of_b:#遍历b的所有对a出牌的响应情况
            remain_list_of_b = cards_b.lst.copy()
            for card in cards_.split():
                remain_list_of_b.remove(card)
            remain_str_of_b = ' '.join(remain_list_of_b)#删除了这种出牌方式
        #一个出牌轮回就此结束。a和b各出一轮（而在此过程之中，a和b分别有很多种出法，所以应该是在两个for循环之中进行递归的）
            if not is_winner(remain_str_of_a, remain_str_of_b, previous=cards_):#precious是b上一轮出的cards_，下一轮交给a进行反映！
                break#这种情况下a出的这种方式被b打败了（不是能赢的策略，直接对b的循环结束》》换a的出牌方式）
        else:#针对b出牌方式的循环正常退出（没有执行break子句）。这种情况下a的这种出牌方式，无论b怎么出，a都能赢（必胜策略）
            return True
    else:#针对a出牌方式的循环正常退出，没有一种a的出牌方式，能招架的住所有b的出牌方式（每一种在遍历b的出牌方式的时候，都输了！）
        return False


while True:
    exec(input())
'''

def is_bigger(poker1: str, poker2: str) -> bool:
    order_dict = dict(zip(('3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'), range(12)))
    cards1 = Poker(poker1)
    class1 = 5
    cards2 = Poker(poker2)
    class2 = 5
    if len(poker1) == 1:
        class1 = 1
    else:
        for i in range(4, 1, -1):
            if cards1.check_count(i):
                class1 = i
                break
    if len(poker2) == 1:
        class2 = 1
    else:
        for i in range(4, 1, -1):
            if cards2.check_count(i):
                class2 = i
                break
    if class1 != class2 and class2 != 4:
        return False
    elif class1 != class2 and class2 == 4:
        return True
    elif class1 == class2 and class1 == 5:
        if len(poker1) != len(poker2):
            return False
        else:
            return order_dict[poker2[0]] > order_dict[poker1[0]]
    else:
        return order_dict[poker2[0]] > order_dict[poker1[0]]



'''