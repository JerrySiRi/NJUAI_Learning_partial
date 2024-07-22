#include <iostream>
using namespace std; 
/* run this program using the console pauser or add your own getch, system("pause") or input loop */

int main()
{
	char ch;
	cin >> ch;
	if('0' <= ch && ch <='9')
		cout << "Êý×Ö";
	else if('a' <= ch && ch <= 'z')
		cout << "Ð¡Ð´×ÖÄ¸";
	else if('A' <= ch && ch <= 'Z')
		cout << "´óÐ´×ÖÄ¸";
	else
		cout << "ÆäËû×Ö·û";	
	return 0;
}
