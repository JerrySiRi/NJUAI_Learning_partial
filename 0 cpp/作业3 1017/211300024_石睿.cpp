#include <iostream>
using namespace std;
/* run this program using the console pauser or add your own getch, system("pause") or input loop */
int main()
{
	int month,day,days;
	cout << "请输入日期的月和日" << endl;
	cin >> month >> day;
	int a;
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
		case 0: cout << month << "月" << day <<"日" << "是2021年的第" << b << "天" <<endl; cout << "是星期五";break; 
		case 1: cout << month << "月" << day <<"日" << "是2021年的第" << b << "天" <<endl; cout << "是星期六";break; 
		case 2: cout << month << "月" << day <<"日" << "是2021年的第" << b << "天" <<endl; cout << "是星期日";break; 
		case 3: cout << month << "月" << day <<"日" << "是2021年的第" << b << "天" <<endl; cout << "是星期一";break; 
		case 4: cout << month << "月" << day <<"日" << "是2021年的第" << b << "天" <<endl; cout << "是星期二";break; 
		case 5: cout << month << "月" << day <<"日" << "是2021年的第" << b << "天" <<endl; cout << "是星期三";break; 
		case 6: cout << month << "月" << day <<"日" << "是2021年的第" << b << "天" <<endl; cout << "是星期四";break; 

	}
	return 0;
}





