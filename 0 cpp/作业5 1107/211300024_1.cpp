#include <iostream>
#include<cmath>
#include <iomanip>
using namespace std;
/*
编写一个函数double func( int a, int n) ，该函数用于计算下面的式子的和：a+aa+aaa+...+ aa..a(n个a) （需要用到循环的！）。main函数自行定义，在main函数中调用func函数。注意,a的范围是1-9，需要考虑不符合范围输入的处理。
不符合的情况都有哪些呢？
a的输入没有在1-9之中！ 
n输入的是一个负数！ 
*/
double func(int a,int n)
{
	int i,b;
	double sum;
	for(i=1;i<=n;i++)
	{
		b*=a;//算出来了i个a相乘了，就差把他加起来啦 
		sum+=b;
	}
	return sum;//注意！要保持输出值和函数类型相等的 
}
int main()
{
	int a,b; 
	cin >> a>>b;
	if(a<1||a>9||b<=0)
		{cout <<"输入有误";return -1;
		}
	else
		cout << func(a,b);
	return 0;
}
