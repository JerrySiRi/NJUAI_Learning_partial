#include <iostream>
using namespace std;
/*
旋转寿司传送带上有20盘寿司，寿司的品种用整数表示，传送带上的寿司品种可能有重复的。
顾客最多能选择10盘。求顾客最多能选择的寿司品种数是多少。

输入说明：在一行输入20个整数，整数之间用空格分隔

输出说明：输出最多能选择到的品种数量

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
	//就得让k发生变化才可以呢！
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
		//现在k是去除了重复元素后的个数啦 
		if(n>=10)
			cout <<"10";
		else
		cout <<n; 
	return 0;
}
/*
方法二：
如果这一位和下一位元素相同，那么后面所有元素往前平移一位，即把第j位的元素给覆盖了 
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
错误代码： 
	for(int i=0;i<k;i++)
		{
			for(int j=i+1;j<k;j++)//j定义在这个地方没有问题 
			{
				if(arr[i]==arr[j])//错误原因：换完之后还有可能是一样的呢！！！ 
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
