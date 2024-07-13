class Poker:
    def __init__(self, cards: str):
        self.lst = cards.split()
        new_lst = self.lst.copy()
        self.dict = dict()
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
            my_set = set(order_lst[i : i + 5])
            if my_set.issubset(set(self.dict.keys())):
                return True
        return False

    def cal_all_ways(self) -> int:
        ways_without_straight = 1
        for value in self.dict.values():
            if value == 4:
                ways_without_straight *= 5
            else:
                ways_without_straight *= value
        if not self.check_straight():
            return ways_without_straight
        else:
            all_ways = ways_without_straight
            all_straights = []
            order_lst = ['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
            for stride in range(4):
                for i in range(8 - stride):
                    my_set = set(order_lst[i : i + 5 + stride])
                    if my_set.issubset(set(self.dict.keys())):
                        all_straights.append(order_lst[i : i + 5 + stride])
            for straight in all_straights:
                new_lst = self.lst.copy()
                for card in straight:
                    new_lst.remove(card)
                new_str = ' '.join(new_lst)
                new_poker = Poker(new_str)
                all_ways += new_poker.cal_all_ways()
            return all_ways

while True:
    exec(input())
