#include <iostream>
using namespace std;
/* run this program using the console pauser or add your own getch, system("pause") or input loop */
/*编程输出小于n的所有素数
思路：可以尝试用一用函数，把这个程序分解成两个部分。
①如果他是素数，把它输出（i<n的其中一个数字i）
②用循环把这个i++直到n哦 
*/ 
	//函数的定义 函数的定义一定要定义在main函数的外边的哦！！！！ 
	bool is_su(int a)        
	{
	int i;
	for(i=2;i <= a;i++)
	{
		if(a%i == 0) break;
	}
	if(a==2 || i==a)		//如果是素数，就返回a，如果不是素数，就什么都不返回  
		return 1;
	else
		return 0;             
	}                 		//定义一个判断这个是不是素数的函数出来，如果是素数，输出素数，如果不是素数，什么都不输出
	//函数调用 （在前面定义的不需要声明一下） 
	int main()
{
	cout << "请输入一个整数，来计算所有小于它的素数都有哪些" << endl;
	int n,j;
	cin >> n;
	for(j=2;j<n;j++)
	{if(is_su(j))
		cout << j << endl;		//函数值不可以直接输出！！！ 
	}
	return 0;
}


/*
问题解决： 
1、如果是有返回值的函数，如果调用，他必须是要出来一个数值的！如果这个数值不满足输出条件，他就会找一个最近的值来输出，他一定是要输出的
2、解决办法：
①可以用bool类型的函数，最后在if处判断一下，如果成立，再输出》》这样就不会每一个数值都直接输出啦！！！
②可以用void类型的函数，满足条件再输出！！！
void su(int a)
{
	.....
	最后再打上cout就可以啦！这样就保证不会每输入一个值他都返回啦！ 
} 
*/
