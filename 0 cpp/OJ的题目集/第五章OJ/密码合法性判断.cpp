#include <iostream>
using namespace std;
/*
题目：密码合法性判断
题目描述：
规定某系统的用户密码只能是数字、英文大小写字母组成，且必须包含数字和字母，长度不能小于8位字符。
针对用户输入的密码，符合密码规则的，输出“valid”，否则输出“invalid”。说明：用户输入的密码最长不会超过20个字符，并且不包含空白符。
*/
int main()
{
	char ch[21];
	cin >> ch;
	int i=0,sum=0;
	while(ch[i]!='\0')
	{
		sum++;//一共有sum个字符的是有效的！
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
				cout << "invalid";return -1;//为什么改成-1就是nzec？？程序返回值非0 
			}
	}
	if((count1+count2<8)||(count1==0)||count2==0)
		cout <<"invalid";
	else
		cout << "valid";
	return 0;
}
