#include <iostream>
using namespace std;
/*
ѧУ�ٰ����������ɣ�Ϊ�˱�֤�˶���ƽ��ÿλѡ��������ֻ�����һ��RFID��ǩ
�ھ���������ʱ��������Ὣ��¼������id��ѡ�ֵĺ��뼰������������ʱ�䣨ʱ�����24Сʱ��ʽ��HH MM SS���ϴ����������С�
�����˶�һ����3�����������ֱ����ڳ����㡢�м����յ㣬��Ӧ�Ĵ�����id�ֱ�Ϊ0��1��2��
���������������ݣ�����ж����˶�ԱΥ�档Υ����жϣ���1�����ĳ���˶�Ա���ĳ����̵�ʱ�����ڰ�Сʱ������������������ĳ�ֽ�ͨ����Υ�棻��2��ȱ���м����յ�Ĵ��������ݡ�

����˵�������������˶�Ա���������������������д��������ݣ�ÿ�д��������ݣ�������id+ �˶�Ա���+ HH MM SS��

���һ������3������****

Ĭ���ڳ����������˶�Ա���������ϴ���

Sample

input:

5 
0 100 08 00 00
0 122 08 00 00
0 132 08 00 00
0 142 08 00 01
0 152 08 00 02

1 132 08 50 46
1 152 08 49 59
1 142 08 51 10
1 122 08 52 00

2 152 09 19 58
2 142 09 34 02
2 100 09 34 05
2 122 09 35 35
2 132 09 36 00
3

output:
2
*/ 

bool time(int i,int n,int A[][5])//��ֻ�ܷ��ʵ�a*5�� 
{
	//���������ǵ�i����**,��ȥ����������һ��ʱ�������� 
	 for(int k=n;k<2*n;k++)//��һ�κ͵ڶ���
	 {
	 	if(A[i][1]==A[k][1])
	 		{
	 			if(A[i][2]==A[k][2])
	 			{
	 				int time;
	 				time=A[k][3]-A[i][3];
	 				if(time<30)
	 					return false;
				 }
				 else
				 {
				 	int time;
				 	int a;
				 	a=A[k][2]-A[i][2];
				 	time=60*a+(60-A[i][3])+A[k][3];
				 	if(time<30)
				 		return false;
				 }
			 }
	 }
	 for(int k=2*n;k<3*n;k++)//��һ�κ͵ڶ���
	 {
	 	if(A[i][1]==A[k][1])
	 		{
	 			if(A[i][2]==A[k][2])
	 			{
	 				int time;
	 				time=A[k][3]-A[i][3];
	 				if(time<30)
	 					return false;
	 				else
	 					return true;
				 }
				 else
				 {
				 	int time;
				 	int a;
				 	a=A[k][2]-A[i][2];
				 	time=60*a+(60-A[i][3])+A[k][3];
				 	if(time<30)
				 		return false;
				 	else
				 		return true;	
				 }
			 }
	 }
}

int main()
{
	int n;
	cin >> n;
	int A[5*n][5];
	int a,b;
	for(a=0;a<5*n;a++)
	{
		for(b=0;b<5;b++)
		{
			int m;
			cin >> m;
			if(m!=3)
				A[a][b]=m;
			if(m==3)
				goto L1;
		}
	}
	L1:
	//��������ˣ�������a*5�Ĵ�С�Ķ�ά���� 
	
	//step1:���ж��ж��ٸ���û���������ݣ�����ס����***
	 //���ҵ����Ƕ�������
	 int sum=0; 
	 for(int i=0;i<n;i++)
	 {
	 	int count;
	 	for(int j=n;j<3*n;j++ )
	 	{	
			count =0;
	 		if(A[i][1]==A[j][1])
	 			count++;
		 }
		 if(count!=2)//����������� 
		 	sum++;
		else
		{
			if(time(i,n,A))
				sum++;
		}
	  } 
	cout << sum;
	return 0;
}



/*
struct Node
{
	int id;
	int hao;
	int a[3];	
	Node *next;
};
*/
/* 
Node *input()
{
	int a;
	int id;
	int b[3];
	cin >> a >> id;
	for(int i=0;i<3;i++)
		cin >> b[i];
	Node *head =NULL;
	while(a!=3)
	{
		if(head==NULL)
		{
			Node *s=new Node;
			s->next=NULL;
			head=s;
			s->
		}
		else
		{
			
		}
		
	}
	
	
}
*/
