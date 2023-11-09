package controllers.limitdepthfirst;

import controllers.limitdepthfirst.Node;
import core.game.Observation;
import core.game.StateObservation;
import core.player.AbstractPlayer;
import ontology.Types;
import tools.ElapsedCpuTimer;
import tools.Vector2d;

import java.awt.*;
import java.lang.reflect.Type;
import java.util.ArrayList;
import java.util.Random;
import java.util.Stack;

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

    protected Stack<Node> target_node= new Stack<Node>();
    //【深搜中操作】最终存放从根节点到叶节点的节点们（回溯的时候加入）
    protected Stack<Types.ACTIONS> sort_actions= new Stack<Types.ACTIONS>();
    //栈顶元素是根节点-》叶节点依次的动作

    protected Stack<Node> being_visit = new Stack<Node>();
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
        System.out.println("LimitdepthfirstSearch is ready");
    }

    /**
     * Picks an action. This function is called every game step to request an action
     * from the player.
     *
     */


    protected boolean is_difference_and_save(StateObservation current_state){
        for(StateObservation nodes_state : been_visited){
            if(nodes_state.equalPosition(current_state)){
                return false;
            }
        }
        been_visited.add(current_state);
        return true;
    }


    boolean first_time=true;//判断是不是第一次（一定要放到act函数的外边！）

    protected int MAX_DEPTH = 10;//搜索的最大深度10层【【【BUG】】】搜索深度很影响最终结果！
    //?但为什么会出现动不了的情况呢？

    //启发式函数
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

    public Types.ACTIONS act(StateObservation stateObs, ElapsedCpuTimer elapsedTimer) {
        //这个函数会被不断重复调用，而深度优先搜索其实只搜索一遍，可以得到所有的步骤，所以这个函数后面的部分只需要执行一次
        if(!sort_actions.empty())
            return sort_actions.pop();

        // 【重新初始化！】
        //因为每一次调用act函数（每一次做出决策之前）都需要进行一次深搜
        //所以每一次都需要对两栈、一集合进行重新初始化

        being_visit = new Stack<Node>();
        been_visited = new ArrayList<StateObservation>();
        target_node = new Stack<Node>();

        boolean depth_overflow = false;//超过了最大深度是true
        boolean key_flag = false;//拿到了钥匙了是true
        Node heur_best_node=null;//超过了MAX_depth之后，进入一个判断，对heur_best_node进行赋值
        //开始深搜，注意目标检测的时机（在要被being_visit的栈往外边拿的时候进行检测）
        while(true){
            if(first_time){//第一次进入，栈中什么都没有
                Node root = new Node();
                root.Node_state=stateObs.copy();
                root.Node_father=null;
                root.Node_action=null;
                root.depth=1;
                being_visit.push(root);
                target_node.push(root);
                first_time=false;
                continue;
            }

            //不是第一次进入，而且栈里边没有东西
            if (being_visit.empty())//此时没有子节点【上面的for循环不进去，即没有possible_action呢】
            {
                System.out.println("Stack Empty");
                continue;
            }

            //不是第一次进入，而且栈里边有东西
            if(!being_visit.empty()){
                Node current_father = being_visit.pop();//当前被pop的父节点
                //刚刚拿出来的节点：三个动作
                //1、目标判断
                //2、拿没拿到钥匙判断
                //3、超没超深度判断
                if (current_father.Node_state.getAvatarPosition().equals(keypos))//拿到了钥匙了
                //判断两个Vector2d的对象的横纵坐标是不是一样的【是不是一个点】
                //即判断当前玩家拿没拿到“钥匙”
                    key_flag = true;//拿到了钥匙
                if(current_father.depth > MAX_DEPTH)
                    depth_overflow=true;


                //【situation1：没有超过最深，而且结束了】
                if(!depth_overflow && current_father.Node_state.isGameOver()){//目标检测,结束了
                    if (current_father.Node_state.getGameWinner()==Types.WINNER.PLAYER_WINS){
                        //没有超最深深度，当前结束，而且是玩家获胜
                        target_node.push(current_father.clone());
                        break;//【唯一出循环的方式，找到了最终目标！】找到了最终目标
                    }
                    //没有超过最深深度，当前结束，而且不是玩家获胜，即输了捏！！
                    //直接进入下一次循环即可，(因为当前节点已经被being_visit给pop掉啦！)

                }

                //【situation2：没有超过深度，而且不是目标，游戏没有结束，要扩展当前节点】
                else if(!depth_overflow && !current_father.Node_state.isGameOver()){

                    //task1：对target_node进行管理
                    if(current_father.Node_father!=null){
                        if(current_father.Node_father.Node_state.equalPosition((target_node.peek()).Node_state))
                            target_node.push(current_father.clone());
                        else{
                            while(!current_father.Node_father.Node_state.equalPosition(target_node.peek().Node_state))
                                target_node.pop();
                            target_node.push(current_father.clone());
                        }
                    }

                    //task2：对being_visit进行管理
                    //判断当前节点可不可以扩展-没有出现过的状态而且当前没有结束
                    //只在这个节点作为父亲节点的时候才进行重复状态检查，产生的子节点不进行检查
                        //没有出现过的状态，而且当前没输！可以扩展current_father
                    ArrayList<Types.ACTIONS> actions = stateObs.getAvailableActions();
                        //所有当前状态可以操作的节点
                    for(Types.ACTIONS possible_action : actions){
                        //把当前所有可以走的步骤，以节点的形式呈现下一步的状态
                        Node node = new Node();
                        node.Node_father = current_father.clone();
                        node.Node_action = possible_action;
                        node.depth=current_father.depth+1;
                        StateObservation state_advance=current_father.Node_state.copy();//当前父节点的状态
                        state_advance.advance(possible_action);
                        node.Node_state = state_advance.copy();//【当前状态的第二个副本，给到子节点】
                        if(is_difference_and_save(state_advance))
                            being_visit.push(node.clone());//子节点没有和原来已有的状态一样
                        }
                    }

                //【situation3：超过了最大深度】
                else{
                    double min_value = 99999;//最小代价（距离目标或者钥匙最近的距离-最少的代价）
                    Node best_node = new Node();

                    // 利用启发函数挑选出一步最优动作
                    while (! being_visit.empty())
                    {
                        Node current_node = being_visit.pop();//当前栈里边没有被遍历的
                        double current_value = heuristic_function(current_node.Node_state, key_flag);
                        if (current_value < min_value)
                        {
                            min_value = current_value;
                            best_node = current_node.clone();
                        }
                    }

                    //到这里都是对的！
                    heur_best_node=best_node.clone();

                    //此时要对target_node进行管理，pop到是当前heur_best_node的父亲节点的位置！
                    // 再把heur_best_node加到这个栈里边呢
                    //BUGBUGBUG!从最终最优节点到根节点的动作加入有问题
                    if(heur_best_node.Node_father!=null){
                        if(heur_best_node.Node_father.Node_state.equalPosition((target_node.peek()).Node_state))
                            target_node.push(heur_best_node.clone());
                        else{
                            while(!heur_best_node.Node_father.Node_state.equalPosition(target_node.peek().Node_state))
                                target_node.pop();
                            target_node.push(heur_best_node.clone());
                        }
                    }
                    break;//【超过了深度就直接出去！找到了还没被遍历的最好节点了！】
                }
            }
        }

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

        return sort_actions.pop();
    }
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
