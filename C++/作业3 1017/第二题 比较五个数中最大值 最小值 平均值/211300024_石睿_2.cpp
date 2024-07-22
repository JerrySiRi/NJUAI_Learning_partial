#include <iostream>
#include<iomanip>
using namespace std; 
/* run this program using the console pauser or add your own getch, system("pause") or input loop */
int main() 
{
	int number[5],i;//题目含义是一次性输入五个数字，就需要编号啦。如果一次一次输入的话就不需要编号，输一次比一次就可以啦 
	cout << "请输入5个整数" << endl;
	for(i=0;i <= 4;i++)//给数组进行编号是从0开始的，下标从0开始 
	{
		cin >> number[i]; //给这五个数进行编号 
	}
	int ma,mi;
	double a;
	ma=number[0];
	mi=number[0];
	for(i=0;i<=4;i++)
	{
		if(number[i]>ma)
			ma = number[i];
		if(number[i]<mi)
			mi = number[i];
	 	a += number[i];
	 } 
	 double c;
	 c = a/5;
	 cout << "五个整数中最大值是" << ma << endl;
	 cout << "五个整数中最小值是" << mi << endl;
	 cout << setiosflags(ios::fixed)<<setprecision(2);
	 cout << "五个数的平均值是" << c;
	return 0;
}
