#include <iostream>
using namespace std; 
/* run this program using the console pauser or add your own getch, system("pause") or input loop */
int main()
{
	int i,j;
	cin >> i >> j;
	int a;
	a=i/j;
	if(i%j==0)
		cout << a;
	else
		cout << "不可以整除";
	return 0;
}
