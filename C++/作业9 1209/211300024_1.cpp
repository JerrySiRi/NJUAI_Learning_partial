#include <iostream>
using namespace std;
/*
编写一个程序：
1 首先建立两个集合（从键盘输入集合的元素，元素为整型,以-1结束）
2 然后计算这两个集合的  【交集】、 【并集】以及 【差集】
（集合1相对集合2的差集运算：去除集合1中属于集合2的元素）
3 最后输出计算结果。要求用链表实现集合的表示。
【从集合的输入（不确定大小）再到集合的运算【交、并、差】都需要用链表的】 

要求：
①不能一main到底。应该多多用main函数之外的函数。方便检查错误 
②集合中元素唯一，不会有重复元素的
 
 
具体思路：
①函数一：输入数据，建立链表（2个）
②交集： 1以一个链表为基础，检索第二个链表
		 2如果第二个有，加到第三个【交集链表之中】
③并集：在一个集合上面操作，如果第二个集合数字和第一个集合不一样，就加进来
》》》改变了其中一个链表的数值**
④差集：
 
*/


/*
错误总结：
①二级指针的问题：
[运用情况：改变指针所指的地址了【原来是指x，现在变成指y了！】√不是改变指针所指的值了！×]
[链表实际上也是由头指针所指的地址所确定的指针的！] 
而由头指针插入--head所指的对象不是原来的p了，而是新加入的new Node*【改变地址>二级指针*】 
	若由尾指针插入--只改变tail指针所指的值**不改变head所指向的地址的，就可以不用二级指针的*

二级指针
int *p=&x;
int **q=&p;
访问x：x\*p\**q
访问p：p\*q 
【定义】函数形参的时候是 void all(Node **head1,Node *head2)
【调用】函数实参的时候是 all(&head1,head2); 
函数声明的时候是extern void all(Node**head1,Node*head2);

②在错误输出的时候就应该注意*
situation1：输出随机值-越界一般都是没有给赋值的*【输出时间不同得到的值都不一样！】 
situation2：没有输出-没有指针指向他，指针乱指  
*/
struct Node
{
	int content;
	Node *next;
};
extern Node* input();
extern Node* same(Node*head1,Node*head2);//交集 返回head3（交集链表头指针），最后(统一output） 
extern void all(Node**head1,Node*head2);
extern void cha(Node*h1,Node*h2);
extern void output(Node*h); 
int main()
{
	cout << "请输入集合1（以-1结尾）"<<endl;
	Node *head1=input();
	cout << "请输入集合2（以-1结尾）"<<endl;
	Node *head2=input();
	Node *head3=same(head1,head2);
	cout <<"两集合的交集是" ;
	output(head3);
	cout<<"集合1对集合2的差集是";
	cha(head1,head2);//顺便给输出啦 
	cout <<endl;
	cout <<"集合2对集合1的差集是";
	cha(head2,head1);
	cout <<endl;
	all(&head1,head2);
	cout <<"两集合的并集是" ;
	output(head1);
	return 0;
} 

Node*input()//输入数据函数***不往里边传入任何形参*** 
{
	Node *head=NULL;
	int x;
	cin >> x;
	while(x!=-1)
	{
		Node *p=new Node;//错误1：p每次都需要重载，一定要放到循环里边呢*** 
		p->content=x;
		if(head==NULL)
		{
			head=p;
			p->next=NULL;
		}
		else
		{
			p->next=head;
			head=p;
		}
		cin >>x;
	}
	return head;
}

Node*same(Node*head1,Node*head2)//计算交集函数 
{
	Node* head3=NULL;
	Node*p;//把p定义成node类型的，因为head指向的也是node类型的**（以及链表中所有元素） 
	for(p=head1;p!=NULL;p=p->next)
	{
		Node*q;//每次都对q进行重载，每次都得从第一个元素开始检索 
		for(q=head2;q!=NULL;q=q->next)//如果是q->next!=NULL，那只能检索到倒数第二个元素了** 
		{
			if(p->content==q->content)//只能取出来一个数值，不能取出来地址（next）
									  //不然原来的链表也发生变化了*** 
			{
				Node*s=new Node;
				if(head3==NULL)
				{
					s->content=q->content;
					head3=s;
					s->next=NULL;
				}
				else
				{
					s->content=q->content;//就差这一行！！！细致再细致
										//在错误输出的时候就应该注意*越界一般都是没有给赋值的* 
					s->next=head3;
					head3=s;
				}
			} 	
		}
	}
	return head3;
}
  
void all(Node **head1,Node *head2)//直接在head1的链表上操作就可以啦 ，不需要返回头指针地址 
							   //尽量少对原始数据操作 ， 现在问题：头指针发生变化了 
{
	
	for(Node*p=*head1;p!=NULL;p=p->next)
	{
		for(Node*q=head2;q!=NULL;q=q->next)
		{
			if(q->content!=p->content)
			{
				Node *a;//排除重复元素，如果不同的元素和head1中所有元素都不同，才进行加入 
				for(a=*head1;a!=NULL;a=a->next)
				{
					if(a->content==q->content) 
						break;
				}
				if(a==NULL)//不是重复的元素 
				{
					Node *s=new Node;//现在加到head1的链表中，链表不能是空的呢** 
					s->content=q->content;
					s->next=*head1;
					*head1=s; 
				}
			}
		}
	}
	
}

//Node *head4=NULL;
/*for(Node*p=head1;p!=NULL;p->next)//完成新链表赋值，从头插入 
	{
		if(head4==NULL)
		{
			Node *s=new Node;
			s->content=p->content;
			s->next=NULL;
			head4=s;
		}
		else
		{
			Node *s=new Node;
			s->content=p->content;
			s->next=head4;
			head4=s;
		}
	}
	return head4;
	*/

void cha(Node *h1,Node *h2)
{
	Node *p3;
	Node *q3;
	int k=0;
	for (q3=h2;q3!=NULL;q3=q3->next)
		k++;//看h2中有多少元素** 
	for (p3=h1;p3!=NULL;p3=p3->next)
	{
		int j=0;
		for (q3=h2;q3!=NULL;q3=q3->next)
		{
			if (p3->content==q3->content)
				break;
			else
				j++; 
		}
		if (j==k)//在链表2中没有找到和1相同的元素，即这个元素是A中独有的，B中没有** 
			cout<<p3->content<<' ';
	}
}

void output(Node *h)//输出函数 
{ for (Node *p=h; p!=NULL; p=p->next)
	 cout << p->content << " ";
   cout << endl;
}






