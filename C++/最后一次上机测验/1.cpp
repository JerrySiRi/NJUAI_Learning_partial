#include <iostream>
using namespace std;
/*
输入两个N*N矩阵A和B，矩阵中的元素为整型。判断B是否为A的逆矩阵。逆矩阵说明：如果A*B=I ,I为单位矩阵，则B是A的逆矩阵。

单位矩阵是：主对角线上的元素为1，其他元素为0。

输入说明：先输入N，然后输入2个N*N的矩阵。

输出说明：是逆矩阵，输出“yes”，否则，输出“no”。

sample:

input:

2
1 2
-1 -3
3 2
-1 -1
*/
int main()
{
	int n;
	cin >> n;
	int A[n][n];
	int B[n][n];
	int c[n][n];
	for(int i=0;i<n;i++)
	{
		for(int j=0;j<n;j++)
			cin >> A[i][j];
	}
		for(int i=0;i<n;i++)
	{
		for(int j=0;j<n;j++)
			cin >> B[i][j];
	}
	for(int i=0;i<n;i++)
	{
		for(int j=0;j<n;j++)
			{
				int sum=0;
				for(int k=0;k<n;k++)
					sum+=A[i][k]*B[k][j];
				c[i][j]=sum;
			}
	}
	
	
	int a; 
	for(a=0;a<n;a++)
	{
		int b;int d;
		for(b=a+1;b<n;b++)
		{
			if(c[a][a]==1&&c[a][b]==0);
			else break;
		}
		if(c[a][a]!=1)
			{cout << "no"; return 0;
			}
		if(b==n)
		{
			for(d=0;d<a;d++)
				{
					if(c[a][d]==0) ;
					else break;
				}		
		
		if(d!=a) 
		{cout << "no"; return 0;}
		
		}
		else
			{cout << "no";return 0;	}

	}
	
	if(a==n)
		cout <<"yes";
	else
		cout << "no";

	return 0;
}
