#include <iostream>
using namespace std;
//输入三个整数，输出其中最大的数。
int main() 
{
	int a,b,i=1;
	for(cin >> a;i<=2;i++;)
		{
			cin >> b;
			if(b>=a)
				a=b;		
		}
	cout << a;
	return 0;
}
/*
一定自己把流程过一遍。
①最大的值应该是谁，是把谁赋给了谁呢！把b赋给a
②每次更新的哪一个变量？输入值和每次更新的变量肯定不能是一个的呀！
b每次都在变，a每次是最大的才会被赋予新的值
③i的值每次都在变，是小于等于3还是小于等于2.是这一遍i++还是下一次开始才加的！ 
 
