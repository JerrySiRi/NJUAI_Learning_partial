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
			for (q=head;q!=NULL;q=q->next)//����֮ǰ���ж��м�����Ҫ��������ˮ������ͬ�� 
			{
				if (strcmp(q->ch,p->ch)==0)//ֵ���** 
				{
					q->count++;
					break;
				}
			}
			if (q==NULL)// �ٰ�����ڵ�����������*** 
			{
				p->next=NULL;
				if (head==NULL)
					head=p;
				else
					tail->next=p;
				tail=p;
				tail->count=1;//��Ϊ��ߵ�Ԫ�ؿ϶���1�󡷡���ֵ��1�϶�ѡ�񲻵����� 
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
