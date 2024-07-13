#include <iostream>
#include<iomanip>
using namespace std;

/*
编程实现输出杨辉三角。输入行数n（n<13）输出n行杨辉三角。例如输入4，输出三角如下
第12行下表是11 0\11 2\11 4.。。11 10 11 12...11 20中间的是11 11哦》》设置二维数组大小是一共有12*23的二维数组大小就可以啦 

            1

         1     1

       1    2    1

    1    3    3     1
    为了让三角保持对齐，第13行杨辉三角最大的数字不超过1000，所以引出iomanip之后 cout << setw(4)就可以了 
*/
int main()
{
	int n;
	cout <<"请输入杨辉三角的行数"<<endl;
	cin >>n;
	int arr[12][23];
	//step1:把三角形的两条边都设定好都是1
	for(int i=0;i<12;i++)
		for(int j=0;j<23;j++)
			arr[i][j]=0;
	for(int i=0;i<12;i++)
		{
			arr[i][11-i]=1; 
			arr[i][i+11]=1;
		}
	//step2：每行第一个元素是arr[i][11-i] 
	for(int i=1;i<11;i++)
		for(int j=0;j<=i;j++)
		{
			int a=11-i+2*j;
			int b=11-i+2*(j+1);
			arr[i+1][a+1]=arr[i][a]+arr[i][b];//现在是访问下标啦！ 
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
