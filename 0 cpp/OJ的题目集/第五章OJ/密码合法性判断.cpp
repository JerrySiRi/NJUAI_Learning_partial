#include <iostream>
using namespace std;
/*
��Ŀ������Ϸ����ж�
��Ŀ������
�涨ĳϵͳ���û�����ֻ�������֡�Ӣ�Ĵ�Сд��ĸ��ɣ��ұ���������ֺ���ĸ�����Ȳ���С��8λ�ַ���
����û���������룬�����������ģ������valid�������������invalid����˵�����û��������������ᳬ��20���ַ������Ҳ������հ׷���
*/
int main()
{
	char ch[21];
	cin >> ch;
	int i=0,sum=0;
	while(ch[i]!='\0')
	{
		sum++;//һ����sum���ַ�������Ч�ģ�
		i++;
	}
	int count1=0,count2=0;
	for(int j=0;j<sum;j++)
	{
		if(ch[j]>='0'&&ch[j]<='9')
			count1++;
		else if((ch[j]>='a'&&ch[j]<='z')||(ch[j]>='A'&&ch[j]<='Z'))
			count2++;
		else
			{
				cout << "invalid";return -1;//Ϊʲô�ĳ�-1����nzec�������򷵻�ֵ��0 
			}
	}
	if((count1+count2<8)||(count1==0)||count2==0)
		cout <<"invalid";
	else
		cout << "valid";
	return 0;
}
