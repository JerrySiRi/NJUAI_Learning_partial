#include<iostream>
#include<cstring>
/*
用递归的方法编程实现：用1~4这4个数字中，组成4位数，每位数字不重复，输出所有符合的数。
*/
using namespace std;
int d[4]; 
void lc (int a,const int c,int n,int s);//函数声明 
int main ()
{
int b=1234;
lc(b,b,0,10);
	return 0;
}

void lc (int a,const int c,int n,int s)//好！传进来两个量，一个量不能动，一个量在函数运行之中会变化
									   //用const传入不变的量！ 
{int i,j;
if (n==4) cout<<d[0]<<d[1]<<d[2]<<d[3]<<' ';
else {for (i=0;i<4-n;i++)
        {a%=s;//把a除以10并且取余数给a 
		 d[n]=a/(s/10);  
		a=(c/s)*(s/10)+a%(s/10);
		s*=10;
              n++;
          lc(a,a,n,10);
          n--;
          a=c;
         }
     }     
}
