#include <iostream>
using namespace std;
/* 
���������������������󣬷ֱ�Ϊn1��n2�У�n2��n3�У������������ĳ˻���

�����ʽ
��һ��Ϊ��������n1,n2,n3��������1000�� �ո�ָ���
������n1�У�ÿ��n2��Ԫ�أ��ո�ָ��������һ�������Ԫ��
������n2�У�ÿ��n3��Ԫ�أ��ո�ָ�������ڶ��������Ԫ��
�����ʽ��
���n1�У�ÿ��n3��Ԫ�أ��ո�ָ�
����������
2 3 2

1 2 3
4 5 6

-1 3
4 9
11 3
���������
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
	for(int i=0;i<n1;i++)//��ȷ������i��j 
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
		cout << endl;//һ��Ҫע�⣬ÿ�����֮��һ��Ҫ�����أ��������Զ����㻻�еģ� 
	}
	return 0;
}
