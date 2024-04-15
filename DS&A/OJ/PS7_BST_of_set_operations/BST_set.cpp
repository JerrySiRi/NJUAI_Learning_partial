#include <iostream>
#include <cassert>
using namespace std;



/*
【重新理解C++中的new！】
---在 C++ 中，通过 new 运算符来实现动态内存分配。new开辟的空间在堆上。
---当在局部函数中new出一段新的空间，该段空间在局部函数调用结束后仍然能够使用，可以用来向主函数传递参数。
new的使用格式，new出来的是一段空间的首地址。【所以一般需要用指针来存放这段地址。】

********所以new出来的是一个内存空间，这个内存空间中放了某种类型（通过这种类型确定空间的大小），new出来的不是一个变量




new 的作用是开辟一片新的内存，并返回内存的起始地址
此为最常用的用法   new 表达式
比如要创建一个整数空间，可以这样定义

1 new int;                     //开辟一个存放整数的存储空间，没有设定值
2 new int(INT_MAX);            //设定初值为INT_MAX
3 new int[5];                  //开辟一个存放数组的空间
4 int *a = new int[5];         //开辟空间+返回首址给a
new运算符使用的一般格式为 　　new 类型 [初值] 　　
用new分配数组空间时不能指定初值。如果由于内存不足等原因而无法正常分配空间，则new会返回一个空指针NULL，用户可以根据该指针的值判断分配空间是否成功。

********如果想在new的过程中同时赋予初值。只能用对应的构造函数啦！！！如上面例子中的int(INT_MAX)
********以及本例子之中的new TreeNode(num);【完成创建内存空间+赋予初始值--两种操作合一啦！！！】
*/

int lans;
int Q,P;


struct TreeNode {//链表来创建树形结构
      int val;
      int count=1;
      TreeNode *left;
      TreeNode *right;
      TreeNode *parent;
      TreeNode(int x) : val(x), left(NULL), right(NULL),parent(NULL){} //构造函数,把val赋值成当前位置的数字。把left和right都赋值成NULL啦！
 };

int test(TreeNode*node){
      assert(node!=NULL);
      return 1;
}

TreeNode * tree_search(TreeNode* root,int value){//修改版的tree_search
//【出来还需要再判断一下是相同的出来 or 遍历到最后要插入的地方啦】
      TreeNode * previous=NULL;
      while(root!=NULL && root->val!=value){//【保证了root！=NULL】
            if(root->val < value)
                  {previous=root; root=root->right;}
            else if(root->val > value)
                  {previous=root; root=root->left;}
            else
                  return root;//找到了重复的节点        
      }
      if(root!=NULL && root->val==value)
            return root;
      return previous;//找到了要插入的地方,此时遍历了之后没有找到相同value的节点，root是空的 
      //此时previous也可能是NULL！！！
}


//【BUG！】一定要返回root呢，在函数里边仍然是局部变量出不去！【最保险的做法！！！】
TreeNode* add_multi(TreeNode *root,int new_num){
      if(root == NULL) {//空的树
            //TreeNode temp1 = TreeNode(1);
            TreeNode *temp  =new TreeNode((lans+new_num)%P);
            root = temp;
      }
      else{
            //树不是空的root！= NULL
            int num=(lans+new_num)%P;
            TreeNode *cur_add = tree_search(root,num);
            if(cur_add == NULL)//root!=NULL previous=NULL,[此时树是空的！！！]
                  {
                        TreeNode *temp  = new TreeNode((lans+new_num)%P);
                        root=temp;
                        return root;
                  }
            
            if(test(cur_add) && cur_add->val == num)//此时cur_add != NULL , 加入了重复元素
                   cur_add->count++;
            else{//要加入新的元素
                  if(test(cur_add) && num < cur_add->val)
                        {cur_add->left = new TreeNode(num);cur_add->left->parent=cur_add;}
                  else
                        {cur_add->right = new TreeNode(num);cur_add->right->parent=cur_add->right;}
                  }
            }
      return root;
}


