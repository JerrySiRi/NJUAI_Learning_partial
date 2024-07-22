#include <iostream>
#include <fstream>
#include <cstring>
#include <iomanip>
#include <ctime>
using namespace std;
/*
练习小程序，需要完成的基本功能要求：

1、程序运行后，显示菜单：用户登录【1】、用户注册【2】。
 
2、用户登录后，显示菜单【3】 

选择练习难度【4】：选择难度等级后，显示相应运行界面【4】，练习结束后，保存练习记录【5】
用户可以再次练习，或者退出程序。【5】 

查看练习记录：自行设计记录内容和样式。

3、用户注册界面：自行设计

其他功能：八仙过海各显神通，可以尝试挑战。比如：是否设计管理员角色、提示用户练习的错误所在、计时练习......

提示：（1）文件数据的读写参照教材332页，9.3.3节，作业额外文件是文件读写的sample

      （2）请实现模块化设计
*/


/*
【输入的格式】 
	①ifstream infile("1.txt",ios::in);
	if(!infile.is_open()) 
	{
		cout << "文件不存在";
		exit(-1);
	}
	char name[20], psw[10];//一定要先定义申请好了空间，才能输出的哦**** 
   infile>>name>>psw;//输出的时候也更是可以定义一个结构类型变量，***（集成化更高的**）
   for(int i=0;i<20;i++)
   infile >> user.name[i] >> user.password[i];
   infile.close();   
	②大部分情况是需要循环读入的**
	while(!infile.eof())循环到打开不成功的时候哦 
	{
		infile>>list[num].name >> list[num].password;
		num++;
	} 
	 


【输出的格式】 
	ofstream outfile("1.txt",ios::app)
	if(!outfile.is_open())
		{
			cout << "文件打开不成功";
			exit(-1);
		}
		char ch[1000];
	outfile << ch << endl;
	outfile.close();
*/
extern void deng(char name[]);
extern void fresh();
extern void log(char name[]);
extern void easy(char name[]); 
extern void average(char name[]);
extern void hard(char name[]);
extern void record(char name[]);
int main() 
{
	char name [10];//要记住成功登录用户的名字的** 
	deng(name);
	L1:
	A:
	cout <<"欢迎您来到打字游戏！请选择您要进行练习的难度（easy、average、hard）"<<endl;
	cout<< "如果您想查看之前的游戏记录，请输入 record"<< endl;
	char choice[10];
	cin >>choice;
	if(strcmp("easy",choice)==0)
			easy(name);
	else if (strcmp("average",choice)==0)
		average(name);
	else if (strcmp("hard",choice)==0)	
		hard(name);
	else if(strcmp("record",choice)==0)
		{
			record(name);
			goto A;
		}
	
	cout << "如果您想继续游戏，请输入yes。如果您想退出游戏，请输入其他。"<<endl;
	char ch[10];
	cin >> ch;
	if(strcmp("yes",ch)==0)
		goto L1;
	return 0;
}

//step1:完成菜单的设计、用户登录、用户注册
/*
菜单：①请输入您的用户名以及密码（让用户在一行输入）+如果未注册-请注册【也可以分模块运行】 
*/ 
void deng(char name[])//用户登录 
{
	char ch1[10];
	cout <<"如果您是新用户，请输入“yes”。如果您已经注册，请输入“no”"<<endl;
	cin >> ch1;
	if(strcmp("yes",ch1)==0)//是新用户
	{
		fresh();//先完成注册 
		log(name);//登录 
	}
	else
		log(name);//登录 
}

void fresh()//【新用户注册】 
{ 
	cout << endl; 
	cout << "~~~~~~~~~~[新用户注册]~~~~~~~~~~"<< endl;
	char ch3[10];
	L2:
	cout << "请输入您的用户名和密码（密码不超过8位，超过8位自动读入前8位）"<<endl;
	ifstream infile("users.txt",ios::in);
	if(!infile.is_open()) 
	{
		cout << "文件不存在";
		exit(-1);
	} 
	
	cin >> ch3;//【错误2】 字符串输入，不能有[]!!!!! 
	//【用户名的输入】	
	char ch2[10];
	infile >> ch2;//【错误1】 
	/*
	这个infile.ios::eof的含义是这一行上一行是没有东西的、
	所以需要在外边先对infile这一行赋值完成 
	不然都进不了这个循环的，上一行是随机值，而不是空呢*** 
	*/
	while(infile.ios::eof()==0)
	{
		if(strcmp(ch3,ch2)==0)
			{	
				cout << "该用户名已被注册，请重新输入新用户名";
				goto L2;
			}
		infile >> ch2;
	}
//现在ch3中存的就是用户的用户名啦**，最后再同一输入到文件之中*** 
	//【密码的输入】 
	char ch1[10];//infile是从文件中输入到程序之中的*** 
	L1:
	cin>>setw(9)>>ch1; 
	int i=0;
	while(ch1[i]!='\0')
	{
		if((ch1[i]<='z'&&ch1[i]>='a')||(ch1[i]<='9'&&ch1[i]>='0')||(ch1[i]<='Z'&&ch1[i]>='A'))
   			;
   		else
   		{
   			cout <<"输入不合法，请重新输入您的密码";
   			goto L1;
		}
		i++;
	}
	infile.close();
	ofstream outfile("users.txt",ios::app);	
	outfile << endl;
	outfile << ch3<< ' ' << ch1;

	outfile.close();
}

