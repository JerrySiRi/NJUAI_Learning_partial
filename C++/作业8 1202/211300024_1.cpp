#include <iostream>
#include <cmath>
using namespace std;
/*
输出一个正整数的每位数字，数字之间用空格分隔。
例如：输入12345    
输出：1 2 3 4 5

大概思路：
1、得新弄出来一个函数（main之外的）在这个函数中不断进行递归
***最后只返回一个东西的（这道题最后返回的应该是一个整形数，可以用void，在函数体之中进行cout）
***或者用int作为函数的返回值类型（应该不行，int只能返回一个没有空格的数字的）
***必须得有一个变量让他不断趋近于结束递归的条件，本道题的结束递归条件只能是位数啊！
》》在函数形式参数之中必须有两个形参（一个是数字本身，一个是位数） 
*/
void single(int a,int b)
{
	if(b==1)   //一开始的错误原因：int k=a;了但殊不知a在每次调用的时候会变，那么k也会在每次被重复赋值的！ 
		cout << a << " ";
	else
	{
		int c = a/pow(10,b-1);
		cout << c << " ";
		a = a-c*pow(10,b-1);
		single(a,b-1);
	} 
}

int main() 
{
	double a;
	int i;
	cin >> a;
	int k=a;
	for(i=1;i<a;i++)//第一步：计算a的位数是多少 
	{
		if((a/10)>1)  
			a=a/10;//错误2：得在循环之中不断改变a的值呀！ 
		else
			break;
	}
	single(k,i);//错误3：在循环中，a的值也被改变了！ 
	return 0;
}
