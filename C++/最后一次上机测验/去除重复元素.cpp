#include <iostream>
using namespace std;
/* 
��Ŀ��ȥ���ظ�Ԫ�أ���������ϰ��

��Ŀ������

�Ӽ�������n��������ȥ���ظ��󣬴�С������������

sample:

input:

10

3 4 5 6 1 2 3 4 6 5

output:

1 2 3 4 5 6
*/


/*
�뷨һ��������������ȥ���ظ�Ԫ����***���ɲ�����Ŀ��զ�������ģ���զ�������أ�Ҫ���Լ���˼����

�뷨������Ŀ����˳����ȥ�أ���������΢�鷳һ�㣬��Ҳ���������� 
*/
int main() 
{
	int n;
	cin >> n;
	int arr[n];
	for(int i=0;i<n;i++)
		cin >> arr[i];
	//step1:ȥ���ظ�Ԫ��
	for(int i=0;i<n;i++)
	{
		for(int j=i+1;j<n;j++)
		{
			if(arr[i]==arr[j])
			{
				for(int k=j;k<n-1;k++)
					{
						arr[k]=arr[k+1];
					}
				j--;//���ô�ԭ����λ�ÿ�ʼ��飬��һ�����ظ����ܵ�һ������***	
				n--;
			}	
		}	
	} 
	//step2:������������ֻ��n��Ԫ���� 
	int k=n;
	while(k>1)
	{
		int max=arr[0];
		for(int i=0;i<k;i++)//�ҵ�k��������Ԫ��
			 if(max<arr[i]) max=arr[i];
		int i; 
		for(i=0;i<k;i++)
			if(max==arr[i]) break;//����i�����Ԫ���±� 
		int temp=arr[k-1];
		arr[k-1]=arr[i];
		arr[i]=temp;
		k--;
	}
	for(int i=0;i<n;i++)
		cout <<arr[i]<<" ";
	return 0;
}
