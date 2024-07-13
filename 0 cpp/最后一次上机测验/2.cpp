#include <iostream>
using namespace std;
/*
学校举办迷你马拉松，为了保证运动公平，每位选手佩戴的手环中有一个RFID标签
在经过传感器时，计算机会将记录传感器id、选手的号码及经过传感器的时间（时间采用24小时格式：HH MM SS）上传到服务器中。
本次运动一共有3个传感器，分别在在出发点、中间点和终点，对应的传感器id分别为0，1，2。
分析传感器的数据，输出有多少运动员违规。违规的判断：（1）如果某个运动员完成某个半程的时间少于半小时，则判他可能利用了某种交通工具违规；（2）缺少中间点或终点的传感器数据。

输入说明：首先输入运动员的人数，接着输入若干行传感器数据，每行传感器数据：传感器id+ 运动员编号+ HH MM SS，

最后一行输入3结束。****

默认在出发点所有运动员均有数据上传。

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

bool time(int i,int n,int A[][5])//但只能访问到a*5的 
{
	//传进来的是第i个人**,先去查找他的下一次时间在哪里 
	 for(int k=n;k<2*n;k++)//第一次和第二次
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
	 for(int k=2*n;k<3*n;k++)//第一次和第二次
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
	//输入完成了，现在是a*5的大小的二维数组 
	
	//step1:先判断有多少个人没有三个数据，并记住他们***
	 //先找到他们都在哪行
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
		 if(count!=2)//这个人有问题 
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
