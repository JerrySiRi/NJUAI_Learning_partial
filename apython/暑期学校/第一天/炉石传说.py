'''
测试用例：
1.
输入：
2
end
end

输出：
0
30
[]
30
[]

2.
输入：
4
summon 1 2 2
summon 1 2 3
end
summon 1 3 4
输出：
0
30
[3, 2]
30
[4]

3.
输入：
4
summon 1 2 2
summon 2 2 3
end
summon 1 3 4
输出：
0
30
[2, 3]
30
[4]


4.
输入：
4
summon 1 2 2
heal 0 10
end
summon 1 3 4
输出：
0
30
[2]
30
[4]

5.
输入：
4
summon 1 1 6
end
summon 1 3 4
attack 1 1
输出：
0
30
[3]
30
[3]

6.
输入：
4
summon 1 1 3
end
summon 1 3 4
attack 1 1
输出：
0
30
[]
30
[3]

7.
输入：
10
summon 1 3 6
summon 2 4 2
end
summon 1 4 5
summon 1 2 1
attack 1 2
end
attack 1 1
end
attack 1 0
输出：
0
26
[2]
30
[2]

8.
输入：
5
summon 1 30 30;end;summon 1 3 4;end;attack 1 0
输出：
1
30
[30]
0
[4]

9.
输入：
4;summon 1 3 3;end;summon 1 100 100;attack 1 0
输出：
-1
-70
[3]
30
[100]

10.【有问题】
输入：
summon 1 3 6;summon 2 4 2;end;#[1]
summon 1 4 5;summon 1 2 1;attack 1 2;end;#[2]
attack 1 1;end;attack 1 0;heal 1 4;end;#[1]
heal 0 5;summon 1 12 12;attack 1 1;attack 1 0;end;#[2]
summon 1 8 8;attack 1 0;summon 2 9 10;attack 2 1;end;#[1]
summon 2 18 18;attack 2 0#[2]
输出：
1
22
[2, 18]
0
[8]
'''

