#include <iostream>
using namespace std;
/*
题目：去除重复元素（第五章练习）
题目描述：
从键盘输入n个整数，去除重复后，从小到大输出结果。
第一步：去掉重复的元素 (方法：如果遇到了重复的元素
需要和最后一位作交换的并且把n-1的，本质上是把后面的数字往前都移了一位呢！)
第二步：从小到大输出结果（需要一步排序的呢！） 
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
	//就得让n发生变化才可以呢！ 
	for(int i=0;i<n;i++)
		{
			for(int j=i+1;j<n;j++)//j定义在这个地方没有问题 
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
	//现在n发生了变化，且删除了重复元素
	//选择排序法
	int k=n;//现在就不能让n发生变化了！
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
