#include <iostream>
#include <cmath>
#include <iomanip>
using namespace std;
//��Ŀ��������֪sin x����չ��Ϊ����� (-1)^n * x^(2n+1) / (2n+1)!�ĺͣ��������������x�����Һ���ֵ��
//����Ϊ����������һ������x����һ����������,�ڶ�����������n����ʾ�ӵ���n��������5λС����
//������λС����Ҫ��0��������λС����ֱ������Ϳ��� 
long double fenzi(long double x,long long int n)//����ֵ��С����� .ͬʱע�ⷵ��ֵӦ����double���ͣ�����Ӧ����int�� 
{
	//****һ��Ҫ��֤return������ֵ�ͺ���������ͬ�ſ����أ�������return��b��long double ��������Ҳ����long double
	//****��������ֵ���úͺ���������ͬ�ģ����Ǻ�������ֵҪ�ͺ���������ͬ���أ����� 
	long double b=0;
	b=x;
	for(long long int i=1;i<=n;i++)
	{
			b=b*x*x;//����x��2n+1�η����Ȱ�b����x��ÿ�γ�x��ƽ�� 
	}
	return b;
}
long double fenmu(long long int n)
{
	long double a=1;     //��ʱ��һ��Ҫ��a��ֵ����Ȼ�����ֵ��i��ˣ� 
	for(long long int i=1;i<=2*n+1;i++)
		a=i*a;
	return a;
}
int main() 
{
	long double x;
	long long int n;
	long double sum=0;//��ʱsumһ����Ҫ����һ����ʼֵ=0��,������������и���׼ 
	cin >> x >> n;
	for(int j =1;j<=n;j++)//i�ǿ��Դ�0��ʼ�� 
	{
		sum+=pow(-1,j)*fenzi(x,j)/fenmu(j);
	}
	cout << setiosflags(ios::fixed)<<setprecision(5)<< sum + x;
	return 0;
}
