#include <iostream>
#include <cstring>
using namespace std;
/* 
��Ŀ���޿�����ѧ��

��Ŀ������

һ����50��ѧ����ѡ�޿����Ρ���50���˶���ѡһ�顿 
�������ɿ����ε�ѡ��ѧ�����֣�����ΪӢ�ģ�����С��10���ַ���û��������
����޿�����ѧ��������˵�����������У�����ѡ�����������һ��Ϊ"###"����ʾ���������
���˵��������޿������ж���ѧ�������������ʱ���ʵ�˳����һ�������������֮���ÿո�ָ���

Sample:
һ�����ֿγ̣�ÿ���γ���һЩѧ��ѡ 
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
step1���Ȱ����������������������˭ѡ��������
step2��������Щ�˵��ֵ�������������*** 
*/
struct Node
{
	char name[10];
	int count;//��Ҫ��ʼ����1,ÿ�ҵ�һ�ζ�+1 
	Node *next;
	
};
int main() 
{
	//step1����������
	Node *head=NULL;
	char ch[10];
	cin >> ch;
	while(strcmp(ch,"###")!=0)//����Ĳ���###�Ž�ѭ����*** 
	{
		if(head==NULL)
		{
			Node *p=new Node;
			strcpy(p->name,ch);
			p->next=NULL;
			head=p;
		}
		else//�����һЩ�ڵ��ˣ��ȿ������������һ�������û���ظ��� 
		{
			Node *s;
			for(s=head;s!=NULL;s=s->next)
			{
				if(strcmp(ch,s->name)==0)
						break;//���������ظ��ģ�sָ������ظ��Ľڵ㡣 
			}
			if(s!=NULL)//���ظ���
				s->count=s->count+1;
			else//û���ظ��� �������½ڵ�** 
			{
				Node *p=new Node;
				strcpy(p->name,ch);
				p->next=head;
				head=p;
			} 
		}
		cin >> ch;
	}
	//ȫ��������� 
	Node *s;
	int max=head->count;
	for(s=head;s!=NULL;s=s->next)
	{
		if(s->count>max)
			max=s->count;
	}
	//����max�����޿����������ˣ�û�����⣡
	//strcmp�����һ���ַ���С�ڵڶ����ַ���������<0***
//���뷨һ����������max���˶������������մ�С��С��������� 
	typedef char A[10];
	A a[50];//a[50]����50��Ԫ�أ�ÿ��Ԫ�ض���10���ַ�����С 
	int i=0;
	for(Node *p=head;p!=NULL;p=p->next)
	{
		if(p->count==max)
		{
			strcpy(a[i],p->name);
			i++;//�����˵��޿�����˵����ֶ�����������������*** 
		}
	} 
//�����Ǵ�СΪi����
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
			//�ҵ���С���Ǹ����±�***
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
//���뷨�����������������������ý���λ�á����Ž�***** 
/*
���� 
�ٰ����ֵ���������****�ı��ʾ��� �����򡱡����ҵ�������˼�롿 
��Ҫ��֮ǰ��������Ŀ���й��������е����龰ֻ�ǻ�������ҩ��*****��
������˼�붼��û���****����������������

���������ķ�����
1������ð�ݡ�ѡ��
2����������
��ֻѧ�������֣�������Ŀ�����£����������ں˵�����ʲô�������Ͼ���һ������λ�õ�ѽ���� 


��˼·��˳����
ǰ��洢��ʱ���Ѿ���������***
�Ѿ���ָ��ָ�����Ŀ��ڵ��ˣ�Ϊʲô���ú�������

��������ã�
�ٴ洢����
�ڿ��Խ��н����ģ�������ͬʱ�����޸�����*** 



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
�뷨����ɾ���ڵ�

���ƣ�
ɾ���ڵ���Ҫ֪������ǵڼ����ڵ㣬������Ҫ�ж����ǲ���ͷ����������
�鷳�Ⱥܸߣ���������
����һ�����ɾ���ڵ����Ŀ��������***�½���һ��������ʵ�ֵ�***
�����ͱ���ɾ���ڵ��˰�***��������Ŀ��������ɾ����������***�� 
 

 
*/

















/*
Node *q;
			Node *min;
			for(q=p->next;q!=NULL;q=q->next)//�ҵ��������С���ֵ�����Ǹ�*** 
			{
			
				if(q->count==max)//���������ֵ����q�Ĵ�С* 
				{
					if(stecmp(p->name,q->name)<0)//p���ֵ����С
						min=p;
					else
						min=q; 
				}
			}
			//������С�ľ���min��**��min����ͺ���***
			//������Ҫɾ���ڵ�**
*/
