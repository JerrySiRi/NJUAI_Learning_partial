#include <iostream>
using namespace std;
/* run this program using the console pauser or add your own getch, system("pause") or input loop */
//编程实现：求出圆周率，并且让他的最后一项误差小于10的-8次方 
int main() 
{
	double n,k=0,m;
	double a=0,b=0;          //如果把a和b换成double就可以了，c用float和double都可以的 
	double c=0;               //最好都用double，float是4个字节，double是八个字节 
	while( 4*k < 1E8-1)      //科学计数法之中没有*的存在。10的正数次方用E，10的负数次方用e 
	{
		n=4*k+1;
		m=4*k+3;       //思路错误（应该不是本题的错误：计算机算的不是极限，误差可以忽略不计，但在思考的时候应该想到） 
		a += 1/n;	   //错误1-数分：无穷项的加法或者减法和加减的顺序有关系，(1+1/5+1/9.....)-(1/3-1/7-1/11-......)在无穷项 
		b += 1/m;	   //的加减法之中不一定和一项加一项减的结果是一样的 
		k++;		   //错误2-误差： 有些小数没有办法保存，误差过大 
	}
	c=a-b;				 
	cout << "圆周率在误差小于10的-8次方情况下为" << 4*c;
	return 0;
}					//***思路：直接按照思路来看，不需要改变题目顺序 



/*另外两种思路：
法①
c += 1/n; 
c -= 1/m;
k++;
最后直接输出c就是结果》》》同时用+=和-=来减少变量的次数 

法②
引出库函数x的n次幂，来计算-1的n次方来控制加一项之后减一项
b = 2*a-1;
c = 1/b;
d = c*pow(-1,a+1);【表示-1的a+1次方】 
*/ 