void log(char name[])//【用户登录】 
{
	cout << "~~~~~~~~~~[登录]~~~~~~~~~~" << endl;
	L3:
	cout << "请输入您的用户名以及密码"<<endl;
	char ch1[10],ch2[10];
	cin>>ch1>>ch2;
	char have1[10],have2[10];
	ifstream infile("users.txt",ios::in);
	infile >> have1>>have2;	
	while(infile.ios::eof()==0)//【eof刚开始返回的值是0；直到文件尾才返回真】 
	{
		if(strcmp(ch1,have1)==0&&strcmp(ch2,have2)==0)
			{
				cout << "登录成功"<<endl;//要记住这个用户名字的**之后要保存记录的
				strcpy(name,ch1);
				break;
			} 
		infile >> have1 >> have2;
		if(strcmp(ch1,have1)==0&&strcmp(ch2,have2)==0)
			{
				cout << "登录成功"<<endl;//要记住这个用户名字的**之后要保存记录的
				strcpy(name,ch1);
				goto L0;//Q：break只能打破if的这层括号？不用goto为什么会进下面的if？ 
			}
	}	
	if(infile.ios::eof()!=0)
	//初衷是：遍历所有的姓名和密码，都没有找到匹配的，才会进这个if 
	//但是如果在最后一行找到， 
		{
			cout <<"用户名或密码输入有误，请重新输入";
			goto L3;
		}
	L0:
	;
}
/*
eof的含义是：这个文件没有任何字符可以被读进来了。如果只读最后一行的前一半的字符，eof还是被给到了0
			如果最后一行的所有字符都被输出了，那么eof被给到1！
所以这次操作的时候，把最后一行的所有东西都输出了，那么eof被给到1！，会进下一次循环的

infile没有必要先输入，eof只要在文件中有东西没有被输出（是一个指针）的时候都会给到0的！ 
*/	
void easy(char name[])
{
	cout << "您选择的为easy模式，内容为 【英文字母表】" << endl;
	cout <<"现在开始记时"<<endl;
	ifstream infile("easy.txt",ios::in);
	char a[20];
	infile >> a;
	while(infile.ios::eof()==0)
	{
		cout << a << " ";
		infile >>a;
	}
	infile.close();//用完必须关闭。现在已经是文档的最后一行啦，之后直接不进循环呢** 
	cout << endl;
	char user[20];
	double accuracy;
	double count=0;
	time_t before = time(0);  //获取当前时间
	ifstream infile1("easy.txt",ios::in);//【一定要换一个对象定义呢】 
	cout << endl;
	infile1 >> a ;//又忘记得先输入一个啦！ 
	while(infile1.ios::eof()==0)
	{	
		cin >> user;
		if(strcmp(a,user)==0)
			count++;		
		infile1 >> a;	
	}
	infile1.close();
	accuracy=count/20;
	time_t now = time(0);     //再次获取时间
	cout<<"您总共用时"<<now-before<<"s"<<endl;    //输出两次时间的秒数差
	cout << "您的正确率为"<< (accuracy)*100 << '%' <<endl;
	cout << "您的训练记录已保存"<<endl;
	//训练记录：训练时间、正确率、总用时 
	char dt[26];  
    strcpy(dt, ctime(&now));   //vs  ctime_s(dt,26,&now) 获取时间字符串
	ofstream outfile("usersrecords.txt",ios::app);
	if(!outfile.is_open())
	{
		cout << "文件打开不成功";
		exit(-1);
	}
	outfile << name << " "<< "mode:easy"<<" "<< "accuracy:"<<accuracy*100 << '%' << " " <<"span:" <<now-before <<" "<< dt;
	outfile << endl;
	outfile.close();
}
	
