#include <iostream>
#include<cmath>
#include <iomanip>
using namespace std;
/*
��дһ������double func( int a, int n) ���ú������ڼ��������ʽ�ӵĺͣ�a+aa+aaa+...+ aa..a(n��a) ����Ҫ�õ�ѭ���ģ�����main�������ж��壬��main�����е���func������ע��,a�ķ�Χ��1-9����Ҫ���ǲ����Ϸ�Χ����Ĵ���
�����ϵ����������Щ�أ�
a������û����1-9֮�У� 
n�������һ�������� 
*/
double func(int a,int n)
{
	int i,b;
	double sum;
	for(i=1;i<=n;i++)
	{
		b*=a;//�������i��a����ˣ��Ͳ������������ 
		sum+=b;
	}
	return sum;//ע�⣡Ҫ�������ֵ�ͺ���������ȵ� 
}
int main()
{
	int a,b; 
	cin >> a>>b;
	if(a<1||a>9||b<=0)
		{cout <<"��������";return -1;
		}
	else
		cout << func(a,b);
	return 0;
}
