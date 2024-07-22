#include <iostream>
using namespace std;
/*
m������Χ����һ��Ȧ������˳ʱ�뷽���1��m��š�
Ȼ���1�ſ�ʼ˳ʱ�뱨��������n���������֣�Ȼ���ٴӸճ��ֵ�������һ��λ�ÿ�ʼ���´�1����.
����ظ���ֱ��ֻʣ�����һ��������������˵�����������ͷš�(1<=n<=m)

���룺
����������С���һ����������Ŀm�ͳ��ֵı���n���ڶ����Ǳ��Ϊ1��m��ÿ����������

�����
��������������[��һ���ַ����ģ���һ����һ����ĸ��**]

�������룺
8 3
A B C D E F G H

���������
G
*/


//�������������

struct Node
{	int no;  //С���ı��
	Node *next; //ָ����һ��С����ָ��
};
int main()
{	int m, //���ڴ洢Ҫ������
		n, //���ڴ洢С���ĸ���
		num_of_children_remained; //���ڴ洢Ȧ����
						       //ʣ�µ�С������
	cout << "������С���ĸ�����Ҫ��������";
	cin >> n >> m;
 //����Ȧ��
	Node *first,*last; //first��last���ڷֱ�ָ���һ����
				    //���һ��С��
	first = last = new Node;  //���ɵ�һ�����
	first->no = 0; //��һ��С���ı��Ϊ0
	for (int i=1; i<n; i++) //ѭ����������С�����
	{	Node *p=new Node;  //����һ��С�����
		p->no = i; //�µ�С�����ı��Ϊi
		last->next = p; //���һ��С����nextָ��������
                                //��С�����
		last = p; //�������ɵ�С������Ϊ���һ�����
	}
	last->next = first;  //�����һ��С������һ��С��
 				      //��Ϊ��һ��С��������Ȧ��

//���ȴ���һ������������ٰ�Ȧ����β��������***
//��ʼ������ֻҪ������������ڵ㣬��ô������***�������ȥ�ˣ�ɾ���ڵ�Ϳ��������� 
	num_of_children_remained = n;  //����ǰ��Ȧ����С������
	Node *previous=last;  //previousָ��ʼ������ǰһ��С��
	while (num_of_children_remained > 1)
	{	for (int count=1; count<m; count++)  //ѭ��m-1�Ρ�ע��count=1����������ó��ͷ�previousָ��Ľڵ�
	//�´�ѭ��previous��ָ��һ��δ֪�Ŀռ��ˣ����������������������ͷŵ�ʱ��һ����һ�������ָ��ָ��Ҫ�ͷŵ�*���� 
			previous = previous->next;
		//ѭ������ʱ��previousָ��Ҫ�뿪Ȧ�ӵ�С����ǰһ��С��
		Node *p=previous->next;  //pָ��Ҫ��Ȧ��С�����
		previous->next = p->next;  //С���뿪Ȧ��
		delete p;  //�ͷ���ȦС�����Ŀռ�
		num_of_children_remained--;  //Ȧ��С������1
	}
	
	//���ʤ���ߵı��
	cout << "The winner is No." << previous->no << "\n";
	delete previous;  //�ͷ�ʤ���߽��Ŀռ�
	return 0;
}
 
 
 
 
 
 
 
 
 
 
 
 
 
 
//����һ����ϰ���飨��������**�� 
/*
int main() 
{
	int m,n;
	cin >> m >> n;
	int k=m;
	typedef char A[10];
	A name[1][m];//һ����m����***���˴���ά���鲻�Ǻ����Ե�***�� 
	//������ʵҲ�����ýṹ��������jail A[m];����ʾ��**
	for(int i=0;i<m;i++)
		cin >> name[1][i];
	bool zai[m];//����ȫ���� 
	for(int i=0;i<m;i++)
		zai[i]=true;
		
	int index=m-1;
	//��һ��Ҫ������λ����(index+1)%m �����ture��count++ 
	while(k>1)//m�ɲ��ܶ��أ�����ÿ�μ���0-m-1�ķ�Χ������Ҫԭ����m�� 
	{
		int count=0;
		int b;
		while(count<n)
		{
			b=(index+1)%m;
			if(zai[b])  count++;
			index++;
		}
		zai[b]=false;
		k--;
	}
	int i;
	for(i=0;i<m;i++)
	{
		if(zai[i]==true) break;
	}
	cout<<name[1][i];

	return 0;
}
*/
