package controllers.limitdepthfirst;

import core.game.StateObservation;
import ontology.Types;

//属性1：当前节点状态StateObservation
//属性2：父节点
//属性3：父节点是通过了什么action到的当前节点（相当于指针了）
//属性4：当前节点深度
//属性5：当前节点拿到了钥匙了没
public class Node  implements Cloneable{//
    public StateObservation Node_state;//当前节点状态
    public Types.ACTIONS Node_action;//父节点-》子节点的动作
    public Node Node_father;//父节点
    public int depth;//深度
    //public boolean whether_key;//拿没拿到钥匙
    public Node clone(){
        Node newone = null;
        try{
            newone = (Node)super.clone();//和直接用等号连接并不相同，此时调用这个方法可以直接克隆一个对象！
        }catch(CloneNotSupportedException e){
            e.printStackTrace();
        }
        return newone;
    }
}
