#include <iostream>
using namespace std;
/*
��ת��˾���ʹ�����20����˾����˾��Ʒ����������ʾ�����ʹ��ϵ���˾Ʒ�ֿ������ظ��ġ�
�˿������ѡ��10�̡���˿������ѡ�����˾Ʒ�����Ƕ��١�

����˵������һ������20������������֮���ÿո�ָ�

���˵������������ѡ�񵽵�Ʒ������

sample

input:

1 1 2 2 3 3 4 4 4 4 5 5 5 1 2 3 4 9 8 10

output:

8
*/
int main()
{
	int a[20];
	for(int i=0;i<20;i++)
	{
		cin >> a[i];
	}
	//�͵���k�����仯�ſ����أ�
	int n=20;
	int i,j;
	for(i=0;i<n-1;i++)
	{
		for(j=i+1;j<n;j++)
		{
			if(a[i]==a[j])
			{
				for(int k=j;k<n-1;k++)
				{
					a[k]=a[k+1];
				}
				j--;
				n--;
			}
		}
	}
		//����k��ȥ�����ظ�Ԫ�غ�ĸ����� 
		if(n>=10)
			cout <<"10";
		else
		cout <<n; 
	return 0;
}
/*
��������
�����һλ����һλԪ����ͬ����ô��������Ԫ����ǰƽ��һλ�����ѵ�jλ��Ԫ�ظ������� 
#include <iostream>
#include <cstring>
#include <iomanip>
using namespace std;
int main()
{
	int n,i,j;
	int a[100];
	cin>>n;
	for(i=0;i<n;i++)
	{
		cin>>a[i];
	}
	for(i=0;i<n-1;i++)
	{
		for(j=i+1;j<n;j++)
		{
			if(a[i]==a[j])
			{
				for(int k=j;k<n-1;k++)
				{
					a[k]=a[k+1];
				}
				j--;
				n--;
			}
	}
	}
	for(i=0;i<n;i++){
		cout<<a[i]<<" ";
	}
	return 0;
}

*/

/* 
������룺 
	for(int i=0;i<k;i++)
		{
			for(int j=i+1;j<k;j++)//j����������ط�û������ 
			{
				if(arr[i]==arr[j])//����ԭ�򣺻���֮���п�����һ�����أ����� 
					{
						if(arr[j]==arr[k-1])
							{
								if(j!=k-1)
								{
								k--;
								while(arr[k-1]==arr[j]&&(j!=k-1))
								{
									k--;
								}
								int temp=arr[k-1];
								arr[k-1]=arr[j];
								arr[j]=temp;
								k--;
								}
							}
						else
						{
						int temp=arr[k-1];
						arr[k-1]=arr[j];
						arr[j]=temp;
						k--;
						}
					}
			}
		}

*/
