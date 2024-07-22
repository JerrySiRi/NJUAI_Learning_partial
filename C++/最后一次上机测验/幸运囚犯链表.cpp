#include <iostream>
using namespace std;
/*
step1:
先完成输入吧 
 */
struct Node
{
	bool is;
	char name[10];
	Node *next;	
};
int main() 
{
	int num,hao;
	cin >> num >> hao;
	//num是有num个人，hao是报到hao就出去，给成false
	//step1:建立链表，一共num个人**,头尾相连哦**
	//注意输入的顺序，题目要求是顺时针+按照输入顺序报数的》》只能尾指针输入啦,保证顺序 
	//最后一个元素是新输入的那个，让他不断指向头指针就可以啦
	Node *head=NULL;
	Node *tail=NULL;//不断定位最后一个元素 
	for(int i=0;i<num;i++)
	{
		if(head==NULL)//一个都没有 
		{
			Node *s=new Node;
			cin >> s->name;
			head=s;
			tail=s;
			s->next=head;//首尾相连 
		}
		else
		{
			Node *s=new Node;
			cin >> s->name;
			tail->next=s;
			s->next=head;
			tail=s;
		}
	}
	//完成输入啦，是一个环形，顺序正确 
	Node *p=head; 
	for(int i=0;i<num;i++)
	{
		p->is=true;
		p=p->next;
	}
	
	//开始报数
	int last=num;
	Node *q=head;
	while(last>1)
	{
		int count=0;//count到hao了就出去啦 
		while(count<=hao)//【错误1】while后面的括号，如果满足这个括号才进这个循环的***否则不进
		//括号的意义是满足者进来，不满足者出去*** 
		{
			if(q->is==true)//在圈子里边 
			{
				count++;
				if(count==hao)
					goto L;//【错误：时刻小心循环的情况，这种情况是先count++再往后移一位。
					//但实际上应该是报到这个数字之后就不应该往后啦，必须出来了。在草稿纸上多多验算一下呀！！！】
				q=q->next;
			}
			else
				q=q->next;
		}
		L:
		//现在q指的就是即将出来的人啦
		q->is=false; //不在圈子里边啦 
		last--;
	}		 
	Node *w=head;
	for(int i=0;i<num;i++)
	{
		if(w->is==true)
		{
			cout << w->name;
			break;
		}
		else
			w=w->next;
	}

	return 0;
}
