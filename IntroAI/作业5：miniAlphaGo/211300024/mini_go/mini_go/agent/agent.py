'''
import random, collections
StepOutput = collections.namedtuple("step_output", ["action", "probs"])


class Agent(object):
    def __init__(self):
        pass

    def step(self, timestep):
        raise NotImplementedError


class RandomAgent(Agent):
    def __init__(self, _id):
        super().__init__()
        self.player_id = _id

    def step(self, timestep):
        cur_player = timestep.observations["current_player"]
        return StepOutput(action=random.choice(timestep.observations["legal_actions"][cur_player]), probs=1.0)

'''

import random, collections, math
import time
from absl import logging, flags, app
from numpy.random import normal
import numpy as np
import copy
import math



'''

Python 内建普通元组 tuple 存在一个局限，即不能为 tuple 中的元素命名，故 tuple 所要表达的意义并不明显。

因此，引入一工厂函数 (factory function) collections.namedtuple，以构造一个带字段名的 tuple。
具名元组 namedtuple 的实例和普通元组 tuple 消耗的内存一样多 (因为字段名都被保存在对应的类中) 
但却更具可读性 (namedtuple 使 tuple 变成自文档，根据字段名很容易理解用途)，令代码更易维护；
同时，namedtuple 不用命名空间字典(namespace dictionary) __dict__ 来存放/维护实例属性，故比普通 dict 更加轻量和快速。
但注意，具名元组 namedtuple 继承自 tuple ，其中的属性均不可变。

'''
StepOutput = collections.namedtuple("step_output", ["action", "probs"])
#环境执行一步玩家的落子动作，返回一个timestep数组（就是StepOutput函数返回的数组）
#包含1、落子后的棋盘状态  2、对应的结果  3、 是否结束的信息

class Agent(object):
    def __init__(self):
        pass

    def step(self, timestep):
        raise NotImplementedError




class RandomAgent(Agent):
    def __init__(self, _id):
        super().__init__()
        self.player_id = _id

    def step(self, timestep):
        cur_player = timestep.observations["current_player"]
        return StepOutput(action=random.choice(timestep.observations["legal_actions"][cur_player]), probs=1.0)




class Node(object):
    def __init__(self, parent, env, time_step, action, P, Q):
        self.initial_state = time_step  # 初始状态,用来对局到最后评分的
        self.env = env#当前环境
        self.cur_id = self.initial_state.observations["current_player"]  # 是哪个玩家
        self.actions = self.initial_state.observations["legal_actions"][self.cur_id]#当前节点可以做出哪些动作
        #即有哪些子节点
        self.parent = parent  # 父节点-用来回溯更新的
        self.children = []#当前节点的子节点
        self.action = action  # 做了哪个动作到的当前节点
        self.Q = Q#mcts中对当前节点的估计
        self.N = 0#对当前节点的访问次数
        self.P = P#mcts中的先验概率

'''
time_step = env.reset()

root=Node(None,env,time_step,None,0,0)
                    #策略网络为深度学习拿到的dqn
                    #快速走棋策略是random_rollout_net
                    #估值网络为random_value_net
mcts=MCTS(root,dqn,random_value_net,random_rollout_net,env,time_limit=5)
'''

class MCTS(object):
    def __init__(self, root, policy_net, value_fn, rollout_fn, env, time=10):
        self.policy_net = policy_net.policy_fn  # 深度学习拿到的策略网络
        self.value_net = value_fn  # 估值网络
        self.rollout_net = rollout_fn # 快速走棋的策略网络
        self.time_limit = time#运行的时间限制
        self.root = root


    def runing(self):
        '''
        在simulate函数中调用，在规定的时间内进行搜索

        '''
        node = self.root
        while len(node.children) != 0:#有子状态可以选择
            node = self.select(node)
        if node.N > 1 or node.parent == None:
            self.expand(node)
            node = self.select(node)
        reward = self.rollout(node)
        self.trace_back(node, reward)

    def select(self, node):
        '''
        蒙特卡洛的第一步-选择
        选择最大置信度Q+U的子节点
        此时设定超参数c=1
        '''

        if node.cur_id == 0:
            node.children.sort(key=lambda child: child.Q + child.P * math.sqrt(node.N) / (1 + child.N))
        else:
            node.children.sort(key=lambda child: -child.Q + child.P * math.sqrt(node.N) / (1 + child.N))

        return node.children[-1]

    def expand(self, node):
        '''
        select选择到一个节点之后，且该节点所代表的的游戏局面没有结束
        》》expand这个节点---创建一系列可能子节点，且对应的子节点之中存了从此节点做出的动作到子节点

        '''
        for action in node.actions:#所有的可选动作》》产生对应子节点
            envs = copy.deepcopy(node.env)
            timestep = envs.step(action)#从父节点依据可选动作产生新的局面
            xianyan = self.cul_P(timestep)
            P = xianyan[action]
            Q = self.cul_Q(timestep)
            child = Node(node, envs, timestep, action, P, Q)
            node.children.append(child)

    def cul_Q(self, timestep):#估值网络，计算Q值
        return self.value_net(timestep, timestep.observations["current_player"])

    def cul_P(self, timestep):#深度学习拿到的策略网络，计算P
        return self.policy_net(timestep, timestep.observations["current_player"])



    def rollout(self, node):
        timestep = node.initial_state
        env = copy.deepcopy(node.env)
        legal_actions = node.actions
        while not timestep.last():#直到当前对局结束
            c_player = timestep.observations["current_player"]
            action = self.rollout_net(timestep, c_player)#快速走步来选择action
            timestep = env.step(action)
        return timestep.rewards[node.cur_id]

    def trace_back(self, node, value):
        while node.parent != None:
            node.N += 1
            node.Q = (node.N * node.Q + value) / node.N
            node = node.parent

    def simulate(self):
        start_time = time.time()
        while True:
            self.runing()
            if time.time() - start_time >= self.time_limit:#模拟的时间到了
                self.root.children.sort(key=lambda node: node.Q/(node.N+1)+
                                                         math.sqrt(math.log(self.root.N+1)/(node.N+1)))
                #选择UCT值最大的【平衡探索和利用】
                return self.root.children[0].action
