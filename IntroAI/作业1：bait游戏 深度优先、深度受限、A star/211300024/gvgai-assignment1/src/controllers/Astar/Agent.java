package controllers.Astar;

import core.game.Observation;
import core.game.StateObservation;
import core.player.AbstractPlayer;
import ontology.Types;
import tools.ElapsedCpuTimer;
import tools.Vector2d;

import java.awt.*;
import java.lang.reflect.Type;
import java.util.*;

/**
 * Created with IntelliJ IDEA. User: ssamot Date: 14/11/13 Time: 21:45 This is a
 * Java port from Tom Schaul's VGDL - https://github.com/schaul/py-vgdl
 */
public class Agent extends AbstractPlayer {

    /**
     * Random generator for the agent.
     */
    protected Random randomGenerator;


    /**二维网格列表，是当前地图的网格
     * Observation grid.
     */
    protected ArrayList<Observation> grid[][];

    /**
     * block size
     */
    protected int block_size;
    protected Vector2d goalpos;//用来存“目标”的位置的容器
    protected Vector2d keypos;//用来存“钥匙”的位置的容器

    protected Stack<Types.ACTIONS> sort_actions= new Stack<Types.ACTIONS>();
    //栈顶元素是根节点-》叶节点依次的动作

    protected PriorityQueue<Node> being_visit = new PriorityQueue<>();
    //【深搜中操作】正在访问扩展的栈中的节点们（即ppt中的stack）

    protected ArrayList<StateObservation> been_visited = new ArrayList<StateObservation>();
    //【深搜中操作】已经访问过的节点（如果走过多步回到了当前状态，那么就不扩展当前节点！）
    //每走一步都应该给benn_visited中加入新元素（如果已经在就不加入了）





    /**
     * Public constructor with state observation and time due.
     *
     * @param so           state observation of the current game.
     * @param elapsedTimer Timer for the controller creation.
     */
    public Agent(StateObservation so, ElapsedCpuTimer elapsedTimer) {
        randomGenerator = new Random();
        grid = so.getObservationGrid();//返回当前状态地图中的网格
        block_size = so.getBlockSize();//即本题的默认值50
        ArrayList<Observation>[] fixedPositions = so.getImmovablePositions();
        ArrayList<Observation>[] movingPositions = so.getMovablePositions();
        goalpos = fixedPositions[1].get(0).position; //目标的坐标
        keypos = movingPositions[0].get(0).position;//钥匙的坐标
        System.out.println("A star is ready");
    }

    /**
     * Picks an action. This function is called every game step to request an action
     * from the player.
     *
     */

    //在加入子节点的时候使用【只判断有没有和“已经扩展过的节点重复！”】
    protected boolean is_difference(StateObservation current_state){
        for(StateObservation nodes_state : been_visited){
            if(nodes_state.equalPosition(current_state)){
                return false;
            }
        }
        return true;
    }


    //在父亲节点拿出来的时候使用【只对been_visited进行状态的加入，已经判断过不在里边啦！】
    protected void save_state(StateObservation current_state){
        been_visited.add(current_state);
    }


    boolean first_time=true;//判断是不是第一次（一定要放到act函数的外边！）

    protected int MAX_DEPTH = 10;//搜索的最大深度10层【【【BUG】】】搜索深度很影响最终结果！
    //?但为什么会出现动不了的情况呢？

    //f(n)=g(n)+h(n)
    // 【是h(n)】启发式函数
    private double heuristic_function(StateObservation stateObs, boolean key_flag)
    {
        Vector2d state_vec = stateObs.getAvatarPosition();//返回玩家位置（游戏没结束的时候）
        if (key_flag)//找到了钥匙
        {
            return state_vec.dist(goalpos);//【当前目标就是找到“目标”（已经拿到了钥匙）】
            //返回当前位置（玩家位置）和传进来参数位置（“目标”位置）的距离！
        }

        return state_vec.dist(keypos)+goalpos.dist(keypos);//【当前目标就是找到“钥匙”（没拿到钥匙呢！）】;
        //计算玩家新位置和“钥匙”的距离+“钥匙”距离“目标”的距离
    }

    // 【不是g(n)!!!!】父节点-当前节点的消耗，过去的消耗（父亲节点的消耗+当前步骤的消耗）
    private double past_cost(Node current_node){
        Node father_node=current_node.Node_father.clone();//但可能father_node是null呢！
        if(father_node==null)
            return 0;//整棵树的根节点！！！
        Vector2d past_vec = father_node.Node_state.getAvatarPosition();
        Vector2d curr_vec = current_node.Node_state.getAvatarPosition();
        return curr_vec.dist(past_vec);
    }

