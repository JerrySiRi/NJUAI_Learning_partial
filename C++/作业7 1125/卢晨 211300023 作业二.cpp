#include<iostream>
#include<ctime>
#include<cstring>
using namespace std;
int holiday(char date[]);
int search(bool a[],int head,int tail);//Ѱ�����޿ճ�λ 
double total(time_t now,time_t before,double fee);//����ͣ���� 
int main ()
{ int bignum,smallnum,place,outnumber,n,m,k,f;
  char date[4];
 struct A
    {bool a[200];//big��λ����0�ŵ�big-1�ţ�small��λ����big�ŵ�big+small-1�� 
    time_t before[200],now[200];
	};
	A bigpark,smallpark;
	time_t today;
    double bigfee,smallfee;
    cin>>bignum>>smallnum;
    cin>>bigfee>>smallfee;//�趨���ͺ�С�ͳ�λ����Ŀ���趨ÿСʱ�շѽ�
    for (k=0;k<=bignum-1;k++)
	bigpark.a[k]=true;
		for (k=bignum;k<=bignum+smallnum-1;k++)
	smallpark.a[k]=true;
    strncpy(date,ctime(&today),3);
    if (holiday(date)==1) {bigfee*=2;smallfee*=2;}//��ĩ��2���ĳ��� 
	char type[6];
	lc:
	cout<<"�Ƿ�Ҫͣ�����ǵĻ�����1����������2.";
	cin>>n; 
	if (n==1)
	{cout<<"�������������ͣ�big or small��";
	cin>>type;
	if (strcmp(type,"big")==0) 
	{place=search(bigpark.a,0,bignum-1);if (place!=-1) {cout<<"���ĳ�λ��"<<place<<endl;bigpark.before[place]=time(0);bigpark.a[place]=false;}
	                                                                 else cout<<"�޳�λ��";}
	if (strcmp(type,"small")==0) 
	{place=search(smallpark.a,bignum,bignum+smallnum-1);if (place!=-1) {cout<<"���ĳ�λ��"<<place<<endl;smallpark.before[place]=time(0);smallpark.a[place]=false;}
	                                                                                   else cout<<"�޳�λ��";}//���ݳ��ͣ����г�λ���򷵻س�λ�ţ���û�У��򷵻�-1��
    }
	cout<<"�Ƿ�Ҫ�������ǵĻ�����1����������2.";
	cin>>m;
	if (m==1) 
{	cout<<"���������ĳ�λ��";
    cin>>outnumber;//������������ĳ�λ�� 
	if ((outnumber>=0)&&(outnumber<=(bignum-1))) {bigpark.a[outnumber]=true;bigpark.now[outnumber]=time(0);cout<<"������"<<total(bigpark.now[outnumber],bigpark.before[outnumber],bigfee)<<endl;}
	if ((outnumber>=bignum)&&(outnumber<=(bignum+smallnum-1))) {smallpark.a[outnumber]=true;smallpark.now[outnumber]=time(0);cout<<"������"<<total(smallpark.now[outnumber],smallpark.before[outnumber],smallfee)<<endl;}
}
	 cout<<"�Ƿ�Ҫ���ȳ��⣿�ǵĻ�����1����������2.";
	cin>>f;
	if (f==2) goto lc;
	else return 0;
}



int search(bool a[],int head,int tail)
{int i;
for(i=head;i<=tail;i++)
 if (a[i]==true) return i;
 return -1;
}



double total(time_t now,time_t before,double fee)
{int s;
s=now-before;
if ((s%3600)==0) return fee*(s/3600);
else return fee*(s/3600+1);
}




int holiday(char date[])
{if (strcmp(date,"Sat")==0) return 1;
if (strcmp(date,"Sun")==0) return 1;
return 0;
}
