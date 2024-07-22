#include<iostream>
#include <fstream>//文件流（把文件视为一种流、从文件到内容） 
using namespace std;
int main()
{   ifstream infile("user.txt",ios::in);   
	//源文件和user.txt在同一个文件夹中。inf：读入文件。infile：是ifstream的一个类。
	//后面是构造函数来初始化这个infile
	//如果和这个cpp不在一个文件中，需要指出他的路径的。D:\\在文件右击鼠标，把地址复制成文本**
	//需要把复制下来的一个\再加一个\，是一个转义序列的 
     char name[20], psw[10];
     
    if(!infile) //读入文件的时候，防止文件不在。来判断这个文件是不是真的存在 
   {  cout<<"文件不存在";
      return 0;
   }
   infile>>name>>psw;    // 读入user.txt文件里第一行用户名、密码
   //文件中会有多个用户的***》》循环读入的
   /*法一：先看有多少个用户（不超过100个）
   user list[100]
   int num=0;
   while(!infile.eof())打开失败
   。。。 
    
    法二：
	打开的文件之中第一行的数据是用户的个数
	打开之后
	
	
	其他：
	是不是用户名有重复
	是不是密码有效
	
	时间记录
	用停车场的时间记录方法 
   */ 
   //infile的作用和cin的作用一样。读入的前提是应该知道文件中存放的是什么**
   //如文件中是nju 21130000000  nju 211409999 【name+password】 
   cout<<name<<"  "<<psw<<endl;
   infile.close();
   char newname[20],newpsw[10];
   cin>>newname>>newpsw;
   ofstream outfile("user.txt",ios::app);   //在文件尾部操作   appendix：在文件尾部增加新用户 
   //outfile：往文件里写。 也是一个构造函数的新定义 
   outfile<<endl<<newname<<" " <<newpsw;  //在user.txt文件中的最后一行写入
   outfile.close();//读入或者读出结束之后需要关闭。类比：指针。》》文件打开之后也需要关闭的
    
    //写练习记录 
    //如果有记录的话、就先关闭再重新打开。如果没有记录，就直接打开 
   ofstream recodefile("recode.txt",ios::out);   //向recode文件写入信息
   
   int time = 10;
   double accuracy = 0.98;
   recodefile<<"Training time :"<<time<<" ; "<<"accuracy : "<<accuracy<<endl;
   recodefile.close();
   return 0;
}
