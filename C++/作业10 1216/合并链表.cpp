#include<iostream>
using namespace std;
/*
��Ŀ�������ϲ�����
����2����������L1��L2����������ĳ��ȷֱ���n1��n2��
ÿ�������е������Ѿ����մ�С�������кã�**   
����Ҫ������������кϲ�������֤�ϲ���������е�������Ȼ���ִ�С��������***��
�����ʽ:	
��һ�У�n1 n2��1��n1��10000��1��n2��10000
�ڶ��У�n1���Ǹ��������ÿո����
�����У�n2���Ǹ��������ÿո����
�����ʽ
�ϲ�����������ݣ��ÿո������
��������
input
3 5****������Ǵ�С����
3 7 11
2 8 9 12 16
output
2 3 7 8 9 11 12 16

��Ŀ˼·��
���������֣����������еĽڵ����ݣ������ú���Node *input(int a)��
        ��Ϊ���ⲻ��-1����������Ҫ��whileѭ����������ĸ�����
��������һ�������н��в��룬�ȽϽڵ����ݵĴ�С**��ע��Ҫʹ�ö�������**���ܶ�head���в����ģ�
""

����

���ڰ�����һ����������ݽ��б䶯��ʱ��һ��Ҫ���ٶ���һ����̬��������ָ��ԭ���Ǹ�
							�����ָ�룬��������������ָ����ָ�Ŀ����ԣ��� 
��βָ�뻹����̫��ѽ���϶�βָ��Ĳ�������ʧ��***
				��ֵ+�����µ�Ԫ��+λ�õı����һ����������*** 
*/

struct Node
{
    int content;
    Node *next;
};

extern Node*input(int a);
extern void insert(Node *&head1,Node *head2);
extern void output(Node *head1);
int main()
{
    int a,b;
    cin >> a >> b;
    Node *head1=input(a);
    Node *head2=input(b);
    insert(head1,head2);
    output(head1);
    return 0;
}


Node *input(int a)//��ͬ����Ŀһ��Ҫͨ����ͬ�ķ�ʽ��������ڵ�����
//������Ҫ��С������������ģ�����һ����ȡβ������*** 
{
    int i,x;
    Node *head=NULL;//����ͷָ�룬��ʼ��ΪNULL��һ��Ҫ����ѭ������ߵ�***��������
    Node *tail=NULL;
    //Ҫ������ĵ�һ��Ԫ��Ҳ�����жϵ�**��һa==0�ء����ж�������**
    for(i=0;i<a;i++)
    {
        cin >>x;
        Node *p=new Node;//������̬�������������У���Ϊ�ڵ㡣һ������ѭ���У�ÿ�����أ������½ڵ�
        p->content=x;//��ô�����Ǹ�ֵѽ������ 
        if(head==NULL)
        {
        	p->next=NULL;//��Ƚ����еĲ��������ǰѳ�ʼ���Ĳ���������if�����** 
        	head=p;
        	tail=p;
        	
        	
        }
        else
        {
            p->next=NULL;
            tail->next=p;
            tail=p;
        }
    }
    return head;
}

//��head1����Ļ����Ͻ��в�����Ҫ��head1���ж���ָ���������***��ʹ��
void insert(Node *&head1,Node *head2)
{
    Node *p,*q,*q1;
    Node *a=head1;
    while(a->next!=NULL)
   		a=a->next;//ÿ�ε�����Ѱ��βָ���λ��
    //for(a=head1;a!=NULL;a=a->next)//a��βָ�롾��һ������Ǵ�������ġ� 
    //{
       // ;
   // }
    for(p=head2;p!=NULL;p=p->next)
    {
    	Node *b=new Node;
    	b->content=p->content;
        for(q=head1;q->next!=NULL;q=q->next)//ѭ���������ڶ���
        {
            q1=q->next;
            if(b->content>=q->content && b->content <=q1->content)//����ͷָ���βָ���λ��
            {
                b->next=q1;
                q->next=b;
                break;
            }
            else if(b->content<=head1->content)//��ͷָ��λ�ò���
            {
                b->next=head1;
                head1=b;
                break;
        	} 
            if(b->content>=a->content) //ֻʣ����βָ����������*
            {
                b->next=NULL;
                a->next=b; 
                a=b;
                break;
            }
        }
    }
}


void output(Node*head1)
{
    Node *p;
    for(p=head1;p!=NULL;p=p->next)
    {
        cout << p->content << " "; 
    }
}

