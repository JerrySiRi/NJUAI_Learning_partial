#include <iostream>
#include <cstring>
using namespace std;
/*
题目：删除子串

题目描述：

编程实现（用字符数组实现，不能用string类）：
输入两个字符串A,B。
1如果A中包含B，[检查子串]从A中剔除B，输出不包含B的结果；
2如果A中没有包含B，输出A。
说明：（1）两个字符串不包含空白符。（2）最终结果中不包含B。

输入说明：在一行中输入A,B两个字符串，A和B之间用空格分隔。

输出说明：输出剔除后的字符串


Sample:

input:

abcdabcd abc

output:

dd

其中一个样例：
bbcc bc 
*/
int main()
{
	char ch1[100],ch2[100];
	cin >>ch1;
	cin >>ch2;
	int a=strlen(ch1);
	int b=strlen(ch2);
	for(int i=0;i<=a-b;i++)	
	{
		bool huan=false;
		if(ch1[i]==ch2[0])
		{
			int j;
			for(j=1;j<b;j++)
			{
				if(ch1[i+j]==ch2[j])	
					;
				else break;
			}
			//出循环两种可能，第一种j=b出来，就是找到了子串了。第二种没有找到，j不等于b 
			if(j==b)//此时i是下标了！
			{
				huan=true;
						//主串的下标储存在ch3中了 
						//想法一：储存下标
						//想法二：直接进行删除操作,采用覆盖的方法，而不是移到最后一个位置
				for(int p=i;p<=a-b;p++)
				{
					ch1[p]=ch1[p+b];
				}
				a=a-b;
				if(a==0)
					ch1[0]='\0';
			}
		}
		if(huan)
			i=-1;
	}
	cout <<ch1;
	return 0;
}
/*
错误：
①重载 
*/
