#include <iostream>
using namespace std;
/* run this program using the console pauser or add your own getch, system("pause") or input loop */
//  编程实现：从键盘输入一个字符序列（以字符‘#’结束），对其中的“>=”进行计数。
int main()
{
	cout << "请输入一个字符序列（以#结束）" << endl;
	char xulie,arr1,arr2;int i=0;
	cin  >> xulie;										//需要先输入一个xulie，来进行while的判断。
	while(xulie !='#')									//（不然如果在循环中多次输入cin，第一次的xuelie无法判断）  
	{
		arr1 = xulie;
		cin  >> xulie;
		arr2 = xulie;									//此时可以不需要再定义了，直接拿arr1和新输入的xulie判断 
		if(arr2 == '#') break;
		else if(arr1 == '>'&& arr2 == '=')				//必须输入一个arr=='#'因为整体来看只是判断了xulie==arr1是不是#的情况 
			    i++;
		cin >> xulie;									//需要再输入一个cin，和第一次的cin作用相同（进行判断+给arr1赋值） 
	}	
	cout << "这个字符序列中>=的个数为" << i << "个" << endl;
	return 0;
	
														//修改之后需要把上一个.exe文件关掉，不然运行的还是上一次的文件 
}


/*
另外一种思路：
int main()
{
	char ch; int count=0        良好的习惯，需要给每一个定义的变量进行赋值
	for(cin >> ch;ch != '#'; cin >> ch)      把所有的循环条件、初值赋值、每次循环的准备都在for的括号中完成 
		{
		if(ch =='>')						
		{cin >> ch;
		if(ch =='=')
			count ++;
		else if(ch =='#')break;}
		
		} 
	cout << "该序列中数目为"  << count ;
	return 0;
}
*/
