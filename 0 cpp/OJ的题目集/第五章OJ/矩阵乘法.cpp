#include <iostream>
using namespace std;
/* 
问题描述：输入两个矩阵，分别为n1行n2列，n2行n3列，输出两个矩阵的乘积。

输入格式
第一行为三个整数n1,n2,n3（不超过1000） 空格分隔，
接下来n1行，每行n2个元素，空格分隔，代表第一个矩阵的元素
接下来n2行，每行n3个元素，空格分隔，代表第二个矩阵的元素
输出格式：
输出n1行，每行n3个元素，空格分隔
输入样例：
2 3 2

1 2 3
4 5 6

-1 3
4 9
11 3
输出样例：
40 30
82 75
*/

int main() 
{
	int n1,n2,n3;
	cin >> n1 >> n2 >> n3;
	int A[n1][n2],B[n2][n3];
	int C[n1][n3];
	for(int i=0;i<n1;i++)
	{
		for(int j=0;j<n2;j++)
			cin >> A[i][j];
	}
	for(int i=0;i<n2;i++)
	{
		for(int j=0;j<n3;j++)
			cin >> B[i][j];
	}
	for(int i=0;i<n1;i++)//先确定下来i和j 
	{
		for(int j=0;j<n3;j++)
		{
			int sum=0;
			for(int k=0;k<n2;k++)
				sum +=A[i][k]*B[k][j];
			C[i][j]=sum;
		}
	}
	for(int i=0;i<n1;i++)
	{
		for(int j=0;j<n3;j++)
			cout << C[i][j] << " ";
		cout << endl;//一定要注意，每行输出之后一定要换行呢，他不会自动给你换行的！ 
	}
	return 0;
}
