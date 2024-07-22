#include <iostream>
using namespace std;
/* 
题目：去除重复元素（第五章练习）

题目描述：

从键盘输入n个整数，去除重复后，从小到大输出结果。

sample:

input:

10

3 4 5 6 1 2 3 4 6 5

output:

1 2 3 4 5 6
*/


/*
想法一：可以先排序，再去除重复元素呢***【可不能题目是咋样描述的，睿睿就咋样做的呢，要有自己的思考】

想法二：题目描述顺序，先去重，再排序（略微麻烦一点，但也可以做啦） 
*/
int main() 
{
	int n;
	cin >> n;
	int arr[n];
	for(int i=0;i<n;i++)
		cin >> arr[i];
	//step1:去除重复元素
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
				j--;//还得从原来的位置开始检查，万一两个重复的跑到一起了呢***	
				n--;
			}	
		}	
	} 
	//step2:排序，现在数组只有n个元素啦 
	int k=n;
	while(k>1)
	{
		int max=arr[0];
		for(int i=0;i<k;i++)//找到k个中最大的元素
			 if(max<arr[i]) max=arr[i];
		int i; 
		for(i=0;i<k;i++)
			if(max==arr[i]) break;//现在i是最大元素下标 
		int temp=arr[k-1];
		arr[k-1]=arr[i];
		arr[i]=temp;
		k--;
	}
	for(int i=0;i<n;i++)
		cout <<arr[i]<<" ";
	return 0;
}
