#include <iostream>
using namespace std;
/* run this program using the console pauser or add your own getch, system("pause") or input loop */
int main()
{
	cout << "�����������������λΪ�ˣ����ʼľ��루��λΪǧ�ף�" << endl;
	int weight,distance,price,a,b,c;
	cin >> weight,distance;
	if(weight<=15) 
		cout << "�շ�����Ϊ" << "5";
	else if(15<weight&&weight<=30)
		cout << "�շ�����Ϊ" << "9";
	else if(30<weight&&weight<=45)
		cout << "�շ�����Ϊ" << "12";
	else if(45<weight&&weight<=60)
		{a=distance%1000;
		price=14+a; 
		cout << "�շ�����Ϊ" << price;
		} 
	else 
		{
		b=distance%1000;
		price=15+2*b; 
		cout << "�շ�����Ϊ" << price;
		}
	return 0;
}
