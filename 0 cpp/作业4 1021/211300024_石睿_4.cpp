#include <iostream>
using namespace std; 
/* run this program using the console pauser or add your own getch, system("pause") or input loop */
//现有1元、2元和5元的货币，购买价值为n元的物品，有多少种支付方式?编程实现输出每一种支付方式
int main() 
{
	int n,i,j,a,b,c,d;
	cout << "请输入购买价格" << endl;
	cin >> n;
	a=n/5;				//a是n除以5取整，即最多可以用a个5元来买 
	for(i=0;i <= a;i++) //分别用1.2.3.到最多的5元个数来买 
	{
		b=n-i*5;        //用5元买之后剩下的钱数 	//b是用完5元之后的钱数 
		c=b/2;          //剩下的钱最多可以用c个2元的
		for(j=0;j <= c;j++)
		{
			d=b-j*2;    //剩下的钱数（用完2、5元的纸币） 
			cout << n << "元价格的产品可以用" << i <<"个5元" <<  j <<"个2元" << d << "个1元" << endl; 	            
				//循环的时候注意cout的放置位置！！如果放到现在这个位置，每一个i会有不同的j、d情况，ok 
		}               
			//如果放到这个位置，每一个i只会输出一遍cout就直接返回循环的起始了 
	}			
	return 0;
}
