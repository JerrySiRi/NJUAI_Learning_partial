#include <iostream>
using namespace std;
/* run this program using the console pauser or add your own getch, system("pause") or input loop */
/*
��֤��°ͺղ��롣�����֤2000���ڵĲ�С��4��***��ż�����ܹ��ֽ�Ϊ��������֮�͡�
��������ʱ���Ӽ�������һ��2000���ڵ���ż��������Ļ��������еķֽ����������������ʽ�����趨��ע�⽻���Ѻá�
�������Ѻ�=�������Ĳ�����ż���������������������Ŷreturn -1�� 
������ֽ⡿������������ 
�ٵ����ҳ���С�������������Щ����,�����Ա���*** 
��֮�����ҳ�����Щ������Щ���������Ե�������� 
���������ҳ�������2000֮�ڵ������������Ա���+����������һ���
*/
bool sushu(int i)//�ж�i�ǲ������� 
{
	int j=2;
	for(;j<i;j++)
	{
		if(i%j==0) return false;//bool���͵ı������true��false���ֵģ�����ֻ��true���͵� 
	}							//����bool���Ϳ϶���Ҫ�ж��ǲ���true��ѽ������һ������false�Ĵ����� 
	if(i%j!=0||i==j)
		return true;
}
int main() 
{
	
	int a;
	cout <<"������һ��2000�����Ҳ�С��4����ż��"<<endl;
	cin >>a;												//��Ҫ���������� 
	if(a<4||a>=2000||a%2!=0)
		{cout <<"�����������������"; return -1;}
	int j=0;
	for(int b=2;b<2000;b++)	
	{													//��һ�������ж�2000֮���ж��ٸ������� 
		int i=2;
		for(;i<b;i++)
		{
			if(b%i==0)break;	
		}
		if(b%i!=0||b==i)						//С��i++�Ǽӹ�һ��i֮������������ų���ѭ����
			j++;								//2000֮����303�������������Դ���j������
	}
	int	arr[j],n=0;								//�ڶ�������ʼ�����ִ浽����֮��
	for(int m=2;m<2000;m++)
	{
		if (sushu(m))
		{
			arr[n]=m;
			n++;
		}
	}
												//����������ʼ�ж���������֮�͵�����	
	for(int p=0;p<j;p++)
	{
		for(int q=0;q<=p;q++)					//Ҫ��ϸ�������pС��j�Ļ����ͻ����ظ�������� 
			{									//Ҫ����˳��ĸı� 
				if(arr[p]+arr[q]==a)
					cout <<a<<"���Էֽ�Ϊ" <<arr[p]<<"��"<< arr[q] <<"��������֮��"<<endl; 
			}
	} 				
	return 0;
}
/*
�������� 
#include <iostream>
#include <cmath>
using namespace std;
int f(int a)
{
	for (int i=2;i<=sqrt(a);i++)
	{
		if (a%i==0)							//�������ķ���***�������Լ��ĸ��Ӽ򵥵�Ŷ 
		  return -1;
	}
	return a;
}
int main ()
{
	int n;
	cin>>n;
	for (int j=2;j<=n;j++)
		for (int k=2;k<=j;k++)
		{
			if (f(j)+f(k)==n && f(j)!=-1 && f(k)!=-1)
			cout<<f(j)<<" "<<f(k);
		}
		
}
*/
