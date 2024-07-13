#include <iostream>
#include <cstring>
using namespace std;
/* 
题目：修课最多的学生

题目描述：

一个班50个学生，选修课外活动课。【50个人都得选一遍】 
输入若干课外活动课的选课学生名字（名字为英文，长度小于10个字符，没有重名）
输出修课最多的学生。输入说明：分若干行，输入选课名单，最后一行为"###"，表示输入结束。
输出说明：如果修课最多的有多名学生，则输出名字时按词典顺序，在一行中输出，名字之间用空格分隔。

Sample:
一共五种课程，每个课程有一些学生选 
input:

Abbet Ackerman Backs Cary Cora Diana Fair Gale Jennifer Nancy Nolan Paige Polly Ted Wade Walter Wolf York
Catharine Dan Finch Jack Napoleon Paige
Abraham Backs Charles Diana Forbes Jennifer Nathan Patti Wade Walter Wolf
Abraham Bacon Cora Eaton Forbes Jack Nancy Nolan Polly Tom
Abel Adam Calvin Cora Eaton Forbes Owen Peter Tanya Thomas Tony Walter York Zack
###

output:

Cora Forbes Walter
*/
/*
step1：先把链表建立起来，看看里边是谁选课是最多的
step2：看看这些人的字典排序是怎样的*** 
*/
struct Node
{
	char name[10];
	int count;//需要初始化成1,每找到一次都+1 
	Node *next;
	
};
int main() 
{
	//step1：建立链表
	Node *head=NULL;
	char ch[10];
	cin >> ch;
	while(strcmp(ch,"###")!=0)//输入的不是###才进循环的*** 
	{
		if(head==NULL)
		{
			Node *p=new Node;
			strcpy(p->name,ch);
			p->next=NULL;
			head=p;
		}
		else//里边有一些节点了，先看看新输入的这一个里边有没有重复的 
		{
			Node *s;
			for(s=head;s!=NULL;s=s->next)
			{
				if(strcmp(ch,s->name)==0)
						break;//如果里边有重复的，s指向这个重复的节点。 
			}
			if(s!=NULL)//有重复的
				s->count=s->count+1;
			else//没有重复的 ，加入新节点** 
			{
				Node *p=new Node;
				strcpy(p->name,ch);
				p->next=head;
				head=p;
			} 
		}
		cin >> ch;
	}
	//全部输入完成 
	Node *s;
	int max=head->count;
	for(s=head;s!=NULL;s=s->next)
	{
		if(s->count>max)
			max=s->count;
	}
	//现在max就是修课最多的门数了，没有问题！
	//strcmp如果第一个字符串小于第二个字符串，返回<0***
//【想法一：把所有是max的人都存起来，按照大小从小到大输出】 
	typedef char A[10];
	A a[50];//a[50]是有50个元素，每个元素都是10个字符串大小 
	int i=0;
	for(Node *p=head;p!=NULL;p=p->next)
	{
		if(p->count==max)
		{
			strcpy(a[i],p->name);
			i++;//所有人的修课最多人的名字都存在这个数组里边了*** 
		}
	} 
//数组是大小为i的呢
		char min[10];
		strcpy(min,a[0]);
		bool all=true;
		while(all)
		{
			for(int j=0;j<i;j++)
			{	
				if(strcmp(a[j],min)<0)
					strcpy(min,a[j]);
			}
			//找到最小的那个的下标***
			int j;
			for(j=0;j<i;j++)
				if(strcmp(a[j],min)==0) break; 
			cout << min<<' ';
			strcpy(a[j],"ZZZZZZZZZ");
			strcpy(min,"ZZZZZZZ"); 
			int s1;
			for(s1=0;s1<i;s1++)
				if(strcmp(a[s1],"ZZZZZZZZZ")!=0) break;
			if(s1==i)
				 all=false;
		}
	return 0;
}
//【想法二：善用链表。善用排序。善用交换位置】最优解***** 
/*
优势 
①按照字典序进行输出****的本质就是 “排序”【得找到最深层的思想】 
【要和之前做过的题目进行勾连，所有的新情景只是换汤不换药的*****】
【本质思想都是没变的****！！！！！！！】

排序有许多的方法：
1、数组冒泡、选择
2、链表啦。
【只学过这两种，拨开题目的外衣，看看它的内核到底是什么。本质上就是一个交换位置的呀！】 


②思路的顺承性
前面存储的时候都已经用链表了***
已经有指针指向这个目标节点了，为什么不好好利用呢

链表的作用：
①存储数据
②可以进行交换的，交换的同时可以修改数据*** 



	node *head2=NULL;
	for (q=head;q!=NULL;q=q->next)
	{
		node *pq=new node;
		strcpy(pq->ch,q->ch);
		if (q->count==max)
		{
			pq->next=head2;
			head2=pq;
		}
	}
	for (q=head2;q!=NULL;q=q->next)
		for (node *s=head2;s!=NULL;s=s->next)
		{
			if (strcmp(q->ch,s->ch)<0)
			{
				char jk[20];
				strcpy(jk,q->ch);
				strcpy(q->ch,s->ch);
				strcpy(s->ch,jk);
			}
		} 

*/



/*
想法三：删除节点

劣势：
删除节点需要知道这个是第几个节点，并且需要判断他是不是头结点或者其他
麻烦度很高！！！！！
》》一般可以删除节点的题目都可以用***新建立一个链表来实现的***
》》就别用删除节点了吧***（除非题目必须让你删除才能用呢***） 
 

 
*/

















/*
Node *q;
			Node *min;
			for(q=p->next;q!=NULL;q=q->next)//找到这里边最小的字典序的那个*** 
			{
			
				if(q->count==max)//看看他的字典序和q的大小* 
				{
					if(stecmp(p->name,q->name)<0)//p的字典序更小
						min=p;
					else
						min=q; 
				}
			}
			//现在最小的就是min啦**把min输出就好啦***
			//但是需要删除节点**
*/
