#include <iostream>
#include <vector>
#include <unordered_map>
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
struct TreeNode {//链表来创建树形结构
      int val;
      TreeNode *left;
      TreeNode *right;
      TreeNode(int x) : val(x), left(NULL), right(NULL){} //构造函数,把val赋值成当前位置的数字。把left和right都赋值成NULL啦！
 };


    // 全局变量，方便在后续递归时使用。
    vector<int> preorder;
    vector<int> inorder;
    unordered_map<int, int> dic;
    int capacity;





    // 通过下面参数锁定遍历划分的范围，含义下面会讲。
    TreeNode* recur(int root, int left, int right) { 
        if(left > right) { //  已经越过叶子结点.
            return NULL; 
        }                       
        TreeNode* node = new TreeNode(preorder[root]);          // 建立根节点
        int i = dic[preorder[root]];                            // 获取当前结点在中序的index
        // 三个参数的含意
        // root：【是根节点在前序遍历的位置】对前序搜索的操作，就是完整遍历前序搜索的vector呢！
        // left：在中序遍历中左边界
        // 递归左子树时，左边界限是确定的，i - 1是右边界，因为i是中序的索引，他的左子树的右边界一定在他的上一位。
        node->left = recur(root + 1, left, i - 1);              // 开启左子树递归
        // 递归右子树时，右边界确定，i + 1是左边界，理由同上，这里的root计算实际就是在前序中加上左子树的长度加一找到右子树根结点。
        node->right = recur(root + i - left + 1, i + 1, right); // 开启右子树递归
        return node;                                            // 回溯返回根节点
    }

    TreeNode* buildTree() {
        // 利用hashMap映射索引，可以在每一次取的时候时间复杂度为o（1）
        //【创建这个新的】
        for(int i = 0; i < capacity; i++) {
             dic[inorder[i]] = i;
        }
        return recur(0, 0, capacity - 1);//第一次调用这个函数就可以啦！每次递归划定【中序】的范围
    }

    TreeNode* Inorder_traversal(TreeNode*local_root,int target){
        if(local_root!=NULL){
            if(local_root->val==target)
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




int main()
{
    int n;
    cin >> n;//总节点个数
    capacity=n;
    for(int i=0;i<n;i++){//对中序的顺序进行存储
        int temp;
        cin >> temp;
        inorder.push_back(temp);
    }
    for(int i=0;i<n;i++){//对前序的顺序进行存储
        int temp;
        cin >> temp;
        preorder.push_back(temp);
    }

    TreeNode* whole_root = buildTree();//直接返回了完整的树的全部样子！

    for(int i=1;i<=n;i++){
        TreeNode*temp = Inorder_traversal(whole_root,i);//一定是可以找到的呢
        if(temp->left!=NULL)
            cout << temp->left->val;
        else
            cout << -1;
        cout << ' ';
        if(temp->right!=NULL)
            cout << temp->right->val;
        else
            cout << -1;
        cout << endl;
    }
}