    //f(n) = (past_cost(Node)+Node.father_node.previous_cost) + heuristic_function(state...)



    public Types.ACTIONS act(StateObservation stateObs, ElapsedCpuTimer elapsedTimer) {
        //这个函数会被不断重复调用，而深度优先搜索其实只搜索一遍，可以得到所有的步骤，所以这个函数后面的部分只需要执行一次
        if (!sort_actions.empty())
            return sort_actions.pop();

        // 【重新初始化！】
        //因为每一次调用act函数（每一次做出决策之前）都需要进行一次深搜
        //所以每一次都需要对两栈、一集合进行重新初始化

        being_visit = new PriorityQueue<Node>();
        been_visited = new ArrayList<StateObservation>();
        Node yes_node = null;

        boolean depth_overflow = false;//超过了最大深度是true
        boolean key_flag = false;//拿到了钥匙了是true
        Node heur_best_node = null;//超过了MAX_depth之后，进入一个判断，对heur_best_node进行赋值
        //开始深搜，注意目标检测的时机（在要被being_visit的栈往外边拿的时候进行检测）
        while (true) {
            if (first_time) {//第一次进入，栈中什么都没有
                Node root = new Node();
                root.Node_state = stateObs.copy();
                root.Node_father = null;
                root.Node_action = null;
                root.depth = 1;
                root.previous_cost = 0;
                root.priority = heuristic_function(stateObs, false);
                being_visit.add(root);
                first_time = false;
                continue;
            }

            //不是第一次进入，而且栈里边没有东西
            if (being_visit.isEmpty())//此时没有子节点【上面的for循环不进去，即没有possible_action呢】
            {
                System.out.println("Stack Empty");
                continue;
            }

            //不是第一次进入，而且栈里边有东西
            Node current_father = being_visit.remove();//当前被remove的父节点【优先级最小的】
            save_state(current_father.Node_state);//把准备扩展的节点加入扩展的状态之中！

            //刚刚拿出来的节点：两个动作（拿没拿到钥匙 在调用heuristic函数的时候就已经赋值过啦！）
            //1、目标判断
            //2、超没超深度判断
            if (current_father.depth > MAX_DEPTH)
                depth_overflow = true;
            //【situation1：没有超过最深，而且结束了】
            if (!depth_overflow && current_father.Node_state.isGameOver()) {//目标检测,结束了
                if (current_father.Node_state.getGameWinner() == Types.WINNER.PLAYER_WINS) {
                    //没有超最深深度，当前结束，而且是玩家获胜
                    yes_node = current_father.clone();
                    break;//【唯一出循环的方式，找到了最终目标！】找到了最终目标
                }


            }

            //【situation2：没有超过深度，而且不是目标，游戏没有结束，要扩展当前节点】
            else if (!depth_overflow && !current_father.Node_state.isGameOver()) {
                //task2：对being_visit进行管理
                //判断当前节点可不可以扩展-没有出现过的状态而且当前没有结束
                //只在这个节点作为父亲节点的时候才进行重复状态检查，产生的子节点不进行检查
                //没有出现过的状态，而且当前没输！可以扩展current_father
                ArrayList<Types.ACTIONS> actions = stateObs.getAvailableActions();
                //所有当前状态可以操作的节点
                for (Types.ACTIONS possible_action : actions) {
                    //把当前所有可以走的步骤，以节点的形式呈现下一步的状态
                    Node node = new Node();
                    node.Node_father = current_father.clone();
                    node.Node_action = possible_action;
                    node.depth = current_father.depth + 1;
                    StateObservation state_advance = current_father.Node_state.copy();//当前父节点的状态
                    state_advance.advance(possible_action);
                    node.Node_state = state_advance.copy();//【当前状态的第二个副本，给到子节点】
                    node.previous_cost = past_cost(node) + node.Node_father.previous_cost;
                    if (node.Node_state.getAvatarPosition().equals(keypos))
                        key_flag = true;
                    node.priority = node.previous_cost + heuristic_function(state_advance, key_flag);
                    if (is_difference(state_advance))//没有和已经扩展的节点状态相同
                        being_visit.add(node.clone());//子节点没有和原来已有的状态一样
                }
            }

            //【situation3：超过了最大深度,直接选出priority最小的节点】
            else {
                heur_best_node = being_visit.remove();
                break;
            }
        }


        if (heur_best_node != null)//超过了深度，yes_node就是heur_best_node了
            yes_node = heur_best_node;
        //没有超过深度就找到了最终节点，yes_node就是最终状态的current_father

        //TODO：依据heur_best_node是不是被赋值了，对sort-actions进行更新这种方式可以直接对sort-action进行管理啦！
        /*
          【因为此时remove出来的节点可能会比较跳跃，所以需要从根节点进行完整遍历！找到当前的路径】
        */
        ArrayList<Types.ACTIONS> all_actions = new ArrayList<Types.ACTIONS>();
        all_actions.add(Types.ACTIONS.ACTION_DOWN);
        all_actions.add(Types.ACTIONS.ACTION_LEFT);
        all_actions.add(Types.ACTIONS.ACTION_RIGHT);
        all_actions.add(Types.ACTIONS.ACTION_UP);
        assert yes_node != null;
        sort_actions.push(yes_node.Node_action);
        Node current_node = yes_node.Node_father.clone();
        Types.ACTIONS action_to_push = current_node.Node_action;
        StateObservation last_state = current_node.Node_father.Node_state;
        while (true) {
            if (current_node.Node_father == null) {
                break;//
            }
            for (Types.ACTIONS action : all_actions) {
                last_state = current_node.Node_father.Node_state.copy();
                last_state.advance(action);
                if (last_state.equalPosition(current_node.Node_state)) {
                    action_to_push = action;
                    break;
                }

            }
            sort_actions.push(action_to_push);
            if (last_state.equalPosition(stateObs)) {
                break;//深度受限的时候调用act函数的时候，此时根节点不一定是null
            }
            current_node = current_node.Node_father.clone();
        }
        //此时sort_actions就是从子节点到当前节点的路径啦！！！
        if (depth_overflow) {
            Types.ACTIONS ultimate = sort_actions.pop();//当前sort_actions的顶就是根节点到第一个结点的动作啦！
            sort_actions = new Stack<Types.ACTIONS>();
            //BUG:如果这里再使用Stack创建一个名字叫sort_actions的对象，就会进入死局
            return ultimate;
        }
        return sort_actions.pop();
    }




/*
        //TODO:【现在有两种情况】
        // s1:heur_best_node 不是null-触发了启发式函数 。对target_node进行pop+push，只返回一步，并且重置！
        // s2：heur_best_node是null-当前在10个深度内找到了赢得策略，和深度优先一样，直接全部返回

        while(!target_node.empty())
            sort_actions.push((target_node.pop().Node_action));
        if(depth_overflow){
            sort_actions.pop();//【【【【BUG】】】!!!拿出来的是当前根节点到上一轮的动作，这是必须拿出来的
            Types.ACTIONS ultimate=sort_actions.pop();
            sort_actions= new Stack<Types.ACTIONS>();

            //BUG:如果这里再使用Stack创建一个名字叫sort_actions的对象，就会进入死局
            return ultimate;
        }
*/


    /**
     * Prints the number of different types of sprites available in the "positions" array.
     * Between brackets, the number of observations of each type.
     * @param positions array with observations.
     * @param str identifier to print
     */
    private void printDebug(ArrayList<Observation>[] positions, String str)
    {
        if(positions != null){
            System.out.print(str + ":" + positions.length + "(");
            for (ArrayList<Observation> position : positions) {
                System.out.print(position.size() + ",");
            }
            System.out.print("); ");
        }else System.out.print(str + ": 0; ");
    }

    /**
     * Gets the player the control to draw something on the screen.
     * It can be used for debug purposes.
     * @param g Graphics device to draw to.
     */
    public void draw(Graphics2D g)
    {
        int half_block = (int) (block_size*0.5);
        for(int j = 0; j < grid[0].length; ++j)
        {
            for(int i = 0; i < grid.length; ++i)
            {
                if(grid[i][j].size() > 0)
                {
                    Observation firstObs = grid[i][j].get(0); //grid[i][j].size()-1
                    //Three interesting options:
                    int print = firstObs.category; //firstObs.itype; //firstObs.obsID;
                    g.drawString(print + "", i*block_size+half_block,j*block_size+half_block);
                }
            }
        }
    }
}

