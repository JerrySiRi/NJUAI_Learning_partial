#include <iostream>
using namespace std;
/*
��Ŀ��ȥ���ظ�Ԫ�أ���������ϰ��
��Ŀ������
�Ӽ�������n��������ȥ���ظ��󣬴�С������������
��һ����ȥ���ظ���Ԫ�� (����������������ظ���Ԫ��
��Ҫ�����һλ�������Ĳ��Ұ�n-1�ģ��������ǰѺ����������ǰ������һλ�أ�)
�ڶ�������С��������������Ҫһ��������أ��� 
*/
int main() 
{
	int n;
	cin >> n;
	int arr[n];
	for(int i=0;i<n;i++)
	{
		cin >> arr[i];
	}
	//�͵���n�����仯�ſ����أ� 
	for(int i=0;i<n;i++)
		{
			for(int j=i+1;j<n;j++)//j����������ط�û������ 
			{
				if(arr[i]==arr[j])
					{
						int temp=arr[n-1];
						arr[n-1]=arr[j];
						arr[j]=temp;
						n--;
					}
			}
		}
	//����n�����˱仯����ɾ�����ظ�Ԫ��
	//ѡ������
	int k=n;//���ھͲ�����n�����仯�ˣ�
	while(k>1)
	{
		int max=0;
		int i;
		for(i=0;i<k;i++)
		{
			if(arr[max]<=arr[i])
				max=i;
		}
		if(max!=n-1)
			{
			int temp=arr[k-1];
			arr[k-1]=arr[max];
			arr[max]=temp;
			}
			k--;
	}
	for(int i=0;i<n;i++)
		cout << arr[i] << " ";
	return 0;
}
