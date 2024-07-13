#include <iostream>
#include <cmath>       //要引用平方根函数的哦 
using namespace std;
/*设计程序，验证数论中著名的“四方定理”
（一个自然数至多只要用四个整数的平方和就可以表示）。要求每输入一个自然数，输出其对应的四个数。
（结果中的四个数从大到小排列，并且从左到右每个数要尽可能地大）*/
int main() 
{
	int a,b,c,i,j,k,m;
	cin >> a;
	b=sqrt(a);c=sqrt(a/4);
	for(i=b;i>=c;i--)
	{
		for(j=i;j>=0;j--)
		{
			for(k=j;k>=0;k--)
			{
				for(m=k;m>=0;m--)
					if(a==pow(i,2)+pow(j,2)+pow(k,2)+pow(m,2))
						{cout <<i<<" "<< j <<" "<< k<<" "<<m << endl;
						return 0; 
			//如果不加return 0的话，会把所有从大到小排列的四方数全部输出！
			//程序是满足了i、j、k、m从大到小的顺序输出了，但是因为i可以取多个值》》多种四方数都输出啦！！！
			//return 0的作用就是见好就收，我只需要第一位最大的那个呢！！ 
						}
			}
		}
	}	
	return 0;
}
