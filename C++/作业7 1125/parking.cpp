#include <iostream>
#include <ctime>
#include <cstring>
#include "define.h"
using namespace std;
/*
给一个停车场设计一个停车系统。
停车场总共有两种不同大小的车位：大型和小型，每种车型分别有固定数目的车位。
停车计费按照每小时计算，不足一小时，按一小时计算。系统包括以下功能：
（1）    初始化系统：设定大型和小型车位的数目，设定每小时收费金额。
（2）    汽车进场：根据车型，如有车位，则返回车位号，如没有，则返回0。
	//设定函数 
（3）    汽车出场：根据汽车进场时间，计算某个车位应该收取的停车费，并输出停车费。
（4）更进一步：如果按周末**节假日区分收费标准，如何设计。暂不考虑跨日，即一辆车的进出都是在同一天。

（5）建议模块化设计程序，适当加入注释以便助教批改。

时间计算可以利用库函数

#include <ctime>

#include <cstring>

 time_t before = time(0);  //获取当前时间

 ……

time_t now = time(0);     //再次获取时间，获得1970至今的秒数！ 

cout<<now-before；    //输出两次时间的秒数差

char dt[26];  

   strcpy(dt, ctime(&now));   //vs  ctime_s(dt,26,&now) 获取时间字符串

 如果输出dt 会显示包含日期的时间， 例如： Wed Nov 18 10:54:31 2020
*/

int main()
{
	//step1：设定有多少大型车和小型车，设置收费金额 
	Car zaibuzai[100];//zaibuzai这个数组有100个元素，每个元素都是一个Car类型（结构），每个元素中（结构）
																					  //都会有两个bool类型 
	int i; 
	for(i=0;i<50;i++)
	{
		zaibuzai[i].da=true;
		zaibuzai[i].xiao=true;	//如果zaibuzai.da或者zaibuzai.xiao之中有一个是true的话，那他就是有车位的 
	}
	double feeda=0.005;			//一秒钟0.005》》大概一个小时不到20块
	double feexiao=0.006; 
	//【汽车进场】 
	L1:
	cout << "请输入车的类型,如果是大型车请输入“d”，如果是小型车请输入“x”"<<endl;
	char arr[2];
	cin >> arr;
	int a=free(arr,zaibuzai);
	if(a==0)
		cout<<"非常抱歉，本车库没有您车型所对应的空余车位了"<<endl;
	else
		cout << "请您进入第"<<a<<"个车位停车"<<endl;
	if(strcmp(arr,"d")==0)
		zaibuzai[a-1].da=false;
	else 
		zaibuzai[a-1].xiao=false;
	time_t before = time(0);
	//获取当前时间
	//【汽车出场】
	int b;
	cout <<"如果您要离开，请输入0以结算价格"<<endl;
	if(strcmp(arr,"d")==0)
		zaibuzai[a-1].da=true;
	else 
		zaibuzai[a-1].xiao=true;
	cin >> b;
	char dt[26]; 
	time_t now = time(0);  
    strcpy(dt, ctime(&now));   //vs  ctime_s(dt,26,&now) 获取时间字符串	
    char arr1[5];
    for(int j=0;j<3;j++)
    	arr1[j]=dt[i];
	if(b==0&&strcmp(arr,"x")==0)
	{     //再次获取时间，获得1970至今的秒数！ 
		if(weekend(arr1))
			cout<<"您本次停车一共"<<(now-before)*(feexiao+0.001)<<"元，请您微信扫码支付"<<endl; 
		else
			cout<<"您本次停车一共"<<(now-before)*feexiao<<"元，请您微信扫码支付"<<endl; 
	}
	else if((b==0)&&(strcmp(arr,"d")==0))
	{     //再次获取时间，获得1970至今的秒数！ 
		if(weekend(arr1))
			cout<<"您本次停车一共"<<(now-before)*(feeda+0.001)<<"元，请您微信扫码支付"<<endl; 
		else
			cout<<"您本次停车一共"<<(now-before)*feeda<<"元，请您微信扫码支付"<<endl; 
	}
	int m;
	cout <<"如果您想继续停车，请输入0，不想停车请输入1"<<endl;
	cin >>m;
	if(m==0) 
		goto L1;
	else
		return 0;
}


/*
出现的问题： 
①struct的问题（多次出现）

main.cpp之中其实不需要再次定义了！因为头文件那里引入了define.h的文件了，这个文件里有struct的定义了呢
define.cpp之中必须要有struct的定义，因为下面定义函数之中 struct Cat作为形式参数传到了函数里边
			必须得让计算机知道这个Cat是个什么类型的变量才可以呢
define.h之中也必须要有struct的定义，因为函数声明之中一定需要把形参表示出来！必须得写出来才能让你过呢！
			所以得让函数声明的时候的形参知道Car是什么东西
【main中引入.h会去找.h之中有啥东西，但是.h和deine.cpp之中并没有引用main.cpp中的定义》》他们不知道
Car是什么东西的捏！】 
 
 
②struct之中如果把结构类型的变量定义成了数组，那么这个数组中的元素就是一个个结构了。
  如上zaibuzai如果定义成了一个结构类型的数组，其中每个元素是一个结构，结构中就不能在有50个bool类型的元素数组了
  》》重复定义了数组，这样就相当于有50*50的元素啦
③ ==的问题又出现了
④ 判断字符串是不是相等可不能用==来判断哦！一定要用strcmp来判断的呢！
⑤头文件引入的问题！
	一定要在main函数之中有“define.h”的！ 
优化：没有必要让用户输入一个字符串，出入d或者x来表示da或者xiao不就没有问题了嘛！
	   判断是不是周末》》只有周末开头是S》》直接用S来判断是不是周末就可以啦！ 
⑥strcmp的用法！
【int strcmp(char *str1, char *str2);
比较字符串str1和str2是否相同。如果相同则返回0；
如果不同，在不同的字符处如果str1的字符大于str2的字符，则返回1，否则返回-1 】！ 
⑦字符串输入：尽管可以整体输入，但是cin>>ch的时候一定不能带[]呀！不然只输入了那一位呢！
  没有把整个字符串都输入呢！ 
  
  不足：
  ①没有实现多线程工作：这个用户不走，让下一个用户进来 
  ②可以在结构类型中多存几个部分，这个用户的存入时间和取出时间
  	这样就方便这个用户不出来，其他用户也可以进来啦 
*/
