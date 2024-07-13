#include <iostream>
using namespace std;
/* run this program using the console pauser or add your own getch, system("pause") or input loop */

int main()
{
	
	int a,b,c;
	cin >> a >> b >> c;
	int d;
	d=a+b+c;
	if(a+b > c && b+c > a && a+c > b)
		cout << d;
	else
		cout << "不能组成三角形";	
	return 0;
}
