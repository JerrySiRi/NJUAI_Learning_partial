#include <iostream>
#include <cstring>
using namespace std;
struct node
{
	char ch[15];
	int count;
	node *next;
};
node *q;
int main ()
{
	char b[20];
	cin>>b;
	node *head=NULL;
	node *tail=NULL;
	while (strcmp(b,"###")!=0)
	{
		for (int i=1;i<=n;i++)
		{
			char a[15];
			cin>>a;
			node *p=new node;
			strcpy(p->ch,a);
			for (q=head;q!=NULL;q=q->next)//加入之前先判断有几个和要加入的这个水果是相同的 
			{
				if (strcmp(q->ch,p->ch)==0)//值相等** 
				{
					q->count++;
					break;
				}
			}
			if (q==NULL)// 再把这个节点插入这个链表*** 
			{
				p->next=NULL;
				if (head==NULL)
					head=p;
				else
					tail->next=p;
				tail=p;
				tail->count=1;//因为里边的元素肯定比1大》》赋值成1肯定选择不到他的 
			}
		}
		cin>>n;
	}
	int max=0;
	for (node *s=head;s!=NULL;s=s->next)
	{
		if (max<s->count)
			max=s->count;
	}
	for (node *t=head;t!=NULL;t=t->next)
	{
		if (t->count==max)
		cout<<t->ch<<endl;
	}
	return 0;
}
