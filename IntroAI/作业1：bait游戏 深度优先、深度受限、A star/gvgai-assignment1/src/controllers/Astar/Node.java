package controllers.Astar;

import core.game.StateObservation;
import ontology.Types;

public class Node implements Cloneable,Comparable {
    public StateObservation Node_state;//当前节点状态
    public Types.ACTIONS Node_action;//父节点-》子节点的动作
    public Node Node_father;//父节点
    public int depth;//深度
    public double priority;
    public double previous_cost;
    public Node clone(){
        Node newone = null;
        try{
            newone = (Node) super.clone();//和直接用等号连接并不相同，此时调用这个方法可以直接克隆一个对象！
        }catch(CloneNotSupportedException e){
            e.printStackTrace();
        }
        return newone;
    }
//让每次PriorityQueue返回的元素都是priority的最小值（走到当前步的开销！）
    @Override
    public int compareTo(Object o) {//实现优先队列的Comparable，他的函数必须返回int类型！
        Node o1 = (Node)o;
        return (int)(this.priority - o1.priority);
    }
}