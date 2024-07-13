#include <iostream>
using namespace std;
/*
题目描述：
输入一个N*N（N不超过10）的矩阵，矩阵元素为整型，将矩阵元素按顺时针方向旋转90度。输出旋转后的结果。
输入说明，先输入N的值，再输入N行N列矩阵的元素。
Sample:
input:
3

1 2 3
1 2 3
1 2 3

output:
1 1 1
2 2 2
3 3 3
思路：只需要改变输出循序就可以啦
原本：把这个矩阵旋转，输出从第一行第一个元素开始输出
现在：以矩阵为参考系（矩阵不动），从第一列最后一个元素开始输出！ 
*/

int main() 
{
	int n;
	cin >> n;
	int A[n][n];
	for(int i=0;i<n;i++)
	{
		for(int j=0;j<n;j++)
			cin >> A[i][j];
	} 
	
	for(int j=0;j<n;j++)
	{
		for(int i=n-1;i>=0;i--)
			cout << A[i][j] << " ";
		cout << endl;
	}

	return 0;
}
