#include <iostream>
#include<iomanip>
using namespace std;

/*
���ʵ�����������ǡ���������n��n<13�����n��������ǡ���������4�������������
��12���±���11 0\11 2\11 4.����11 10 11 12...11 20�м����11 11Ŷ�������ö�ά�����С��һ����12*23�Ķ�ά�����С�Ϳ����� 

            1

         1     1

       1    2    1

    1    3    3     1
    Ϊ�������Ǳ��ֶ��룬��13����������������ֲ�����1000����������iomanip֮�� cout << setw(4)�Ϳ����� 
*/
int main()
{
	int n;
	cout <<"������������ǵ�����"<<endl;
	cin >>n;
	int arr[12][23];
	//step1:�������ε������߶��趨�ö���1
	for(int i=0;i<12;i++)
		for(int j=0;j<23;j++)
			arr[i][j]=0;
	for(int i=0;i<12;i++)
		{
			arr[i][11-i]=1; 
			arr[i][i+11]=1;
		}
	//step2��ÿ�е�һ��Ԫ����arr[i][11-i] 
	for(int i=1;i<11;i++)
		for(int j=0;j<=i;j++)
		{
			int a=11-i+2*j;
			int b=11-i+2*(j+1);
			arr[i+1][a+1]=arr[i][a]+arr[i][b];//�����Ƿ����±����� 
		}
	for(int i=0;i<n;i++)
		{for(int j=0;j<=23;j++)
			{
			if(arr[i][j]==0)
				cout<< "    ";
			else 
				cout <<setw(4)<<arr[i][j];
			}
			cout << endl; 
		}	
	return 0;
}
