#include<iostream>
using namespace std;
/*
����ӽ��1�����n���ж�������ͬ·��������n�����·������
*/
int main()
{
	int n;
	cin >>n;
	int arr[n];
	arr[0]=1;
	arr[1]=1;
	arr[2]=2;
	for(int i=3;i<n;i++)
	{
		if((i+1)%2!=0)//˵��i������
			arr[i]=arr[i-1]+arr[i-2];
		else                           
			arr[i]=arr[i-1]+arr[i-2]+arr[i-3]; 
	}	
	/*
	������ҪС�ģ�����ѭ��ֻ�ܴ�С����ȥ����Ҫ��֤��ֵ��ʱ���ж���ſ��Եģ� 
	*/
	cout <<arr[n-1];
	return 0;
}