'''
【有一个wa的BUG】
游戏在一个战斗棋盘上进行，由两名玩家轮流进行操作，本题所使用的炉石传说游戏的简化规则如下：
    * 玩家会控制一些角色，每个角色有自己的生命值和攻击力。当生命值小于等于 0 时，该角色死亡。【角色分为英雄和随从。】
    * 玩家【各控制一个英雄】，游戏开始时，英雄的生命值为 30，攻击力为 0。当英雄死亡时，游戏结束，英雄未死亡的一方获胜。
    * 玩家可在游戏过程中召唤随从。棋盘上每方都有【 7 个可用于放置随从的空位】，从左到右一字排开，被称为战场。当随从死亡时，它将被从战场上移除。
    * 游戏开始后，两位玩家轮流进行操作，每个玩家的连续一组操作称为一个回合。
    * 每个回合中，当前玩家可进行【零个】或者【多个】以下操作：
        1) 召唤随从：玩家召唤一个随从进入战场，随从具有指定的生命值和攻击力。
        2) 随从攻击：玩家控制自己的某个随从【攻击对手的英雄】或者【某个随从】。
        3）治疗：玩家为己方的指定角色【只能恢复其中一个角色！】恢复一定的生命值。
        4) 结束回合：玩家声明自己的当前回合结束，游戏将进入对手的回合。该操作一定是一个回合的最后一个操作。
      * 当随从攻击时，攻击方和被攻击方会同时【对彼此】造成等同于自己攻击力的伤害。
        受到伤害的角色的生命值将会减少，数值等同于受到的伤害。
            例如，随从 X 的生命值为 HX、攻击力为 AX，随从 Y 的生命值为 HY、攻击力为 AY，
            如果随从 X 攻击随从 Y，则攻击发生后随从 X 的生命值变为 HX - AY，随从 Y 的生命值变为 HY - AX。攻击发生后，角色的生命值可以为负数。
      * 当治疗时，治疗的目标均为己方的角色（无法治疗已死亡的角色），且恢复后的生命值不能超出角色初始的生命值上限
            例如：对于初始生命值为10的随从。

本题将给出一个游戏的过程，要求编写程序模拟该游戏过程并输出最后的局面。

输入格式：
输入一行用";"分号划分的操作，每个操作格式如下：（所有的操作格式都是一样的！）
<action> <arg1> <arg2> ...
其中<action>表示操作类型，是一个字符串，共有 3 种：summon表示召唤随从，attack表示随从攻击，heal表示治疗，end表示结束回合。这 4 种操作的具体格式如下：
* summon <position> <attack> <health>：当前玩家在位置<position>召唤一个生命值为<health>、攻击力为<attack>的随从。
    其中<position>是一个 1 到 7 的整数，表示召唤的随从出现在战场上的位置，原来该位置及右边的随从都将顺次向右移动一位。
* attack <attacker> <defender>：当前玩家的角色<attacker>攻击对方的角色 <defender>。
    <attacker>是 1 到 7 的整数，表示发起攻击的本方随从编号，
    <defender>是 0 到 7 的整数，表示被攻击的对方角色，0 表示攻击对方英雄，1 到 7 表示攻击对方随从的编号。
* heal <position> <health>: 当前玩家对己方<position>的角色恢复<health>点生命值。
    <position>是 0 到 7 的整数，表示被治疗的角色，0 表示己方英雄，1 到 7 表示己方随从的编号。
* end：当前玩家结束本回合。
注意：随从的编号会随着游戏的进程发生变化，当召唤一个随从时，玩家指定召唤该随从放入战场的位置，此时，原来该位置及右边的所有随从编号都会增加 1。
    而当一个随从死亡时，它右边的所有随从编号都会减少 1。任意时刻，战场上的随从总是从1开始连续编号。

输出格式：
输出共 5 行。
第 1 行包含一个整数，表示这 n 次操作后（以下称为 T 时刻）游戏的胜负结果
    1 表示先手玩家获胜，-1 表示后手玩家获胜，0 表示游戏尚未结束，还没有人获胜。
第 2 行包含一个整数，表示 T 时刻先手玩家的英雄的生命值。
第 3 行包含一个列表，表示己方场上随从在 T 时刻的生命值（按照从左往右的顺序）。
第 4 行和第 5 行与第 2 行和第 3 行类似，只是将玩家从先手玩家换为后手玩家。

样例输入：

summon 1 3 6;summon 2 4 2;end;summon 1 4 5;summon 1 2 1;attack 1 2;end;attack 1 1

样例输出：
0     有没有胜负，谁赢谁输？
30    先手玩家生命值
[2]   先手玩家的随从当前时刻的生命值（从左往右）
30    后手玩家生命值
[2]   后手玩家的随从当前时刻的生命值（从左往右）

样例说明：
1. 先手玩家在位置 1 召唤一个生命值为 6、攻击力为 3 的随从 A，是本方战场上唯一的随从。
2. 先手玩家在位置 2 召唤一个生命值为 2、攻击力为 4 的随从 B，出现在随从 A 的右边。
3. 先手玩家回合结束。
4. 后手玩家在位置 1 召唤一个生命值为 5、攻击力为 4 的随从 C，是本方战场上唯一的随从。
5. 后手玩家在位置 1 召唤一个生命值为 1、攻击力为 2 的随从 D，出现在随从 C 的左边。
6. 随从 D 攻击随从 B，双方均死亡。
7. 后手玩家回合结束。
8. 随从 A 攻击随从 C，双方的生命值都降低至 2。

测试数据说明：
* 随从的初始生命值为 1 到 100 的整数，攻击力为 0 到 100 的整数。
* 保证所有操作均合法，包括但不限于：
　　1) 召唤随从的位置一定是合法的，即如果当前本方战场上有 m 个随从，则召唤随从的位置一定在 1 到 m + 1 之间，其中 1 表示战场最左边的位置，m + 1 表示战场最右边的位置。
　　2) 当本方战场有 7 个随从时，不会再召唤新的随从。
　　3) 发起攻击和被攻击的角色一定存在，发起攻击的角色攻击力大于 0。
　　4) 一方英雄如果死亡，就不再会有后续操作。

'''

