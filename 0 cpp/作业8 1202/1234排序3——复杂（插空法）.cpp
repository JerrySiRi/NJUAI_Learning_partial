#include <iostream>
using namespace std;
int fctrl(int n)//����׳˵ĺ��� 
{int product=1;
while(n>1)
	{product*=n;
	n--;
	}
return product;
}

void swap(char *p,char *q)//�ı����������ֵ 
{char temp=*p;
*p=*q;
*q=temp;
return;
}

typedef char A[5];

void permute(A a[],int n)
{int num=fctrl(4);//4�Ľ׳� 
if(n==1)
	for(int i=0;i<num;i++)
		a[i][0]='1';//�������ά����ÿ��Ԫ�ض���ֵΪ1 
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
