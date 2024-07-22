#include <iostream>
using namespace std;

	struct Node
{	int content;  //�����������
	Node *next;  //�����һ�����ĵ�ַ
}; 
extern Node *input(); //�������ݣ������������������ͷָ��
extern void sort(Node *h); //����
extern void output(Node *h); //�������
extern void remove(Node *h); //��������

int main()//���ɣ��������Ŀһ��������Ķ���ͷָ��*ֻҪ֪��ͷָ��������������Ͷ�֪���� 
{  Node *head;
	head = input();
	sort(head);
	output(head);
	remove(head);
    return 0;
}

/*
Node *input() //�ӱ�β�������ݡ��������0��1++��1������Ĺ��̺϶�Ϊһ�� 
{  Node *head=NULL, //ͷָ��   
		  Node*tail=NULL; //βָ��
		  ����������Ϊ�ա� 
	int x;
	cin >> x;����ʼ��������**��һ�����ݵ�����Ҳ����Ҫ�жϵġ� 
    while (x != -1)
	{ Node *p=new Node;
	   p->content = x; 
	   p->next = NULL;
	   if (head == NULL)����0-1�Ĺ��̡� 
	      head = p;
       else
		tail->next = p;***else������* 
	
       tail = p;
       cin >> x;
	}
	return head;
}
*/
Node *input() //�ӱ�ͷ�������ݡ����������ַ���Ŷ***�� 
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
	   //�������˴�0-1+1-����Ĺ��̡�
	   //����Ƕ�������****��0-1�ٵ�1-���࣬�����������*** 
	   /*
	   ��0-1**
	   p�е�next��NULL
	   head������p
	   
	   ��1-����**
	    
	    ������
		
		���ϣ�ֻ��Ҫ��head�ĳ�ʼֵ����NULL�Ϳ�����*** 
	   */
	   head = p;
	}
       cin >> x;
	}
	return head;
} 

void sort(Node *h) //����ѡ������С����ǰ�š���������ͷָ��**�� 
{  if (h == NULL || h->next == NULL) return;//��ɶҲû��*�� 
    //������ͷ��ʼ����С����ķ�Χ
	for (Node *p1=h; p1->next != NULL; p1 = p1->next)
	{ Node *p_min=p1; //p_minָ����С�Ľ�㣬��ʼ��Ϊp1��������������סλ�����ĵ�***�� 
       //��p1����һ����ʼ��p_min���бȽ� 
	   for (Node *p2=p1->next; p2 != NULL; p2=p2->next)
	      if (p2->content < p_min->content)  p_min = p2;//��������ַ�ͺ���**�� 
	    
	   if (p_min != p1) //�����������ݡ�ֻ����ֵ����λ�á� 
	   { int temp = p1->content;
          p1->content = p_min->content;
          p_min->content = temp;
	   }
	}
}

/*
����ѭ����
��ʼ��������ʼѭ���Ľڵ���ֵ
ѭ��������һ��ѭ�������һ�����ߵ����ڶ���
ѭ�����£����ָ��ָ����һ��ָ��** 

�������е�ѡ������ͬ���ǣ�
�����������ѡ���������ģ��ŵ���󣬲�����n--

�ڵ���������ֻȡ�ֲ�������***������С����ǰ��*** 
*/
void output(Node *h)
{ for (Node *p=h; p!=NULL; p=p->next)
	 cout << p->content << ',';
   cout << endl;
}

void remove(Node *h)
{	while (h != NULL)
	{	Node *p=h;
		h = h->next;
		delete p;
	}
}

