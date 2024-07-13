#include <iostream>
using namespace std;
#include <ctime>
#include <cstdlib>
/*
猜数游戏：程序随机产生一个正整数，用户进行猜测。
step1：根据输入的数字，程序反馈：猜大了or猜小了
step2：用户猜中之后**，程序询问用户是否进行下一轮，用户可以选择继续下一轮游戏，也可以直接退出游戏 
*/
int main()
{
	L: 
//生成随机数字x 
	int x=rand();
	cout <<"请您输入一个数字";
	int a;
	cin >>a; 
	while(a!=x)
	{
		if(a>x)
			cout <<"猜大喽，再小一点试试看";
		else if(a<x)
			cout << "猜小喽，再大一点试试看";
		cin >> a;
	}
	cout <<"恭喜你猜对啦！。如果您想再玩一次请输入1.不想玩输入0";
	int b;
	A:
	cin >>b;
	while(b==0||b==1)
	{
	if(b==1)
		goto L;
	if(b==0)
		return 0;
	}
	cout << "您输入错误了哦，您再输入一遍哦";
	goto A;
	return 0;
}
