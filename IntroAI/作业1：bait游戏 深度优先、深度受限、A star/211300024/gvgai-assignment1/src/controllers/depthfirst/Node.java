package controllers.depthfirst;

/*
【因为要不断在agent的脑海中跑运行情况，所以需要不断多个不是引用（等号赋值）的副本！！！】
由于java中的传参是引用类型，所以会出现这样的结果，我们希望传递的是对象的一份拷贝
所以这里就用到了Object的clone()方法。
克隆的实现需要一下几步：
1、在派生类中覆盖基类的clone()方法，并声明为public。
2、在派生类的clone()方法中，调用super.clone()。
3、在派生类中实现Cloneable接口。
   Cloneable接口没有任何抽象的方法，这样的成为标识接口。
   实现这个接口，只是为了告诉编译器这个对象可以被克隆了。我们按照上面的步骤将上面的代码修改如下：

 */
/*
class Point implements Cloneable{
int x,y;
Point (int x,int y)
{
this.x = x;
this.y = y;
}
public Object clone()
{
    Point p = null;
    try
    {
        p = (Point)super.clone();
    }catch (Exception e)
    {
        e.printStackTrace();
    }
    return p;
}
}

 */

import core.game.StateObservation;
import ontology.Types;

//属性1：当前节点状态StateObservation
//属性2：父节点
//属性3：父节点是通过了什么action到的当前节点（相当于指针了）
public class Node implements Cloneable {
    public StateObservation Node_state;//当前节点状态
    public Types.ACTIONS Node_action;//父节点-》子节点的动作
    public controllers.depthfirst.Node Node_father;//父节点
    public controllers.depthfirst.Node clone(){
        Node newone = null;
        try{
            newone = (Node)super.clone();//和直接用等号连接并不相同，此时调用这个方法可以直接克隆一个对象！
        }catch(CloneNotSupportedException e){
            e.printStackTrace();
        }
        return newone;
    }
}








