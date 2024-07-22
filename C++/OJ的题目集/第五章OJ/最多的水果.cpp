#include <iostream>
#include <cstring>
using namespace std;
/*  
题目：最多的水果（用链表实现）
题目描述：
每个果农拥有若干块*大小相同的地，每块地都种了水果。请从中找出种植最多的那种水果。**

输入：
输入多个果农的种植情况，以0作为最终的结束。【输出结束*】 
每个果农若干行，第一行为耕地数目n，后续n行分别为每块地种植的水果。

输出：
最多的水果是什么(数量相等情况下，输出先出现的水果,之后再输出一样多得水果)【循环的选择啦*】 

样例输入：
5
peach
apple
banana
apple
apple
3
pear
orange
pear
1
pear
0

样例输出：
apple
pear
*/
struct Node
{
	char ch[20];
	Node *next;	
};

/*
提升和教训：
①while或者for的循环条件算在整个循环体中的 
但是下一次再进行条件判断的时候是下一次循环了
while(n!=0)
{
	int n
	cin >> n;
} 
这样的n始终只能在上一次循环体中存在，不能在下一次循环的开始进行条件的判断**
【轻易不重载！！！】

【修改：直接cin >>n也是可以改变int n的值***（杰哥代码就是这样的）】

②计数器，累加器  都必须要赋给他初值的***
int count =0;
int sum=0; 

③考虑问题要考虑清楚***》》一般都会有特殊情况的***
【如果传进来的是一个NULL呢***（计算当前节点有多少个重复元素***）】 

④一般if后面都接直接的操作的 (尽量不使用if;+else的情况（可读性差）)
【if(strcmp(a,b)==0)
	count++;】 
	
⑤什么东西应该放在循环里边，什么东西不应该放在循环里边 
【自己写完自己脑子里边过一下两次循环的情况呀！】
head \max\max1都是放在外边的呢** 
*/ 
extern Node *input(int n,Node *&head);
extern int what (Node *s,Node *head);
extern void fruit(Node *head);

int main() 
{
	int n;
	cin >> n;
	Node *head=NULL;//得在外面定义head，之后每次会修改head的值（有可能不修改呢） 
	for(;n!=0;cin >> n) 
	{
		head=input(n,head);
	}
	fruit(head);
	return 0;
}

//step1:输入函数（计算输入的个数的）
//传进来输入几个+头指针（之后要在这个上面进行操作的，而且需要用引用**在头指针后面插入捏） 
Node *input(int n,Node *&head)//要往这个指针里边加入n个元素* 
{
	for(int i=0;i<n;i++)
	{
		char ch[20];//要用strcpy来进行字符串的赋值的捏 
		cin >> ch;//每次这个ch都需要重载的**重新输入
		Node *p=new Node;
		if(head==NULL)
		{
			strcpy(p->ch,ch);
			p->next=NULL;
			head=p;
		} 
		else
		{
			strcpy(p->ch,ch);
			p->next=head;
			head=p;
		}
	}
	return head;
}


int what (Node *s,Node *head)//计算每一个节点有多少个和他重复的 
//如果只把s这个指针传进来，那只能知道s之后的节点是什么，不知道前面的呀 
{
	int count=0;
	char a[20];
	if(s==NULL)
	{
		return 0;
	}
	strcpy(a,s->ch);
	for(Node *p=head;p!=NULL;p=p->next)
	{
		if(strcmp(a,p->ch)==0) 
			count++;//相同返回0 ，加一个！就进if语句了 
	}
	return count;
}


void fruit(Node *head)
{
	int max=0;
	char max1[20];	
	Node *s;
	Node *p=head;
//Q5:
	max=what(p,head);
	strcpy(max1,p->ch);
	
	for(;p!=NULL;p=s)//p变到哪要由链表里的水果具体是谁来决定的 
	{
		
		for(s=p->next;s!=NULL;s=s->next)
			if(strcmp(s->ch,p->ch)) break;
			//现在s就是下一个需要计数的位点啦* 
		int a;
		a=what(s,head); 
		if(max<a) 
		{
			strcpy(max1,s->ch);
			max=a;
		}
	}
	p=head;
	if (what(p,head)==max) cout<<p->ch;
	for(;p!=NULL;p=s)//p变到哪要由链表里的水果具体是谁来决定的 
	{
		
		for(s=p->next;s!=NULL;s=s->next)
		{
			if(strcmp(s->ch,p->ch)) break;
		}//现在s就是下一个需要计数的位点啦* 
				
		if (what(s,head)==max) cout<<s->ch;
	}
}

