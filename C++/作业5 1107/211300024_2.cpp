#include <iostream>
#include<cmath>
#include <iomanip>
using namespace std;
/*
中位数（Median）又称中值，统计学中的专有名词，是按顺序排列的一组数据中居于中间位置的数。
如果观察值有偶数个，通常取最中间的两个数值的平均数作为中位数。
step1：键盘输入n
step2：n个整型数，输出它们的中位数。
输出要求：分两行输出
第一行先输出排序后的这n个数----冒泡法或者选择排序法！！！两种方法都用一下
第二行输出中位数。
*/
//方法一：选择排序法，最大的挪到最后，并且把最后的和前面的交换就可以 
//要把数组传给函数的呢！ 
void paixu(int arr[],int n)//排序函数+把他输出哦！选择排序法：step1找到一个最大的就把他n——，
{												//step2下次再从新数值的n开始就可以
	int max=0,a;								//把最大的下表定义成max，max在0到n-1之间的
	a=n;
	while(n>=1)									//此处n可以大于也可以大于等于1的哦！等于1的时候什么都不做而已 
	{
		max=0; 									//******错误！：每次循环之后再循环外定义的函数值都会改变的！ 
		for(int i=1;i<n;i++)					//每次一定注意要给他重新初始化一下的！！！！！！ 
		{
			if(arr[max]<arr[i])	max=i;			//开始找最大的呢,本质上是下表的运算的相互赋值的,得到最大下标是max
		}
		int temp;								//再把最大的和最后一项做交换。要有中间变量的
		temp=arr[n-1];							//值和访问数组的某一项可以相互赋值的哦！ 
		arr[n-1]=arr[max];
		arr[max]=temp;
		n--;			 
	}
												//上面一个循环把n的值改变了哦！ 
	for(int j=0;j<a;j++) 
		cout <<arr[j]<<" ";						//注意交互友好：加上空格！ 
}
int main()
{
	int n,i;
	int arr1[n]; 
	cin>>n;
	for(i=0;i<n;i++)
		cin >> arr1[i];//数组的定义一定是要在main函数之中的！ 				
	paixu(arr1,n);	//step1：输出排序后的数组！
					//step2：输出中位数，需要判断是不是偶数的！
	cout << endl;
	int c;
	c=n+1;
	if(c%2==0)
		cout <<arr1[c/2-1]; //下表是从0开始的！ 
	else
		{
			double b;               //需要注意，平均值可不一定是整数的哦 
			b=arr1[n/2-1]+arr1[n/2];//取整是向下取整的呢
			cout << b/2; 
		}
	return 0;
}
