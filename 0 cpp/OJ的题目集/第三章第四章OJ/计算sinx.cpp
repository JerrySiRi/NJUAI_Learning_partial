#include <iostream>
#include <cmath>
#include <iomanip>
using namespace std;
//题目描述：已知sin x可以展开为无穷级数 (-1)^n * x^(2n+1) / (2n+1)!的和，编程求解任意给定x的正弦函数值。
//输入为两个数，第一个数是x（不一定是整数）,第二个数是整数n，表示加到第n项。结果保留5位小数。
//不足五位小数的要补0，大于五位小数的直接输出就可以 
long double fenzi(long double x,long long int n)//任意值》小心溢出 .同时注意返回值应该是double类型，而不应该是int！ 
{
	//****一定要保证return出来的值和函数类型相同才可以呢！！！即return的b是long double 函数类型也得是long double
	//****函数输入值不用和函数类型相同的，但是函数返回值要和函数类型相同的呢！！！ 
	long double b=0;
	b=x;
	for(long long int i=1;i<=n;i++)
	{
			b=b*x*x;//计算x的2n+1次方，先把b给成x，每次成x的平方 
	}
	return b;
}
long double fenmu(long long int n)
{
	long double a=1;     //这时候一定要给a赋值，不然是随机值和i相乘！ 
	for(long long int i=1;i<=2*n+1;i++)
		a=i*a;
	return a;
}
int main() 
{
	long double x;
	long long int n;
	long double sum=0;//此时sum一定是要给他一个初始值=0的,后面加起来得有个基准 
	cin >> x >> n;
	for(int j =1;j<=n;j++)//i是可以从0开始的 
	{
		sum+=pow(-1,j)*fenzi(x,j)/fenmu(j);
	}
	cout << setiosflags(ios::fixed)<<setprecision(5)<< sum + x;
	return 0;
}