TreeNode *successor(TreeNode *root,TreeNode*cur_add){//找到后继节点
      TreeNode* cur_add_p = cur_add->parent;
      if(test(cur_add) && cur_add->right!=NULL){//右子树存在，找到右子树中的最左侧
            cur_add=cur_add->right;
            while(cur_add!=NULL)
                  cur_add=cur_add->left;
            return cur_add;
      }
      else{//右子树不存在，就要上去来找
            while(  test(cur_add_p) && cur_add_p != NULL && cur_add == cur_add_p ->right){
                  cur_add = cur_add_p;
                  cur_add_p = cur_add_p->parent;
            }
      }
      return cur_add_p;
}

TreeNode* transplant(TreeNode*root,TreeNode*u,TreeNode* v){//以一颗以v为根的子树来替换根为u的子树，并成为其双亲的孩子节点
      if(u==NULL)
            return root;
      if(u->parent==NULL)
            root=v;
            //【此时u可能是空的呢！】u!=NULL  && u->parent->left!=NULL &&
      else if(u == u->parent->left)//u是一个左节点--目标，找到v的新父节点来给父节点的left或者right修改！
            u->parent->left=v;
      else
            u->parent->right=v;

      if(v!=NULL)
            v->parent=u->parent;
      return root;
            
}

/*
TreeNode* tree_delete(TreeNode*root,TreeNode*cur_add){//删除cur_add的节点
      if (cur_add == NULL || root == NULL) {
        return root;
      }

      if (root == cur_add && root->right == NULL) {
        // 一、删除的是根节点，并且根节点没有右子树
        // 处理：切断targetPtr与左子树的关联，返回左子树，释放targetPtr
        root = root->left;
        if (root != NULL) {
            root->parent = NULL;
        }
        cur_add->left = NULL;
        return root;
    }

      if(cur_add->left==NULL)//situation1:没有左孩子，或者两个孩子都没有（直接拿NULL替换就好啦）
            root=transplant(root,cur_add,cur_add->right);
      else if (cur_add->right==NULL)//situation2：没有右孩子,一定有左孩子
            root=transplant(root,cur_add,cur_add->left);
      else{//situation3:有两个孩子
            TreeNode* suc = successor(root,cur_add);//当前节点cur_add的后继！
            if(suc->parent!=cur_add){//situation3.2:cur_add的后继不是它的右孩子
                  root=transplant(root,suc,suc->right);
                  suc->right=cur_add->right;
                  suc->right->parent=suc;
            }
            root=transplant(root,cur_add,suc);
            //situation3.2+3.1的后续操作:cur_add的后继是他的右孩子【则这个右孩子一定没有左孩子】
            suc->left=cur_add->left;
            suc->left->parent=suc;
      }
      return root;
}

*/



// 在二叉搜索树中插入value，如果二叉树中已经存在则不进行插入（简化处理逻辑）
TreeNode *tree_delete(TreeNode *root, TreeNode *targetPtr) {
    if (targetPtr == NULL || root == NULL) {
        return root;
    }
    if (root == targetPtr && root->right == NULL) {
        // 一、删除的是根节点，并且根节点没有右子树
        // 处理：切断targetPtr与左子树的关联，返回左子树，释放targetPtr
        root = root->left;
        if (root != NULL) {
            root->parent = NULL;
        }
        targetPtr->left = NULL;
    }
    else if (targetPtr->left == targetPtr->right) {
        // 二、删除的叶节点
        // targetPtr->left == targetPtr->right,只能是同时为NULL
        // 操作：切断parent与targetPtr的关联，返回root，释放targetPtr
        if (targetPtr->parent->left == targetPtr) {
            targetPtr->parent->left = NULL;
        } else {
            targetPtr->parent->right = NULL;
        }
        // 切断targetPtr 与targetPtr->parent的关联
        targetPtr->parent = NULL;
    }     
    else if (targetPtr->right == NULL) {
        // 三、删除节点右子树为空      需要找到远祖父节点【即后继】
        TreeNode *pParent = targetPtr;
        // 祖父节点B，并且使得节点targetPtr在远祖父节点B的左子树
        while (pParent->parent != NULL && pParent->parent->right == pParent) {
            pParent = pParent->parent;
        }
        if (pParent->parent == NULL) {
            // 如果targetPtr不存在一个远祖父节点B，使得leftPtr在远祖父B的左子树
            // 操作：只能删除这个节点，并且把左子树放到当前节点的位置
            targetPtr->parent->right = targetPtr->left;
            targetPtr->left->parent = targetPtr->parent;
            // 切断targetPtr与parent、left的关系
            targetPtr->parent = NULL;
            targetPtr->left = NULL;
        }
        else {
            // 如果targetPtr存在一个远祖父节点pParent，B就是targetPtr的后继
            // 否则pParent->parent->value替换targetPtr->value，再删除pParent->parent（递归）

            if(pParent->parent!=targetPtr){//situation3.2:cur_add的后继不是它的右孩子
                  root=transplant(root,pParent,pParent->right);
                  pParent->right=targetPtr->right;
                  pParent->right->parent=pParent;
            }
            root=transplant(root,targetPtr,pParent);
            //situation3.2+3.1的后续操作:cur_add的后继是他的右孩子【则这个右孩子一定没有左孩子】
            pParent->left=targetPtr->left;
            pParent->left->parent=pParent;
        }
    }





    else {
        // 四、删除节点存在右子树，直接在右子树寻找中序遍历的第一个节点
        TreeNode * leftPtr = targetPtr->right;
        // 一直往left寻找
        while (leftPtr->left != NULL) {
            leftPtr = leftPtr->left;
        }
        // 将leftPtr->value替换到targetPtr->value
        targetPtr->val = leftPtr->val;
        // targetPtr->right就是leftPtr
        if (targetPtr->right == leftPtr) {
            // 将targetPtr->right指向leftPtr右子树
            targetPtr->right = leftPtr->right;
            // 如果targetPtr->right ！= NULL，还需要设置parent
            if (leftPtr->right != NULL) {
                leftPtr->right->parent = targetPtr;
            }
        }
        else {
            // 否则leftPtr->parent与leftPtr切断关系
            leftPtr->parent->left = NULL;
        }
        // 将leftPtr于其parent切断关系并释放
        leftPtr->parent = NULL;
    }
    return root;
}





