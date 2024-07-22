#include <iostream>
using namespace std;
/*题目描述：写一个竞猜游戏，让用户猜一个神秘数字（事先初始化为2021）。
在每次猜完后程序会告诉用户他猜的数是大了（输出”too big“）还是小了（输出“too small”），直到猜测正确，
输出猜测的总次数(需要计数器),程序结束。如果用户连续猜测同一个数字，则只算一次。
记住上一次输出的数据****（需要添加一个if语句） 
注：每条输出应占一行。为防止EOF的问题，我们固定输入个数为十个数字。
（用户一定可以在10次之内猜对问题,且用户一次性输完，不在过程中得到任何信息）*/
int main() 
{
	int a=2021,b,c,i=0;                    
	for(cin>>b;b!=a;)
	{
		if(b<a)
			cout << "too small" << endl;
		else if (b>a)
			cout << "too big" << endl;
		else break; 
		c=b;              //记住上一个输入的数字是几 
		cin >> b;
		i++;
		if(c==b)
			i--;
	}			
	cout << i+1;
	return 0;
}


