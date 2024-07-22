#include <iostream>
using namespace std; 
/* run this program using the console pauser or add your own getch, system("pause") or input loop */
//判断从键盘输入的一个整数是否为素数【例3-16 书中p67页】 
/*思路：
定义：素数1因子只有他自己和1》得从2开始一个一个除+除到n-1就可以啦
×优化：除2之外的偶数都不是，但是因为是从2开始除，所以这个不需要 
*/
 
int main() 
{
	cout << "请输入一个整数" << endl;
	int a,i;
	cin >> a;
	for(i=2;i <= a;i++)
	{
		if(a%i == 0) break;   //如果通过这条出来的，i的值就是a%i==0的值，就不会变了 
	}
	if(a==2 || i==a)		  //循环是啥时候不满足才出来的，不满足的时候已经把这个i+1了，a-1的时候是满足的，a-1+1=a的时候就满足了
							  //i是等于a的时候才出来的！！！
							  //是运行完最后一步的下一次循环准备的时候才会进行循环条件判断的哦 
		cout << a << "是素数";
	else
		cout << a << "不是素数";
	return 0;
}
