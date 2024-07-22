#include <iostream>
using namespace std;
/* run this program using the console pauser or add your own getch, system("pause") or input loop */
int main()
{
	cout << "请输入包裹重量（单位为克）和邮寄距离（单位为千米）" << endl;
	int weight,distance,price,a,b,c;
	cin >> weight,distance;
	if(weight<=15) 
		cout << "收费数额为" << "5";
	else if(15<weight&&weight<=30)
		cout << "收费数额为" << "9";
	else if(30<weight&&weight<=45)
		cout << "收费数额为" << "12";
	else if(45<weight&&weight<=60)
		{a=distance%1000;
		price=14+a; 
		cout << "收费数额为" << price;
		} 
	else 
		{
		b=distance%1000;
		price=15+2*b; 
		cout << "收费数额为" << price;
		}
	return 0;
}
