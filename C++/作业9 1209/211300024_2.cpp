#include <iostream>
using namespace std;
/*
������ʵ�ֲ�������
�Ѵ���������ֳ��������֣�AΪ���ź��������BΪδ�ź��������
��ʼ״̬�£�A��û��Ԫ�ء����㷨���δ�B��ȡ�����뵽A�е���Ӧλ�ã�ֱ��B�е���ȡ��Ϊֹ��
�������㷨��һ������ʵ��**���Զ���main������ɶԸú����ĵ��ò��ԡ�

˼·��
�����β��뵽��Ӧλ�� 
����B���ҵ�����Ԫ�أ�����A�����С����Ұ�B��Ԫ�ص�content�ĵ��������һ��ѭ��������û��Ԫ�أ� 
*/

/*
�����ܽ᣺
�ٶ���ָ������á���ԭ��������֮�н���ɾ��**��
ֻҪ��ԭ����֪�������в�����Ӧ���ö���ָ���**

��������������Ҫÿ���������ݾ�Ӧ�÷���ѭ���ڽ�������**��
������p_maxû�зŵ�ѭ��֮��
��ô��һ���ҵ����������Ľڵ�֮��֮�������ڵ�ɾ��֮��
p_max���ָ��û�ж����ˣ������޷�����p->content��ѭ���е�content���бȽ���
����p_maxҲ�޷��������µ�ֵ*
����ָ��ָ����Ч����**

��Ѱ�ҽڵ��ǵڼ�����i++��λ�á�
Ū��if�����Ǹ�ʲô�ģ�ֵ���֮���ٳ�ѭ����
Ū��i++�Ǹ�ʲô�ģ�ֻҪѭ���ƶ�һ�Σ�������������Ϊ����ô����λ��һ��Ҫ��һ����** 
*/
struct Node
{
	int content;
	Node* next;
};
extern Node *input();
extern Node *pai(Node **head1);
extern void output(Node *h);

int main() 
{
	cout << "�������������������У���-1������"<<endl;
	Node *head1=input();//��ɶ�B������������**
						//��ɶ�A��Ԫ�صĲ��� 
	Node*head2=pai(&head1);
	output(head2);
	return 0;
}


Node *input() //�ӱ�ͷ��������
{  Node *head=NULL; //ͷָ��
	int x;
	cin >> x;
    while (x != -1)
	{ Node *p=new Node;
	   p->content = x;
	   if(head==NULL)
	   {
	   	p->next=NULL;
	    head=p;
	   }
	   else
	   {
	   p->next = head;
	   head = p;
	}
       cin >> x;
	}
	return head;
} 


Node *pai(Node **head1)
{
	Node *head2=NULL;
	while(*head1!=NULL)
	{Node *p_max=*head1;//������2��û��ÿ������***�� 
		//step1:�ҵ�����Ԫ�� 
		for(Node *s=*head1;s!=NULL;s=s->next)//�ж�һ�»���û��Ԫ�� 
		{
		     //p_maxָ�����Ľ�㣬��ʼ��Ϊp1��������������סλ�����ĵ�***�� 
			if (s->content > p_max->content)  p_max = s;//��������ַ�ͺ���**�� 
	    //��������Ԫ�ؾ���p_max��*
		}
		int i=0;
		for(Node *s=*head1;s!=NULL;s=s->next)
		{	i++;//������3��i++��λ���ǲ�������if��ߡ� 
			if(s->content==p_max->content)
				break;
		}
		//step2: ����������ĸ�ֵ
		if(head2==NULL)
		{
			Node *t=new Node;
			t->content=p_max->content;
			t->next=NULL;
			head2=t;
		} 
		else
		{
			Node*t=new Node;
			t->content=p_max->content;
			t->next=head2;
			head2=t;
		}
		//step3:ɾ���ڵ�--ѭ���������ı� 
		if (i == 1) //Ҫɾ���Ľ��������ĵ�һ����㡣
		{	
		Node *p=*head1; //pָ���һ����㡣
		*head1 = (*head1)->next; //headָ���һ�����
						//����һ����㡣
		delete p; //�黹��ɾ�����Ŀռ䡣
		}
	else //Ҫɾ���Ľ�㲻������ĵ�һ����㡣��ɾ�����һ���Ͳ������һ����һ����
											//���һ����next����ֵ��Ϊ��NULL�ˣ��� 
	{	
		Node *p=*head1; //pָ���һ����㡣
		int j=1; //��ǰ������ţ���ʼ��Ϊ1
		while (j<i-1) //ѭ�����ҵ�i-1�����
		{	p = p->next; //pָ����һ�����
			j++; //�����ż�1
		}
			Node *q=p->next; //q��ס��i����㡣
			p->next = q->next; //�ѵ�i-1������next
						  //ָ���i+1�����
			delete q;  //�黹��i�����Ŀռ䡣
	}
	}	 
	return head2; 
}



void output(Node *h)//������� 
{ for (Node *p=h; p!=NULL; p=p->next)
	 cout << p->content << " ";
   cout << endl;
}
