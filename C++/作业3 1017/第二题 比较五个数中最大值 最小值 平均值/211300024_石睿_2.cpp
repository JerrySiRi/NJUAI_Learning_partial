#include <iostream>
#include<iomanip>
using namespace std; 
/* run this program using the console pauser or add your own getch, system("pause") or input loop */
int main() 
{
	int number[5],i;//��Ŀ������һ��������������֣�����Ҫ����������һ��һ������Ļ��Ͳ���Ҫ��ţ���һ�α�һ�ξͿ����� 
	cout << "������5������" << endl;
	for(i=0;i <= 4;i++)//��������б���Ǵ�0��ʼ�ģ��±��0��ʼ 
	{
		cin >> number[i]; //������������б�� 
	}
	int ma,mi;
	double a;
	ma=number[0];
	mi=number[0];
	for(i=0;i<=4;i++)
	{
		if(number[i]>ma)
			ma = number[i];
		if(number[i]<mi)
			mi = number[i];
	 	a += number[i];
	 } 
	 double c;
	 c = a/5;
	 cout << "������������ֵ��" << ma << endl;
	 cout << "�����������Сֵ��" << mi << endl;
	 cout << setiosflags(ios::fixed)<<setprecision(2);
	 cout << "�������ƽ��ֵ��" << c;
	return 0;
}
