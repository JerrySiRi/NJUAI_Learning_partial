#include <iostream>
using namespace std;
/* run this program using the console pauser or add your own getch, system("pause") or input loop */
int main()
{
	int month,day,days;
	cout << "���������ڵ��º���" << endl;
	cin >> month >> day;
	int a=0;
	for(int i=1;i<month;i++)
	{
		switch(i)
			{
				case 1:case 3:case 5:case 7:case 8:case 10:case 12:
					days = 31;
					break;
				case 4:case 6:case 9:case 11:
					days = 30;
					break;
				case 2:
					days = 28;
					break;	
			}
	a +=days;
	 } 
	int b;
	b = a + day;	
	int c;
	c= (b-1)%7; 
	switch(c)
	{
		case 0: cout << month << "��" << day <<"��" << "��2021��ĵ�" << b << "��" <<endl; cout << "��������";break; 
		case 1: cout << month << "��" << day <<"��" << "��2021��ĵ�" << b << "��" <<endl; cout << "��������";break; 
		case 2: cout << month << "��" << day <<"��" << "��2021��ĵ�" << b << "��" <<endl; cout << "��������";break; 
		case 3: cout << month << "��" << day <<"��" << "��2021��ĵ�" << b << "��" <<endl; cout << "������һ";break; 
		case 4: cout << month << "��" << day <<"��" << "��2021��ĵ�" << b << "��" <<endl; cout << "�����ڶ�";break; 
		case 5: cout << month << "��" << day <<"��" << "��2021��ĵ�" << b << "��" <<endl; cout << "��������";break; 
		case 6: cout << month << "��" << day <<"��" << "��2021��ĵ�" << b << "��" <<endl; cout << "��������";break; 

	}
	return 0;
}

