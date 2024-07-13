#include<iostream>
using namespace std;
/*
计算从结点1到结点n共有多少条不同路径。输入n，输出路径数。
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
		if((i+1)%2!=0)//说明i是奇数
			arr[i]=arr[i-1]+arr[i-2];
		else                           
			arr[i]=arr[i-1]+arr[i-2]+arr[i-3]; 
	}	
	/*
	尤其需要小心：这类循环只能从小往大去做。要保证赋值的时候都有定义才可以的！ 
	*/
	cout <<arr[n-1];
	return 0;
}
