#include <iostream>
using namespace std;
/*
��дһ������
1 ���Ƚ����������ϣ��Ӽ������뼯�ϵ�Ԫ�أ�Ԫ��Ϊ����,��-1������
2 Ȼ��������������ϵ�  ���������� ���������Լ� �����
������1��Լ���2�Ĳ���㣺ȥ������1�����ڼ���2��Ԫ�أ�
3 ��������������Ҫ��������ʵ�ּ��ϵı�ʾ��
���Ӽ��ϵ����루��ȷ����С���ٵ����ϵ����㡾�������������Ҫ������ġ� 

Ҫ��
�ٲ���һmain���ס�Ӧ�ö����main����֮��ĺ�������������� 
�ڼ�����Ԫ��Ψһ���������ظ�Ԫ�ص�
 
 
����˼·��
�ٺ���һ���������ݣ���������2����
�ڽ����� 1��һ������Ϊ�����������ڶ�������
		 2����ڶ����У��ӵ�����������������֮�С�
�۲�������һ�������������������ڶ����������ֺ͵�һ�����ϲ�һ�����ͼӽ���
�������ı�������һ���������ֵ**
�ܲ��
 
*/


/*
�����ܽ᣺
�ٶ���ָ������⣺
[����������ı�ָ����ָ�ĵ�ַ�ˡ�ԭ����ָx�����ڱ��ָy�ˣ����̲��Ǹı�ָ����ָ��ֵ�ˣ���]
[����ʵ����Ҳ����ͷָ����ָ�ĵ�ַ��ȷ����ָ��ģ�] 
����ͷָ�����--head��ָ�Ķ�����ԭ����p�ˣ������¼����new Node*���ı��ַ>����ָ��*�� 
	����βָ�����--ֻ�ı�tailָ����ָ��ֵ**���ı�head��ָ��ĵ�ַ�ģ��Ϳ��Բ��ö���ָ���*

����ָ��
int *p=&x;
int **q=&p;
����x��x\*p\**q
����p��p\*q 
�����塿�����βε�ʱ���� void all(Node **head1,Node *head2)
�����á�����ʵ�ε�ʱ���� all(&head1,head2); 
����������ʱ����extern void all(Node**head1,Node*head2);

���ڴ��������ʱ���Ӧ��ע��*
situation1��������ֵ-Խ��һ�㶼��û�и���ֵ��*�����ʱ�䲻ͬ�õ���ֵ����һ������ 
situation2��û�����-û��ָ��ָ������ָ����ָ  
*/
struct Node
{
	int content;
	Node *next;
};
extern Node* input();
extern Node* same(Node*head1,Node*head2);//���� ����head3����������ͷָ�룩�����(ͳһoutput�� 
extern void all(Node**head1,Node*head2);
extern void cha(Node*h1,Node*h2);
extern void output(Node*h); 
int main()
{
	cout << "�����뼯��1����-1��β��"<<endl;
	Node *head1=input();
	cout << "�����뼯��2����-1��β��"<<endl;
	Node *head2=input();
	Node *head3=same(head1,head2);
	cout <<"�����ϵĽ�����" ;
	output(head3);
	cout<<"����1�Լ���2�Ĳ��";
	cha(head1,head2);//˳�������� 
	cout <<endl;
	cout <<"����2�Լ���1�Ĳ��";
	cha(head2,head1);
	cout <<endl;
	all(&head1,head2);
	cout <<"�����ϵĲ�����" ;
	output(head1);
	return 0;
} 

Node*input()//�������ݺ���***������ߴ����κ��β�*** 
{
	Node *head=NULL;
	int x;
	cin >> x;
	while(x!=-1)
	{
		Node *p=new Node;//����1��pÿ�ζ���Ҫ���أ�һ��Ҫ�ŵ�ѭ�������*** 
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

Node*same(Node*head1,Node*head2)//���㽻������ 
{
	Node* head3=NULL;
	Node*p;//��p�����node���͵ģ���Ϊheadָ���Ҳ��node���͵�**���Լ�����������Ԫ�أ� 
	for(p=head1;p!=NULL;p=p->next)
	{
		Node*q;//ÿ�ζ���q�������أ�ÿ�ζ��ôӵ�һ��Ԫ�ؿ�ʼ���� 
		for(q=head2;q!=NULL;q=q->next)//�����q->next!=NULL����ֻ�ܼ����������ڶ���Ԫ����** 
		{
			if(p->content==q->content)//ֻ��ȡ����һ����ֵ������ȡ������ַ��next��
									  //��Ȼԭ��������Ҳ�����仯��*** 
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
					s->content=q->content;//�Ͳ���һ�У�����ϸ����ϸ��
										//�ڴ��������ʱ���Ӧ��ע��*Խ��һ�㶼��û�и���ֵ��* 
					s->next=head3;
					head3=s;
				}
			} 	
		}
	}
	return head3;
}
  
void all(Node **head1,Node *head2)//ֱ����head1�������ϲ����Ϳ����� ������Ҫ����ͷָ���ַ 
							   //�����ٶ�ԭʼ���ݲ��� �� �������⣺ͷָ�뷢���仯�� 
{
	
	for(Node*p=*head1;p!=NULL;p=p->next)
	{
		for(Node*q=head2;q!=NULL;q=q->next)
		{
			if(q->content!=p->content)
			{
				Node *a;//�ų��ظ�Ԫ�أ������ͬ��Ԫ�غ�head1������Ԫ�ض���ͬ���Ž��м��� 
				for(a=*head1;a!=NULL;a=a->next)
				{
					if(a->content==q->content) 
						break;
				}
				if(a==NULL)//�����ظ���Ԫ�� 
				{
					Node *s=new Node;//���ڼӵ�head1�������У��������ǿյ���** 
					s->content=q->content;
					s->next=*head1;
					*head1=s; 
				}
			}
		}
	}
	
}

//Node *head4=NULL;
/*for(Node*p=head1;p!=NULL;p->next)//���������ֵ����ͷ���� 
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
		k++;//��h2���ж���Ԫ��** 
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
		if (j==k)//������2��û���ҵ���1��ͬ��Ԫ�أ������Ԫ����A�ж��еģ�B��û��** 
			cout<<p3->content<<' ';
	}
}

void output(Node *h)//������� 
{ for (Node *p=h; p!=NULL; p=p->next)
	 cout << p->content << " ";
   cout << endl;
}






