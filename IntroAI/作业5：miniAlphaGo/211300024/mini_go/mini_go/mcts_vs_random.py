import random, collections,math
from absl import logging, flags, app
from numpy.random import normal
import numpy as np
from absl import logging, flags, app
from environment.GoEnv import Go
import time, os
from algorimths.dqn import DQN
import tensorflow as tf
import agent.agent as agent
from agent.agent import Node,MCTS

FLAGS = flags.FLAGS

flags.DEFINE_integer("num_train_episodes", 10000,
                     "Number of training episodes for each base policy.")
flags.DEFINE_integer("num_eval", 1000,
                     "Number of evaluation episodes")
flags.DEFINE_integer("eval_every", 2000,
                     "Episode frequency at which the agents are evaluated.")
flags.DEFINE_integer("learn_every", 128,
                     "Episode frequency at which the agents learn.")
flags.DEFINE_integer("save_every", 2000,
                     "Episode frequency at which the agents save the policies.")
flags.DEFINE_list("hidden_layers_sizes", [
    128, 128
], "Number of hidden units in the Q-net.")
flags.DEFINE_integer("replay_buffer_capacity", int(5e4),
                     "Size of the replay buffer.")
flags.DEFINE_integer("reservoir_buffer_capacity", int(2e6),
                     "Size of the reservoir buffer.")
StepOutput = collections.namedtuple("step_output", ["action", "probs"])


#alpha的快速走棋策略[此时就不采用神经网络啦]
def rollout_net(time_step, player_id):
    legal_actions = time_step.observations["legal_actions"][player_id]
    return random.choice(legal_actions)

#alpha估值网络
def value_net(time_step, player_id):
    return normal(scale=0.1)


#alpha的策略网络为下面经过DPN训练出来的深度学习网络

def main(unused_argv):
    begin = time.time()
    env = Go()
    info_state_size = env.state_size
    num_actions = env.action_size
    random_agent=agent.RandomAgent(0)
    hidden_layers_sizes = [int(l) for l in FLAGS.hidden_layers_sizes]
    kwargs = {    #借鉴dpn_vs_random_demo中的参数传入
        "replay_buffer_capacity": FLAGS.replay_buffer_capacity,
        "epsilon_decay_duration": int(0.6*FLAGS.num_train_episodes),
        "epsilon_start": 0.8,
        "epsilon_end": 0.001,
        "learning_rate": 1e-3,
        "learn_every": FLAGS.learn_every,
        "batch_size": 128,
        "max_global_gradient_norm": 10,
    }
   
    ret = [0]
    max_len = 2000
    with tf.Session() as sess:
        policy_net=DQN(sess, 0, info_state_size,num_actions, hidden_layers_sizes, **kwargs)
        policy_net.restore("saved_model/10000")
        for ep in range(10):
            print("MCTS trainging episode  "+str(ep))
            '''
            reset the game at the beginning of the game to get an initial state
        :return: should reset the env and return a initial state
            '''
            time_step = env.reset()#初始状态
            while not time_step.last():
                player_id = time_step.observations["current_player"]
                if player_id == 0:  #玩家1：采用MCTS
                    root=Node(None,env,time_step,None,0,0)
                    #策略网络为深度学习拿到的dqn
                    #快速走棋策略是random_rollout_net
                    #估值网络为random_value_net
                    mcts=MCTS(root,policy_net,value_net,rollout_net,env,time=5)#模拟的时间为5s
                    action_list=mcts.simulate()
                else:               #玩家2：随机策略
                    agent_output = random_agent.step(time_step).action
                    action_list = agent_output  #获得动作
                time_step = env.step(action_list)     
            print("MCTS vs random  ")
            print(time_step.rewards)
    print('Time elapsed:', time.time()-begin)


if __name__ == '__main__':
    app.run(main)