'''
每一个玩家可以进行的操作和被进行的操作：
1、英雄进行的操作：    
    ①召唤随从
    ②对另一方英雄、他的随从进行攻击
    ③治疗己方英雄、己方随从

2、随从进行的操作：
    ①攻击敌方英雄或者随从
'''

class player:
    def __init__(self,num):
        self.exp=30
        self.suicongs=[]#按照顺序排列的啦！
        self.num=num
    def zhaohuan(self,position,attack,health):
        self.suicongs.insert(position-1,sui(attack,health))#insert的是列表下标的位置，position是从1开始的！！！

    def attack(self,attacker,defender):#attacker本方发动攻击（1-7）。defender被攻击方（0-7）
        attacker-=1;defender-=1
        if defender==-1:
            if self.num==1:#发动攻击的是玩家1
                game2.exp-=self.suicongs[attacker].attack
            else:#发动攻击的是玩家2
                game1.exp-=self.suicongs[attacker].attack
        else:
            if self.num==1:#当前玩家是1号，发动攻击的随从attacker，被攻击的是game2的defender
                game1.suicongs[attacker].health-=game2.suicongs[defender].attack
                game2.suicongs[defender].health-=game1.suicongs[attacker].attack
            else:#2号玩家来攻击，attacker来自2号玩家。defender来自1号玩家
                game2.suicongs[attacker].health-=game1.suicongs[defender].attack
                game1.suicongs[defender].health-=game2.suicongs[attacker].attack

    def die(self):#每次调用两次，看看两方是不是都得改变当前列表【tip：每次攻击完成之后只能又有一个随从死亡】
        for i in self.suicongs:
            if i.health<=0:
                self.suicongs.remove(i)

    def heal(self,position,health):
        if (self.suicongs[position-1].health+health)>=self.suicongs[position-1].initial:
            self.suicongs[position-1].health=self.suicongs[position-1].initial
        else:
            self.suicongs[position-1].health+=health


class sui:
    def __init__(self,attack,health):
        self.health=health
        self.attack=attack
        self.initial=health

'''
样例输入：

summon 1 1 16;summon 2 1 20;end;summon 1 4 50;summon 1 2 14;attack 1 2;attack 2 2;attack 2 0;heal 2 1;end;attack 1 1

样例输出：
0     有没有胜负，谁赢谁输？
30    先手玩家生命值
[2]   先手玩家的随从当前时刻的生命值（从左往右）
30    后手玩家生命值
[2]   后手玩家的随从当前时刻的生命值（从左往右）
'''

manip=input().split(';')#每一个元素都是两方的操作
caozuo=[]
for i in manip:
    caozuo.append(i.split())
game1=player(1)
game2=player(2)
#tip:每次攻击完了之后都得调用双方的“死亡”函数，看一看要不要改position
game=1
for i in caozuo:
    if i[0]=='summon':
        if game==1:#玩家1操作
            game1.zhaohuan(int(i[1]),int(i[2]),int(i[3]))
        else:
            game2.zhaohuan(int(i[1]),int(i[2]),int(i[3]))
    elif i[0]=='attack':
        if game==1:
            game1.attack(int(i[1]),int(i[2]))
            game1.die()
            game2.die()
        else:
            game2.attack(int(i[1]),int(i[2]))
            game2.die()
            game1.die()
    elif i[0]=='heal':
        if game==1:
            game1.heal(int(i[1]),int(i[2]))
        else:
            game2.heal(int(i[1]),int(i[2]))
    elif i[0]=='end':
        if game==1:
            game=2
        else:
            game=1
def sheng(game1,game2):
    if game2.exp<=0:#先手玩家获胜
        return 1
    elif game1.exp<=0:#后手玩家获胜
        return -1
    else:
        return 0
def shengming(game_x):
    l=[]
    for i in game_x.suicongs:
        l.append(i.health)
    return l
print(sheng(game1,game2))
print(game1.exp)
print(shengming(game1))
print(game2.exp)
print(shengming(game2))

