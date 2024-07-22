#include <iostream>
using namespace std;
struct Node{int num;Node *next;};

void sort(Node **head,int n)
{for(int i=1;i<n;i++)
	{Node *p=*head,*pre_p=*head;
	while(p->next!=NULL)
		{pre_p=p;
		p=p->next;
		}
	int a=p->num;
	int min=(*head)->num;
	Node *m=*head,*after_m=(*head)->next;
	for(int j=1;j<i;j++)
		{m=m->next;
		after_m=m->next;
		}
	int max=m->num;
	if(a<min)
		{p->next=*head;
		*head=p;
		pre_p->next=NULL;
		}
	else if(a>=max)
		{if(i<n-1)
		{p->next=after_m;
		m->next=p;
		pre_p->next=NULL;
		}
		}
	else
		{Node *q=(*head)->next,*pre_q=*head;
		for(int j=2;j<=i;j++)
			{if(q->num>=a)
				{p->next=q;
				pre_q->next=p;
				pre_p->next=NULL;
				break;
				}
			else
				{pre_q=q;
				q=q->next;
				}
			}
		}
	}
return;
}

int main()
{Node *head=new Node;
Node *p=head,*pre;
int n;
cout<<"请输入待排序整数的数目:"<<endl;
cin>>n;
cout<<"请输入待排序的各整数:"<<endl; 
for(int i=1;i<=n;i++)
	{cin>>p->num;
	p->next=new Node;
	pre=p;
	p=p->next;
	}
delete p;
pre->next=NULL;
sort(&head,n);
cout<<"排序结果为:"<<endl;
Node *m=head;
while(m!=NULL)
	{cout<<m->num<<' ';
	m=m->next;
	}
delete head; 
return 0;
}
