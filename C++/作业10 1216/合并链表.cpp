#include<iostream>
using namespace std;
/*
题目描述【合并链表】
给定2个单向链表L1，L2，其中链表的长度分别是n1，n2。
每个链表中的数据已经按照从小到大排列好，**   
现在要求将两个链表进行合并，并保证合并后的链表中的数据仍然保持从小到大排列***。
输入格式:	
第一行：n1 n2。1≤n1≤10000，1≤n2≤10000
第二行：n1个非负整数，用空格隔开
第三行：n2个非负整数，用空格隔开
输出格式
合并后的链表数据，用空格隔开。
样例数据
input
3 5****输入的是从小到大
3 7 11
2 8 9 12 16
output
2 3 7 8 9 11 12 16

题目思路：
①输入数字，输入链表中的节点数据（可以用函数Node *input(int a)）
        因为本题不以-1结束，所以要用while循环来看链表的个数的
②在其中一个链表中进行插入，比较节点内容的大小**（注意要使用二级链表**可能对head进行操作的）
""

错误：

①在把其中一个链表的数据进行变动的时候一定要【再定义一个动态变量，别动指向原来那个
							链表的指针，这样能显著降低指针乱指的可能性！】 
②尾指针还不是太熟呀！老对尾指针的操作出现失误***
				赋值+加入新的元素+位置的变更、一个都不能少*** 
*/

struct Node
{
    int content;
    Node *next;
};

extern Node*input(int a);
extern void insert(Node *&head1,Node *head2);
extern void output(Node *head1);
int main()
{
    int a,b;
    cin >> a >> b;
    Node *head1=input(a);
    Node *head2=input(b);
    insert(head1,head2);
    output(head1);
    return 0;
}


Node *input(int a)//不同的题目一定要通过不同的方式进行链表节点输入
//本题是要从小到大输入链表的，所以一定采取尾部输入*** 
{
    int i,x;
    Node *head=NULL;//创建头指针，初始化为NULL。一定要放在循环的外边的***不能重载
    Node *tail=NULL;
    //要对输入的第一个元素也进行判断的**万一a==0呢。先判断再输入**
    for(i=0;i<a;i++)
    {
        cin >>x;
        Node *p=new Node;//创建动态变量加入链表中，作为节点。一定放在循环中，每次重载，加入新节点
        p->content=x;//怎么老忘记赋值呀！！！ 
        if(head==NULL)
        {
        	p->next=NULL;//相比较书中的操作，咱们把初始化的操作放在了if里边了** 
        	head=p;
        	tail=p;
        	
        	
        }
        else
        {
            p->next=NULL;
            tail->next=p;
            tail=p;
        }
    }
    return head;
}

//在head1链表的基础上进行操作，要对head1进行二级指针或者引用***的使用
void insert(Node *&head1,Node *head2)
{
    Node *p,*q,*q1;
    Node *a=head1;
    while(a->next!=NULL)
   		a=a->next;//每次得重新寻找尾指针的位置
    //for(a=head1;a!=NULL;a=a->next)//a是尾指针【有一种情况是从最后插入的】 
    //{
       // ;
   // }
    for(p=head2;p!=NULL;p=p->next)
    {
    	Node *b=new Node;
    	b->content=p->content;
        for(q=head1;q->next!=NULL;q=q->next)//循环到倒数第二个
        {
            q1=q->next;
            if(b->content>=q->content && b->content <=q1->content)//不在头指针和尾指针的位置
            {
                b->next=q1;
                q->next=b;
                break;
            }
            else if(b->content<=head1->content)//在头指针位置插入
            {
                b->next=head1;
                head1=b;
                break;
        	} 
            if(b->content>=a->content) //只剩下在尾指针后面插入啦*
            {
                b->next=NULL;
                a->next=b; 
                a=b;
                break;
            }
        }
    }
}


void output(Node*head1)
{
    Node *p;
    for(p=head1;p!=NULL;p=p->next)
    {
        cout << p->content << " "; 
    }
}

