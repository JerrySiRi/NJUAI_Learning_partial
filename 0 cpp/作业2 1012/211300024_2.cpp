#include <iostream>
using namespace std; 
/* run this program using the console pauser or add your own getch, system("pause") or input loop */

int main()
{
	char ch;
	cin >> ch;
	if('0' <= ch && ch <='9')
		cout << "����";
	else if('a' <= ch && ch <= 'z')
		cout << "Сд��ĸ";
	else if('A' <= ch && ch <= 'Z')
		cout << "��д��ĸ";
	else
		cout << "�����ַ�";	
	return 0;
}
