#include <iostream>
#include <unordered_map>
//#include <vector>
using namespace std;


/*
补充：C++中结构体的构造函数！

struct node{
    int data;
    string str;
    char x;
    // 自定义构造函数
    void init(int a, string b, char c){
        this->data = a;
        this->str = b;
        this->x = c;
    }
    // 无参数构造函数, 这里顺序随意, 初始化时须以定义顺序初始化, 建议这里也以定义顺序书写
    node(): data(), str(), x(){}
    // 有参数构造函数
    // 在建立结构体数组时, 【如果只写带参数的构造函数将会出现数组无法初始化的错误】, 须先写无参数构造函数
    node(int a, string b, char c) :data(a), str(b), x(c){}
};

*/
/*
input
5
2 5 1 4 3 
4 5 2 1 3

output
-1 -1
-1 -1
-1 -1
5 3
2 1

*/

//vector<int> preorder;
//vector<int> inorder;


/*
以下可能会触发segmentation fault的情况（本例子中）

1、指针没有初始化（不会自动给成NULL的）
2、堆溢出（使用new或者malloc的时候）

char *p=(char *)malloc(sizeof(char)*10);
char *q=strcpy(p,"This is an example of a heap error");
分配的堆空间为 10 个 byte。多出来的字符被放置在 10 之后的内存中。一不小心发生
了越界。才出现了这个堆被破坏的错误。

3、栈溢出（函数调用之中发生溢出，修改了函数的返回地址）

栈越界破坏的都是相邻的数据块，栈越界
通常修改当前函数返回地址，参数或者局部变量，如果返回地址被修改可能会产生指令错误或者执行非预期的代码


*/





int capacity;
int *preorder=NULL;
int *inorder=NULL;
unordered_map<int, int> dic;

struct TreeNode {       //链表来创建树形结构
      int value;
      TreeNode *left=NULL;
      TreeNode *right=NULL;
      //TreeNode(int x) : value(x){} //构造函数,把val赋值成当前位置的数字。把left和right都赋值成NULL啦！, left(NULL), right(NULL)
 };




TreeNode* construct(int index, int left, int right) { 
    if(left > right) {                                      //  递归结束，已经越过叶子结点.
        return NULL; 
    }                       
    TreeNode* node = new TreeNode();          // 建立根节点preorder[index]
    node ->value=preorder[index];
    // 获取当前结点在中序的index
    int i = dic[preorder[index]];          
        // index：是根节点在前序遍历的位置就是完整遍历前序搜索的vector呢！
        // left：在中序遍历中截断的左界
        // right:同上
        // 递归左子树
        node->left = construct(index + 1, left, i - 1);             
        // 递归右子树
        node->right = construct(index + i - left + 1, i + 1, right);
        return node;                                           
    }

TreeNode* buildTree() {
        // 利用hashMap映射索引，可以在每一次取的时候时间复杂度为o（1）
        //【创建这个新的】
    for(int i = 0; i < capacity; i++) {
         dic[inorder[i]] = i;
    }

    return construct(0, 0, capacity - 1);//第一次调用这个函数就可以啦！每次递归划定【中序】的范围
}


/*

    TreeNode* Inorder_traversal(TreeNode*local_root,int target){
        if(local_root!=NULL){
            if(local_root->value==target)
                return local_root;
            else{
                TreeNode * temp1 =Inorder_traversal(local_root->left,target);
                if(temp1!=NULL)
                    return temp1;
                TreeNode * temp2 = Inorder_traversal(local_root->right,target);
                return temp2;
            }
        }
        return NULL;
    }
*/
    void Inorder_traversal(TreeNode *root,int answer_left[],int answer_right[]){
        if(root!=NULL){
            if(root->left!=NULL)
                answer_left[root->value-1]=root->left->value;
            else
                answer_left[root->value-1]=-1;

            if(root->right!=NULL)
                answer_right[root->value-1]=root->right->value;
            else
                answer_right[root->value-1]=-1;
            Inorder_traversal(root->left,answer_left,answer_right);
            Inorder_traversal(root->right,answer_left,answer_right);
            }
        }



int main()
{
    int n;
    cin >> n;//总节点个数
    capacity=n;
    int a[n],b[n];
    inorder=a;
    preorder=b;
    for(int i=0;i<n;i++)//对中序的顺序进行存储
        cin >> a[i];
    for(int i=0;i<n;i++)//对前序的顺序进行存储
        cin >> b[i];

    TreeNode* whole_root = buildTree();//直接返回了完整的树的全部样子！

    /*
    for(int i=1;i<=n;i++){//现在的复杂度是n平方
        TreeNode* temp = Inorder_traversal(whole_root);//一定是可以找到的呢
        if(temp->left!=NULL)
            cout << temp->left->value;
        else
            cout << -1;
        cout << ' ';
        if(temp->right!=NULL)
            cout << temp->right->value;
        else
            cout << -1;
        cout << endl;
    }
*/


    //想法：能不能不使用中序遍历，直接用一个一阶循环，把每一个value的存储在不同的下标位置呢
    int answer_left[n];//存储当前元素值是i的左孩子的value
    int answer_right[n];//存储当前元素值是i的右孩子的value
    Inorder_traversal(whole_root,answer_left,answer_right);
/*BUG!中序遍历没有以高效的方式运行！！！*/
    for(int i=0;i<n;i++){
        cout <<answer_left[i];
        cout << ' ';
        cout << answer_right[i];
        cout <<endl;
    }
}