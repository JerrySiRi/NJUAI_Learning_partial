#include <iostream>
#include <cmath>
using namespace std;
/*
题目：水仙花数（教材第三章）
题目描述：
水仙花数是指一个 3 位数，它的每个位上的数字的 3次幂之和等于它本身。
输出满足条件的水仙花数，每个数字后，输出一个空格。
*/
int main() 
{
	int a=0,b=0,c=0,d=0;
	for(a=100;a<=999;a++)
	{
	b = a/100;    //百位                     //法一：不用数组的情况 
	c = (a-b*100)/10; //十位 
	d = a-b*100-c*10; //个位 
	if(a==pow(b,3)+ pow(c,3)+pow(d,3))       //一定要小心！！！！要写两个等号的哦！！！ 
		cout << a <<" ";
	}
	return 0;
}
