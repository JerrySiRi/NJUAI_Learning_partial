#include <iostream>
using namespace std;
/*
题目：母牛计算问题（教材第四章习题）
题目描述：
若一头小母牛，从出生起第四个年开始每年生一头母牛，假定母牛全部存活，按此规律，第n年有多少头母牛。输入n，输出第n年的母牛数量。
Sample
Input:
8
Output:
9
要弄清问题是什么呢：第几个年头是这整个一年都算这个年头的！
所以第七年的时候第四年出生的小牛也可以生小牛啦！
所以第n年小牛的数量=n-1年小牛的数量+n-3年小牛数量的加和！（n-3年生的小牛在第n年都可以继续生啦） 
*/
int main()
{
	int n;
	cin >>n;
	int arr[n];
	arr[0]=1;
	arr[1]=1;
	arr[2]=1;
	for(int i=n;i>=3;i--)
	{
		arr[i]=arr[i-1]+arr[i-3];
	}
	cout << arr[n-1];
	return 0;
} 
