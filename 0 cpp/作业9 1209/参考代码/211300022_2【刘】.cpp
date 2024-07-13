#include <iostream>
using namespace std;
struct Node
{
	double content;
	Node *next;
};
Node *input(int n)
{
	Node *head=NULL;
	double x;
	for (int i=1;i<=n;i++)
	{
		cin>>x;
		Node *s=new Node;
		s->content=x;
		s->next=head;
		head=s;
	}
	return head;
}
void swap(double *s,double *v)
{
	int t=*s;
	*s=*v;
	*v=t;
}
void f(Node *&h1,Node*&h2)
{
	Node *q1=new Node;
	q1->content=h1->content;
	q1->next=h2;
	h2=q1;
	Node *p=h1->next;
	for (;p!=NULL;p=p->next)
	{
		Node *q2=new Node;
		q2->content=p->content;
		q2->next=h2;
		h2=q2;
		for (Node *q3=h2;q3->next!=NULL;q3=q3->next)
		{
			Node *q4=q3->next;
			if (q3->content>q4->content)
				swap(&q3->content,&q4->content);
		}
	}
}
int main ()
{
	int n;
	cout<<"请输入您要输入的元素（先输入元素个数）：";
	cin>>n;
	Node *h1=input(n);
	Node *h2=NULL;
	f(h1,h2);
	Node *q4=h2;
	for (;q4!=NULL;q4=q4->next)
		cout<<q4->content<<' ';
}
