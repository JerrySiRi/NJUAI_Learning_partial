#include <iostream>
using namespace std;
/*
题目：去除重复元素（第五章练习）
题目描述：
从键盘输入n个整数，去除重复后，从小到大输出结果。
第一步：去掉重复的元素 (方法：如果遇到了重复的元素
需要和最后一位作交换的并且把n-1的，本质上是把后面的数字往前都移了一位呢！)
第二步：从小到大输出结果（需要一步排序的呢！） 
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
	for(int i=0;i<n;i++)//这个n是随时在变化的，所以要赋值n=n-1 
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
	}//完成了数组的删除重复元素了 ,目前在数组之中只有n个元素了，n已经发生改变了
	int k=n;
	while(n>1)
	{	
		int max=0;
		int i;
		for(i=0;i<n;i++)
		{
			if(arr[max]<arr[i])
				max=i;//前n项的最大的下表是max啦 
		} 
		int temp=arr[n-1];
		arr[n-1]=arr[i];              
		arr[i]=temp;
		n--;//完成排序了！ 
	}
	
	for(int i=0;i<k;i++)
		cout<<arr[i]<<" ";
	return 0;
 } 
 
 
 /*
 .h写到了main函数之中用到了函数 的声明
 .cpp（另外一个cpp） 完成函数体的设计 
 这两个不需要include了！ 
 .cpp完成的是函数体的实现（只需要引用mystring.h就可以啦***） 
*/
