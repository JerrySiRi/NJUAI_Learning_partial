#include <iostream>
using namespace std;
struct Node{int num;Node *next;};

void intersection(Node *head1,Node *head2,Node *head)
{Node *p=head1,*m=head,*pre;
while(p!=NULL)
	{Node *q=head2;
	int a=p->num;
	while(q!=NULL)
		{if(q->num==a)
			{m->num=a;
			m->next=new Node;
			pre=m;
			m=m->next;
			break;
			}
		else
			q=q->next;
		}
	p=p->next;
	}
delete m;
pre->next=NULL;
return;
}

void difference(Node *head1,Node *head2,Node *head)
{Node *p=head1,*m=head,*pre;
while(p!=NULL)
	{Node *q=head2;
	int a=p->num;
	bool different=true;
	while(q!=NULL)
		{if(q->num==a)
			{different=false;
			break;
			}
		else
			q=q->next;
		}
	if(different)
		{m->num=a;
		m->next=new Node;
		pre=m;
		m=m->next;	
		}
	p=p->next;
	}
delete m;
pre->next=NULL;
return;
}

void union_(Node *head1,Node *head2,Node *head)
{Node *head_difference=new Node;
difference(head1,head2,head_difference);
Node *p=head_difference,*q=head2,*m=head,*pre;
while(p!=NULL)
	{m->num=p->num;
	p=p->next;
	m->next=new Node;
	pre=m;
	m=m->next;
	}
while(q!=NULL)
	{m->num=q->num;
	q=q->next;
	m->next=new Node;
	pre=m;
	m=m->next;
	}
delete m;
pre->next=NULL;
delete head_difference;
return;
}

int main()
{int a,b;
cout<<"请输入集合A中元素数目:"<<endl;
cin>>a;
Node *head1=new Node;
Node *p=head1,*pre;
cout<<"请输入集合A中各元素:"<<endl;
for(int i=1;i<=a;i++)
	{cin>>p->num;
	p->next=new Node;
	pre=p;
	p=p->next;
	}
delete p;
pre->next=NULL;
cout<<"请输入集合B中元素数目:"<<endl;
cin>>b;
Node *head2=new Node;
p=head2;
cout<<"请输入集合B中各元素:"<<endl;
for(int i=1;i<=b;i++)
	{cin>>p->num;
	p->next=new Node;
	pre=p;
	p=p->next;
	}
delete p;
pre->next=NULL;

Node *head3=new Node;
intersection(head1,head2,head3);
cout<<"所求交集中的元素为:"<<endl;
p=head3;
while(p!=NULL)
	{cout<<p->num<<' ';
	p=p->next;
	}
cout<<endl;
delete head3;

Node *head4=new Node;
difference(head1,head2,head4);
cout<<"所求差集中的元素为:"<<endl;
p=head4;
while(p!=NULL)
	{cout<<p->num<<' ';
	p=p->next;
	}
cout<<endl;
delete head4;

Node *head5=new Node;
union_(head1,head2,head5);
cout<<"所求并集中的元素为:"<<endl;
p=head5;
while(p!=NULL)
	{cout<<p->num<<' ';
	p=p->next;
	}
delete head5;
return 0;
}