void average(char name[])
{
	cout << "您选择的为average模式，内容为 【英文名言】" << endl;
	cout << "正确率标准为：一个词语全部输入正确才计算为正确（含标点哦）"<<endl;
	cout <<"现在开始记时"<<endl;
	ifstream infile("average.txt",ios::in);
	char a[15];
	infile >> a;
	while(infile.ios::eof()==0)
	{
		cout << a << " ";
		infile >>a;
	}
	infile.close();//用完必须关闭。现在已经是文档的最后一行啦，之后直接不进循环呢** 
	cout << endl;
	char user[15];
	double accuracy;
	double count=0;
	time_t before = time(0);  //获取当前时间
	ifstream infile1("average.txt",ios::in);//【一定要换一个对象定义呢】 
	cout << endl;
	infile1 >> a ;//又忘记得先输入一个啦！ 
	while(infile1.ios::eof()==0)
	{	
		cin >> user;
		if(strcmp(a,user)==0)
			count++;		
		infile1 >> a;	
	}
	infile1.close();
	accuracy=count/17;
	time_t now = time(0);     //再次获取时间
	cout<<"您总共用时"<<now-before<<"s"<<endl;    //输出两次时间的秒数差
	cout << "您的正确率为"<< (accuracy)*100 << '%' <<endl;
	cout << "您的训练记录已保存"<<endl;
	//训练记录：训练时间、正确率、总用时 
	char dt[26];  
    strcpy(dt, ctime(&now));   //vs  ctime_s(dt,26,&now) 获取时间字符串
	ofstream outfile("usersrecords.txt",ios::app);
	if(!outfile.is_open())
	{
		cout << "文件打开不成功";
		exit(-1);
	}
	outfile << name << " "<<"mode:average" << "accuracy:"<<accuracy*100 << '%' << " " <<"span:" <<now-before <<" "<< dt;
	outfile << endl;
	outfile.close();
}
	
	
/*
I will greet this day with love in my heart.
Do what you say,say what you do.
I can make it through the rain. I can stand up once again on my own.
*/ 
	

void hard(char name[])
{
	cout << "您选择的为hard模式，内容为 【英文诗歌】" << endl;
	cout << "正确率标准为：一个词语全部输入正确才计算为正确（含标点哦）"<<endl;
	cout <<"现在开始记时"<<endl;
	ifstream infile("hard.txt",ios::in);
	char a[15];
	infile >> a;
	while(infile.ios::eof()==0)
	{
		cout << a << " ";
		infile >>a;
	}
	infile.close();//用完必须关闭。现在已经是文档的最后一行啦，之后直接不进循环呢** 
	cout << endl;
	char user[15];
	double accuracy;
	double count=0;
	time_t before = time(0);  //获取当前时间
	ifstream infile1("hard.txt",ios::in);//【一定要换一个对象定义呢】 
	cout << endl;
	infile1 >> a ;//又忘记得先输入一个啦！ 
	while(infile1.ios::eof()==0)
	{	
		cin >> user;
		if(strcmp(a,user)==0)
			count++;		
		infile1 >> a;	
	}
	infile1.close();
	accuracy=count/146;
	time_t now = time(0);     //再次获取时间
	cout<<"您总共用时"<<now-before<<"s"<<endl;    //输出两次时间的秒数差
	cout << "您的正确率为"<< (accuracy)*100 << '%' <<endl;
	cout << "您的训练记录已保存"<<endl;
	//训练记录：训练时间、正确率、总用时 
	char dt[26];  
    strcpy(dt, ctime(&now));   //vs  ctime_s(dt,26,&now) 获取时间字符串
	ofstream outfile("usersrecords.txt",ios::app);
	if(!outfile.is_open())
	{
		cout << "文件打开不成功";
		exit(-1);
	}
	outfile << name << " "<<"mode:hard" << " " << "accuracy:"<<accuracy*100 << '%' << " " <<"span:" <<now-before <<" "<< dt;
	outfile << endl;
	outfile.close();
}

void record(char name[])
{
	ifstream infile("usersrecords.txt",ios::in);
	char ch1[20],ch2[20],ch3[20],ch4[20],ch5[20],ch6[20],ch7[20],ch8[20],ch9[20];
	while(infile.ios::eof()==0)
	{
		infile >> ch1>>ch2>>ch3>>ch4>>ch5>>ch6>>ch7>>ch8>>ch9;
		if(strcmp(ch1,name)==0)
		{
			cout << ch1<<" "<<ch2<<" "<<ch3<<" "<<ch4<<" "<<ch5<<" "<<ch6<<" "<<ch7<<" "<<ch8<< " "<<ch9;
			cout <<endl;
		}
	}
}
//Q:重复输出？？ 



	