int count_quan(TreeNode*root,int L,int R){//递归来求解啦！
      if(root==NULL)
            return 0;
      if(root->val>L && root->val<R)
            return (root->count)*(root->val)+count_quan(root->left,L,R)+count_quan(root->right,L,R);
      else if(root->val <= L)
            return count_quan(root->right,L,R);
      else if(root->val == R)
            return (root->count)*(root->val)+count_quan(root->left,L,R);
      else 
            return count_quan(root->left,L,R);
}

int main()
{
      lans=0;
      int temp_q,temp_p;
      cin >> temp_q >> temp_p;//输入的操作个数和mod P
      Q=temp_q;P=temp_p;
      TreeNode *root = NULL;//一开始的根节点
       for(int i=0 ; i<Q ; i++){
            int cur_op;
            cin >> cur_op;//选当前的操作是什么
            if(cur_op==0){
                  int new_num;
                  cin >> new_num;
                  root=add_multi(root,new_num);
            }
            else if(cur_op==1){//有删除的情况！所以小心如果当前树没有了会怎样！
                  int new_num;
                  cin >> new_num;
                  int t_num=(lans+new_num)%P;
                  TreeNode *cur_add=tree_search(root,t_num);
                  //两种情况，可能是真的有，可能是没有

                  //[BUG！可能previous是一个NULL！]
                  if(cur_add == NULL  )//当前树是空的！【可能有问题！！！】
                        cout << 0 << endl;
                  else if(cur_add->val!=t_num)//没有这个节点
                        cout << 0 << endl;
                  else{//真的有！
                        cout << cur_add->count << endl;
                        if(cur_add->count >= 2)
                              cur_add->count--;
                        else if(cur_add->count == 1)//只有一个节点，就需要删除啦！
                              root=tree_delete(root,cur_add);//传入的是当前节点的指针呢！
                  }
                        
            }
            else if(cur_op==2){
                  int L,R;
                  cin >> L >> R;
                  L=(lans+L)%P;
                  R=(lans+R)%P;
                  if( ((L<R)?L:R) != L){//此时两者需要交换一下,R现在是最小值
                        int temp=L;
                        L=R;
                        R=temp;
                  }
                  int sum=count_quan(root,L,R);//总和啦
                  lans=sum;
                  cout << sum << endl;
            }
      }
}
/*
测试
6 10
0 3
0 3
0 5
0 1
1 3
2 0 8


4 9
0 3
1 3
0 6
2 0 7


2 9
0 3
1 3



9 30
0 5
0 5
1 5
2 0 3
2 4 5
0 3
1 3
1 3
1 3




*/








