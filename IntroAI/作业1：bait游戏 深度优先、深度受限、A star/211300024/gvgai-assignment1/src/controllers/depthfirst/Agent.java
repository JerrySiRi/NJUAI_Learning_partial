package controllers.depthfirst;
import java.awt.Graphics2D;
import java.util.ArrayList;
import java.util.Random;
import java.util.Stack;

import core.game.Observation;
import core.game.StateObservation;
import core.player.AbstractPlayer;
import ontology.Types;
import tools.ElapsedCpuTimer;



/*
第一题：题目要求
* 针对第一个关卡，实现深度优先搜索 controllers.DepthFirst.java:
* 在游戏一开始就使用深度优先搜索找到成功的路径通关，记录下路径，并在之后每一步按照路径执行动作。
* 注意在搜索时避免回路，可使用StateObservation类的equalPosition方法判断状态是否相等。
* 由于搜索到通关路径所需时间较长，通过CompetitionParameters.ACTION_TIME来设置足够的时间来允许完成搜索。

*/


/*
以下是直接赋值而来sampleRandom的全部代码，
 */


/**
 * Created with IntelliJ IDEA.
 * User: ssamot
 * Date: 14/11/13
 * Time: 21:45
 * This is a Java port from Tom Schaul's VGDL - https://github.com/schaul/py-vgdl
 */
public class Agent extends AbstractPlayer {

    /**
     * Random generator for the agent.
     */
    protected Random randomGenerator;

    /**
     * Observation grid.
     */
    protected ArrayList<Observation> grid[][];

    /**
     * block size
     */
    protected int block_size;


    protected Stack<Node> target_node= new Stack<Node>();
    //【深搜中操作】最终存放从根节点到叶节点的动作们（回溯的时候加入）
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
        grid = so.getObservationGrid();
        block_size = so.getBlockSize();
    }

    /**
     * Picks an action. This function is called every game step to request an action
     * from the player.
     *
     *
     * @return An action for the current state
     */

    //BUG所在！！！函数或者这个集合有问题
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

/*
Bug
父类是一个抽象类，里边有抽象方法，当子类继承父类时，需要使用该该抽象方法[参数什么的都不能改变！]
 */
    public Types.ACTIONS act(StateObservation stateObs, ElapsedCpuTimer elapsedTimer) {
    //这个函数会被不断重复调用，而深度优先搜索其实只搜索一遍，可以得到所有的步骤，所以这个函数后面的部分只需要执行一次
        if(!sort_actions.empty())
            return sort_actions.pop();

        //开始深搜，注意目标检测的时机（在要被being_visit的栈往外边拿的时候进行检测）
        while(true){
            if(first_time){//第一次进入，栈中什么都没有
                Node root = new Node();
                root.Node_state=stateObs.copy();
                root.Node_father=null;
                root.Node_action=null;
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
                if(current_father.Node_state.isGameOver()){//目标检测,结束了
                    if (current_father.Node_state.getGameWinner()==Types.WINNER.PLAYER_WINS){
                        //当前结束，而且是玩家获胜
                        target_node.push(current_father.clone());
                        break;//【唯一出循环的方式，找到了最终目标！】找到了最终目标
                    }
                        //当前结束，而且不是玩家获胜，即输了捏！！
                        //直接进入下一次循环即可，(因为当前节点已经被being_visit给pop掉啦！)

                }

                else{//不是目标，游戏没有结束，要扩展当前节点

                    //task1：对target_node进行管理
                    //  BUG：比较相等的时候只能比较当前状态的呀，直接比较两个对象肯定不一样呢！
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
                    boolean newstate=true;//判断是不是之前没有出现过的状态
                    newstate = is_difference_and_save(current_father.Node_state);
                    //判断当前节点可不可以扩展-没有出现过的状态而且当前没有结束
                    //只在这个节点作为父亲节点的时候才进行重复状态检查，产生的子节点不进行检查
                    if(newstate){
                        //没有出现过的状态，而且当前没输！可以扩展current_father
                        ArrayList<Types.ACTIONS> actions = stateObs.getAvailableActions();
                        //所有当前状态可以操作的节点
                        for(Types.ACTIONS possible_action : actions)
                        //把当前所有可以走的步骤，以节点的形式呈现下一步的状态
                        {
                                Node node = new Node();
                                node.Node_father = current_father.clone();
                                node.Node_action = possible_action;
                                StateObservation state_advance=current_father.Node_state.copy();//当前父节点的状态
                                state_advance.advance(possible_action);
                                node.Node_state = state_advance.copy();//【当前状态的第二个副本，给到子节点】
                                //BUG所在点！！！现在删掉了子节点和已有状态的比较
                                //把没有进行过goal test而且也不和之前状态相同的子节点加入到栈当中
                                being_visit.push(node.clone());
                        }
                    }
                }
            }

        }
        //深搜完成啦，此时找到了最终赢的状态，从根节点走到当前节点的
        //拿到的target_actions栈顶元素是叶节点产生的方法
        while(!target_node.empty())//把所有的节点的状态都给到了sort_actions里边呢
            sort_actions.push((target_node.pop().Node_action));


        //按照从根节点到叶节点动作顺序排，此时栈顶是根节点的动作

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
            for (int i = 0; i < positions.length; i++) {
                System.out.print(positions[i].size() + ",");
            }
            System.out.print("); ");
        }else System.out.print(str + ": 0; ");
    }



    /**
     * Gets the player the control to draw something on the screen.
     * It can be used for debug purposes.
     * @param g Graphics device to draw to.
     */
//这个draw，使不使用sampleRandom中的实现都没有影响
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
