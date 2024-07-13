#include <iostream>
using namespace std;
/*题目：九九乘法表（教材第三章）
题目描述：
输出九九乘法表，输出时，每个算式后面空2个空格
前三行的输入如下：
1*1=1  
1*2=2  2*2=4  
1*3=3  2*3=6  3*3=9  
*/
int main() 
{
	int i,j;//外层行数为i，内层列数为j 
	for(i=1;i <= 9;i++)
	{
		for(j=1;j <= i;j++)
		cout << j << "*" << i << "=" << j*i << "  " ;
		cout << endl;
	}
	return 0;
}
