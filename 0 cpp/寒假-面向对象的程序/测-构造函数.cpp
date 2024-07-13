#include <iostream>
#include <cstring>
using namespace std;
/* run this program using the console pauser or add your own getch, system("pause") or input loop */

class A
{
	public:
		A()
		{
			a=b=0;
			strcpy(c,"aaa");
		}
		A(int x1)
		{
			a=x1;
			b=0;
			strcpy(c,"bbb");
		}
		A(const char *p)
		{
			a=b=0;
			strcpy(c,p);
			//一定是写p呢！p指向的位置是新字符串的第一个字符地址*** 
			//进而用p可以代替整个数组。 
		}
		//【理解1】[函数形参是char *p的时候会有警告的，原来char *背后的含义是：给我个字符串，我要修改它。]
		//而理论上，我们传给函数的字面常量是没法被修改的。传进来的是控制台输入的呀 
		//所以说，比较合理的办法是把参数类型修改为const char *。
		// 【理解2】 strcpy在cstring库中的第二个形参本来就是const类型的》》传入的指针也应该是const
		//不然编译器认为在strcoy之中就有可能把第二个字符串给修改啦** 
		//这个类型说背后的含义是：给我个字符串，我只要读取它。
		void print();
		
	private:
		int a,b;
		char c[10];
};

void A::print()
{
	cout << a << b << c;
}

int main() 
{
	A b[5]={A(),A(1),A("abcd"),A(2),"xyz"};
	//【所有的都写成A(。。。)把，不会报错哒】 
	for(int i=0;i<5;i++)
		{b[i].print();cout <<endl;
		}
		
	return 0;
}
