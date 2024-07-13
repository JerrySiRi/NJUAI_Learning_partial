#include <iostream>
#include <cstdio>
using namespace std;
struct Node
{
	int content;
	Node *next;
};
Node *input(int n)
{
	Node *head=NULL;
	int x;
	for (int i=1;i<=n;i++)
	{
		cin>>x;
		Node *pk=new Node;
		pk->content=x;
		pk->next=head;
		head=pk;
	}
	return head;
}
void jiaoji(Node *h1,Node *h2)
{
	Node *p1=new Node;
	Node *q1=new Node;
	p1=h1;
	while (p1!=NULL)
	{
		for (q1=h2;q1!=NULL;q1=q1->next)
		{
			if (p1->content==q1->content)
			{
				cout<<p1->content<<' ';
				break;
			}
		}
		p1=p1->next;
	}
}
void bingji(Node *h1,Node*h2)
{
	Node *p2;
	Node *q2;
	p2=h1;
	int k=0;
	for (;p2!=NULL;p2=p2->next)
	{
		cout<<p2->content<<' ';
		k++;
	}
	for (q2=h2;q2!=NULL;q2=q2->next)
	{
		int j=0; 
		for (p2=h1;p2!=NULL;p2=p2->next)
		{
			if (p2->content==q2->content)
				break;
			else
				j++;
		}
		if (j==k)
			cout<<q2->content<<' ';
	}
}
void chaji(Node *h1,Node *h2)
{
	Node *p3;
	Node *q3;
	int k=0;
	for (q3=h2;q3!=NULL;q3=q3->next)
		k++;
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
		if (j==k)
			cout<<p3->content<<' ';
	}
}
int main ()
{
	cout<<"�����뼯��1�������뼯��1��Ԫ�ظ�������";
	Node *head1;
	Node *head2;
	int n1,n2;
	cin>>n1;
	head1=input(n1);
	cout<<"�����뼯��2�������뼯��2��Ԫ�ظ�������";
	cin>>n2;
	head2=input(n2);
	cout<<"����Ϊ��"; 
	jiaoji(head1,head2);
	cout<<endl;
	cout<<"����Ϊ��";
	bingji(head1,head2);
	cout<<endl; 
	cout<<"�Ϊ��";
	chaji(head1,head2);
	cout<<endl; 
}
