#include<iostream>
#include<cstring>
/*
�õݹ�ķ������ʵ�֣���1~4��4�������У����4λ����ÿλ���ֲ��ظ���������з��ϵ�����
*/
using namespace std;
int d[4]; 
void lc (int a,const int c,int n,int s);//�������� 
int main ()
{
int b=1234;
lc(b,b,0,10);
	return 0;
}

void lc (int a,const int c,int n,int s)//�ã���������������һ�������ܶ���һ�����ں�������֮�л�仯
									   //��const���벻������� 
{int i,j;
if (n==4) cout<<d[0]<<d[1]<<d[2]<<d[3]<<' ';
else {for (i=0;i<4-n;i++)
        {a%=s;//��a����10����ȡ������a 
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
