#include <iostream>
#include <cstring>
using namespace std;
/*  
��Ŀ������ˮ����������ʵ�֣�
��Ŀ������
ÿ����ũӵ�����ɿ�*��С��ͬ�ĵأ�ÿ��ض�����ˮ����������ҳ���ֲ��������ˮ����**

���룺
��������ũ����ֲ�������0��Ϊ���յĽ��������������*�� 
ÿ����ũ�����У���һ��Ϊ������Ŀn������n�зֱ�Ϊÿ�����ֲ��ˮ����

�����
����ˮ����ʲô(�����������£�����ȳ��ֵ�ˮ��,֮�������һ�����ˮ��)��ѭ����ѡ����*�� 

�������룺
5
peach
apple
banana
apple
apple
3
pear
orange
pear
1
pear
0

���������
apple
pear
*/
struct Node
{
	char ch[20];
	Node *next;	
};

/*
�����ͽ�ѵ��
��while����for��ѭ��������������ѭ�����е� 
������һ���ٽ��������жϵ�ʱ������һ��ѭ����
while(n!=0)
{
	int n
	cin >> n;
} 
������nʼ��ֻ������һ��ѭ�����д��ڣ���������һ��ѭ���Ŀ�ʼ�����������ж�**
�����ײ����أ�������

���޸ģ�ֱ��cin >>nҲ�ǿ��Ըı�int n��ֵ***���ܸ������������ģ���

�ڼ��������ۼ���  ������Ҫ��������ֵ��***
int count =0;
int sum=0; 

�ۿ�������Ҫ�������***����һ�㶼�������������***
���������������һ��NULL��***�����㵱ǰ�ڵ��ж��ٸ��ظ�Ԫ��***���� 

��һ��if���涼��ֱ�ӵĲ����� (������ʹ��if;+else��������ɶ��Բ)
��if(strcmp(a,b)==0)
	count++;�� 
	
��ʲô����Ӧ�÷���ѭ����ߣ�ʲô������Ӧ�÷���ѭ����� 
���Լ�д���Լ�������߹�һ������ѭ�������ѽ����
head \max\max1���Ƿ�����ߵ���** 
*/ 
extern Node *input(int n,Node *&head);
extern int what (Node *s,Node *head);
extern void fruit(Node *head);

int main() 
{
	int n;
	cin >> n;
	Node *head=NULL;//�������涨��head��֮��ÿ�λ��޸�head��ֵ���п��ܲ��޸��أ� 
	for(;n!=0;cin >> n) 
	{
		head=input(n,head);
	}
	fruit(head);
	return 0;
}

//step1:���뺯������������ĸ����ģ�
//���������뼸��+ͷָ�루֮��Ҫ�����������в����ģ�������Ҫ������**��ͷָ���������� 
Node *input(int n,Node *&head)//Ҫ�����ָ����߼���n��Ԫ��* 
{
	for(int i=0;i<n;i++)
	{
		char ch[20];//Ҫ��strcpy�������ַ����ĸ�ֵ���� 
		cin >> ch;//ÿ�����ch����Ҫ���ص�**��������
		Node *p=new Node;
		if(head==NULL)
		{
			strcpy(p->ch,ch);
			p->next=NULL;
			head=p;
		} 
		else
		{
			strcpy(p->ch,ch);
			p->next=head;
			head=p;
		}
	}
	return head;
}


int what (Node *s,Node *head)//����ÿһ���ڵ��ж��ٸ������ظ��� 
//���ֻ��s���ָ�봫��������ֻ��֪��s֮��Ľڵ���ʲô����֪��ǰ���ѽ 
{
	int count=0;
	char a[20];
	if(s==NULL)
	{
		return 0;
	}
	strcpy(a,s->ch);
	for(Node *p=head;p!=NULL;p=p->next)
	{
		if(strcmp(a,p->ch)==0) 
			count++;//��ͬ����0 ����һ�����ͽ�if����� 
	}
	return count;
}


void fruit(Node *head)
{
	int max=0;
	char max1[20];	
	Node *s;
	Node *p=head;
//Q5:
	max=what(p,head);
	strcpy(max1,p->ch);
	
	for(;p!=NULL;p=s)//p�䵽��Ҫ���������ˮ��������˭�������� 
	{
		
		for(s=p->next;s!=NULL;s=s->next)
			if(strcmp(s->ch,p->ch)) break;
			//����s������һ����Ҫ������λ����* 
		int a;
		a=what(s,head); 
		if(max<a) 
		{
			strcpy(max1,s->ch);
			max=a;
		}
	}
	p=head;
	if (what(p,head)==max) cout<<p->ch;
	for(;p!=NULL;p=s)//p�䵽��Ҫ���������ˮ��������˭�������� 
	{
		
		for(s=p->next;s!=NULL;s=s->next)
		{
			if(strcmp(s->ch,p->ch)) break;
		}//����s������һ����Ҫ������λ����* 
				
		if (what(s,head)==max) cout<<s->ch;
	}
}

