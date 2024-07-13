'''
合法出牌：单，对，三，四，单顺
手牌上限：14
'''
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

while True:
    exec(input())
