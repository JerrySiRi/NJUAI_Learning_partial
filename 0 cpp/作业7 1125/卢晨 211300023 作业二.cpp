#include<iostream>
#include<ctime>
#include<cstring>
using namespace std;
int holiday(char date[]);
int search(bool a[],int head,int tail);//寻找有无空车位 
double total(time_t now,time_t before,double fee);//计算停车费 
int main ()
{ int bignum,smallnum,place,outnumber,n,m,k,f;
  char date[4];
 struct A
    {bool a[200];//big车位都在0号到big-1号，small车位都在big号到big+small-1号 
    time_t before[200],now[200];
	};
	A bigpark,smallpark;
	time_t today;
    double bigfee,smallfee;
    cin>>bignum>>smallnum;
    cin>>bigfee>>smallfee;//设定大型和小型车位的数目，设定每小时收费金额。
    for (k=0;k<=bignum-1;k++)
	bigpark.a[k]=true;
		for (k=bignum;k<=bignum+smallnum-1;k++)
	smallpark.a[k]=true;
    strncpy(date,ctime(&today),3);
    if (holiday(date)==1) {bigfee*=2;smallfee*=2;}//周末收2倍的车费 
	char type[6];
	lc:
	cout<<"是否要停车？是的话输入1，否则输入2.";
	cin>>n; 
	if (n==1)
	{cout<<"请输入汽车类型（big or small）";
	cin>>type;
	if (strcmp(type,"big")==0) 
	{place=search(bigpark.a,0,bignum-1);if (place!=-1) {cout<<"您的车位是"<<place<<endl;bigpark.before[place]=time(0);bigpark.a[place]=false;}
	                                                                 else cout<<"无车位啦";}
	if (strcmp(type,"small")==0) 
	{place=search(smallpark.a,bignum,bignum+smallnum-1);if (place!=-1) {cout<<"您的车位是"<<place<<endl;smallpark.before[place]=time(0);smallpark.a[place]=false;}
	                                                                                   else cout<<"无车位啦";}//根据车型，如有车位，则返回车位号，如没有，则返回-1。
    }
	cout<<"是否要出车？是的话输入1，否则输入2.";
	cin>>m;
	if (m==1) 
{	cout<<"请输入您的车位号";
    cin>>outnumber;//输入出场车辆的车位号 
	if ((outnumber>=0)&&(outnumber<=(bignum-1))) {bigpark.a[outnumber]=true;bigpark.now[outnumber]=time(0);cout<<"车费是"<<total(bigpark.now[outnumber],bigpark.before[outnumber],bigfee)<<endl;}
	if ((outnumber>=bignum)&&(outnumber<=(bignum+smallnum-1))) {smallpark.a[outnumber]=true;smallpark.now[outnumber]=time(0);cout<<"车费是"<<total(smallpark.now[outnumber],smallpark.before[outnumber],smallfee)<<endl;}
}
	 cout<<"是否要打烊车库？是的话输入1，否则输入2.";
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
