#include <iostream>
using namespace std;
/* run this program using the console pauser or add your own getch, system("pause") or input loop */

int main() 
{
	int a[20];
	int i;
	for(i=0;i<20;i++)
		{
			int x;
			cin >> x;
			if(x!=9)
				a[i]=x;
			else
				break;
		}
	for(int m=0;m<20;m++)
		cout << a[m] << " ";
	cout<< endl;
	
	return 0;
}
