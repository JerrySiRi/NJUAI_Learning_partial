#include <iostream>
using namespace std;
#include <ctime>
#include <cstdlib>
/*
������Ϸ�������������һ�����������û����в²⡣
step1��������������֣����������´���or��С��
step2���û�����֮��**������ѯ���û��Ƿ������һ�֣��û�����ѡ�������һ����Ϸ��Ҳ����ֱ���˳���Ϸ 
*/
int main()
{
	L: 
//�����������x 
	int x=rand();
	cout <<"��������һ������";
	int a;
	cin >>a; 
	while(a!=x)
	{
		if(a>x)
			cout <<"�´�ඣ���Сһ�����Կ�";
		else if(a<x)
			cout << "��Сඣ��ٴ�һ�����Կ�";
		cin >> a;
	}
	cout <<"��ϲ��¶������������������һ��������1.����������0";
	int b;
	A:
	cin >>b;
	while(b==0||b==1)
	{
	if(b==1)
		goto L;
	if(b==0)
		return 0;
	}
	cout << "�����������Ŷ����������һ��Ŷ";
	goto A;
	return 0;
}
