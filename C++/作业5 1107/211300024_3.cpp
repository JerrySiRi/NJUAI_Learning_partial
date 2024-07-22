#include <iostream>
using namespace std;
/* run this program using the console pauser or add your own getch, system("pause") or input loop */
/*
验证哥德巴赫猜想。编程验证2000以内的不小于4的***正偶数都能够分解为两个素数之和。
程序运行时，从键盘输入一个2000以内的正偶数，在屏幕上输出所有的分解结果。输入输出的形式自行设定，注意交互友好。
【交互友好=如果输入的不是正偶数，可以让他重新输出的哦return -1】 
【任务分解】包含两个任务： 
①得先找出来小于这个数字有哪些素数,并加以保存*** 
②之后再找出来这些素数哪些加起来可以等于这个数 
方法二：找出来所有2000之内的素数，并加以保存+再运算会更简单一点的
*/
bool sushu(int i)//判断i是不是素数 
{
	int j=2;
	for(;j<i;j++)
	{
		if(i%j==0) return false;//bool类型的必须得有true和false两种的！不能只有true类型的 
	}							//运用bool类型肯定是要判断是不是true的呀，所以一定会有false的存在嘛 
	if(i%j!=0||i==j)
		return true;
}
int main() 
{
	
	int a;
	cout <<"请输入一个2000以内且不小于4的正偶数"<<endl;
	cin >>a;												//不要忘记输入了 
	if(a<4||a>=2000||a%2!=0)
		{cout <<"输入错误，请重新输入"; return -1;}
	int j=0;
	for(int b=2;b<2000;b++)	
	{													//第一步：先判断2000之内有多少个素数！ 
		int i=2;
		for(;i<b;i++)
		{
			if(b%i==0)break;	
		}
		if(b%i!=0||b==i)						//小心i++是加过一个i之后不满足条件后才出的循环的
			j++;								//2000之内有303个素数》》可以创建j个数组
	}
	int	arr[j],n=0;								//第二步：开始把数字存到数组之中
	for(int m=2;m<2000;m++)
	{
		if (sushu(m))
		{
			arr[n]=m;
			n++;
		}
	}
												//第三步：开始判断两个素数之和的问题	
	for(int p=0;p<j;p++)
	{
		for(int q=0;q<=p;q++)					//要仔细！如果是p小于j的话，就会有重复输出啦！ 
			{									//要避免顺序的改变 
				if(arr[p]+arr[q]==a)
					cout <<a<<"可以分解为" <<arr[p]<<"和"<< arr[q] <<"两个素数之和"<<endl; 
			}
	} 				
	return 0;
}
/*
方法二： 
#include <iostream>
#include <cmath>
using namespace std;
int f(int a)
{
	for (int i=2;i<=sqrt(a);i++)
	{
		if (a%i==0)							//求素数的方法***比咱们自己的更加简单地哦 
		  return -1;
	}
	return a;
}
int main ()
{
	int n;
	cin>>n;
	for (int j=2;j<=n;j++)
		for (int k=2;k<=j;k++)
		{
			if (f(j)+f(k)==n && f(j)!=-1 && f(k)!=-1)
			cout<<f(j)<<" "<<f(k);
		}
		
}
*/
