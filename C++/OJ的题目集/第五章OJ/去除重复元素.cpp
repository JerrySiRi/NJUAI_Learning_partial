#include <iostream>
using namespace std;
/*
��Ŀ��ȥ���ظ�Ԫ�أ���������ϰ��
��Ŀ������
�Ӽ�������n��������ȥ���ظ��󣬴�С������������
��һ����ȥ���ظ���Ԫ�� (����������������ظ���Ԫ��
��Ҫ�����һλ�������Ĳ��Ұ�n-1�ģ��������ǰѺ����������ǰ������һλ�أ�)
�ڶ�������С��������������Ҫһ��������أ��� 
sample:
input:
10
3 4 5 6 1 2 3 4 6 5
output:
1 2 3 4 5 6
*/
int main()
{
	int n;
	cin >> n;
	int arr[n];	
	for(int i=0;i<n;i++)
		cin >> arr[i];
	for(int i=0;i<n;i++)//���n����ʱ�ڱ仯�ģ�����Ҫ��ֵn=n-1 
	{
		for(int j=i+1;j<n;j++)
		{
			if(arr[i]==arr[j])
				{
					for(;j<n-1;j++)
						arr[j]=arr[j+1];
					n--;	 
				}
		}
	}//����������ɾ���ظ�Ԫ���� ,Ŀǰ������֮��ֻ��n��Ԫ���ˣ�n�Ѿ������ı���
	int k=n;
	while(n>1)
	{	
		int max=0;
		int i;
		for(i=0;i<n;i++)
		{
			if(arr[max]<arr[i])
				max=i;//ǰn��������±���max�� 
		} 
		int temp=arr[n-1];
		arr[n-1]=arr[i];              
		arr[i]=temp;
		n--;//��������ˣ� 
	}
	
	for(int i=0;i<k;i++)
		cout<<arr[i]<<" ";
	return 0;
 } 
 
 
 /*
 .hд����main����֮���õ��˺��� ������
 .cpp������һ��cpp�� ��ɺ��������� 
 ����������Ҫinclude�ˣ� 
 .cpp��ɵ��Ǻ������ʵ�֣�ֻ��Ҫ����mystring.h�Ϳ�����***�� 
*/
