import random
from environment.GoEnv import Go
import time
from agent.agent import RandomAgent

if __name__ == '__main__':
    begin = time.time()
    env = Go()
    agents = [RandomAgent(idx) for idx in range(2)]

    for ep in range(1):
        time_step = env.reset()
        while not time_step.last():
            player_id = time_step.observations["current_player"]
            if player_id == 0:
                agent_output = agents[player_id].step(time_step)  #返回[action,prob],agent需要给出计算出来的动作
            else:
                agent_output = agents[player_id].step(time_step)
            action_list = agent_output.action  #获得最优的动作--以1-25+pass来表示下棋的位置或者不下
            time_step = env.step(action_list)     #在环境里执行动作

        # Episode is over, step all agents with final info state.
        for agent in agents:
            agent.step(time_step)
    print('Time elapsed:', time.time()-begin)
