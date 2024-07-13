#include<iostream>
using namespace std;
/* run this program using the console pauser or add your own getch, system("pause") or input loop */ 
//编程实现：对于输入的一个算术表达式（以字符'#'结束），检查其圆括号配对情况，根据是否配对，输出：配对、不配对。
/*
分析：
①配对意味着 （ 和 ）的个数相等。不管是((()))还是()()()()....
②配对也意味着( 和 ）的相对位置不能改变。即    1、先出现 ) 2、完成一对配对之后先出现 ) 
  可以让上面两种情况归为一种，即在一对括号配对之后进行结果的重置（恢复初始状态） 
*/ 
int main()
{
	cout << "请输入一个以#结束的算术表达式" << endl; 
	int a;                            //最好给附上初始值，以免出现出现随机值的现象。 
	char ch;
	for(cin>>ch;ch!='#';cin>>ch)	  //for也可以运用于未知循环次数的情况（循环体中有多层if嵌套的情况下让循环条件、准备工作） 
		{if(ch=='(')				  //在for的括号之中都体现出来，这样就会更清楚了 
			a++;
		else if(ch==')')				
			a--;
		if(a<0)
			{cout <<"不配对";return 0;}//只要以小于0了，就立即结束 
		}
	if(a==0)
		cout<<"配对";
	else
		cout<<"不配对";
	return 0;
}
