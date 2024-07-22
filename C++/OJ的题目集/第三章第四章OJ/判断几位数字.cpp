#include <iostream>
using namespace std;
/* run this program using the console pauser or add your own getch, system("pause") or input loop */
//输入一个正整数，判断该整数为几位数，输出其位数。
int main() 
{
	int a,b,i;
	cin >> a;
	while(a/b >=10)
		{
			b *=10;	
			i++;
		}
	cout << i;
	return 0;
}
