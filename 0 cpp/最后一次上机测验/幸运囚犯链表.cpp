#include <iostream>
using namespace std;
/*
step1:
���������� 
 */
struct Node
{
	bool is;
	char name[10];
	Node *next;	
};
int main() 
{
	int num,hao;
	cin >> num >> hao;
	//num����num���ˣ�hao�Ǳ���hao�ͳ�ȥ������false
	//step1:��������һ��num����**,ͷβ����Ŷ**
	//ע�������˳����ĿҪ����˳ʱ��+��������˳�����ġ���ֻ��βָ��������,��֤˳�� 
	//���һ��Ԫ������������Ǹ�����������ָ��ͷָ��Ϳ�����
	Node *head=NULL;
	Node *tail=NULL;//���϶�λ���һ��Ԫ�� 
	for(int i=0;i<num;i++)
	{
		if(head==NULL)//һ����û�� 
		{
			Node *s=new Node;
			cin >> s->name;
			head=s;
			tail=s;
			s->next=head;//��β���� 
		}
		else
		{
			Node *s=new Node;
			cin >> s->name;
			tail->next=s;
			s->next=head;
			tail=s;
		}
	}
	//�������������һ�����Σ�˳����ȷ 
	Node *p=head; 
	for(int i=0;i<num;i++)
	{
		p->is=true;
		p=p->next;
	}
	
	//��ʼ����
	int last=num;
	Node *q=head;
	while(last>1)
	{
		int count=0;//count��hao�˾ͳ�ȥ�� 
		while(count<=hao)//������1��while��������ţ��������������ŲŽ����ѭ����***���򲻽�
		//���ŵ������������߽������������߳�ȥ*** 
		{
			if(q->is==true)//��Ȧ����� 
			{
				count++;
				if(count==hao)
					goto L;//������ʱ��С��ѭ��������������������count++��������һλ��
					//��ʵ����Ӧ���Ǳ����������֮��Ͳ�Ӧ������������������ˡ��ڲݸ�ֽ�϶������һ��ѽ��������
				q=q->next;
			}
			else
				q=q->next;
		}
		L:
		//����qָ�ľ��Ǽ�������������
		q->is=false; //����Ȧ������� 
		last--;
	}		 
	Node *w=head;
	for(int i=0;i<num;i++)
	{
		if(w->is==true)
		{
			cout << w->name;
			break;
		}
		else
			w=w->next;
	}

	return 0;
}
