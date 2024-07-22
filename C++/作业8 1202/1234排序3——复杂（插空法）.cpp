#include <iostream>
using namespace std;
int fctrl(int n)//计算阶乘的函数 
{int product=1;
while(n>1)
	{product*=n;
	n--;
	}
return product;
}

void swap(char *p,char *q)//改变两个数组的值 
{char temp=*p;
*p=*q;
*q=temp;
return;
}

typedef char A[5];

void permute(A a[],int n)
{int num=fctrl(4);//4的阶乘 
if(n==1)
	for(int i=0;i<num;i++)
		a[i][0]='1';//把这个二维数组每个元素都赋值为1 
else
	{permute(a,n-1);
	int fct=fctrl(n);
	for(int i=0;i<fct;i++)
		for(int j=0;j<num/fct;j++)
			{a[i*num/fct+j][n-1]=n+'0';
			for(int k=1;k<=i%n;k++)
				swap(a[i*num/fct+j][n-k],a[i*num/fct+j][n-k-1]);
			}
	}
return;
}

int main()
{int num=fctrl(4);
A a[num];
for(int i=0;i<num;i++)
	{for(int j=0;j<4;j++)
		a[i][j]='0';
	a[i][4]='\0';
	}
permute(a,4);
for(int i=0;i<num;i++)
	cout<<a[i]<<' ';
return 0;
}
