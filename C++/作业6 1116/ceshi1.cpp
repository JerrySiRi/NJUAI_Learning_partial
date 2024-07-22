#include <iostream>
using namespace std;
/* run this program using the console pauser or add your own getch, system("pause") or input loop */
//函数1：str_len计算字符串长度，并返回他的长度（不算\0）
int str_len(char str[])
{
	int count=0;
	while(str[count]!='\0')
		count++;
	return count;
} 
//函数7：str_insert功能：在下标index处插入str5
//str_insert(str1,index,str5)
void str_insert(char str1[],int index,char str5[])
{
	char ch[20];//不会被改变的中间量 
	for(int i=0;i<str_len(str1);i++)
		ch[i]=str1[i];
	int a=str_len(str5);
	int b=str_len(str1);
	for(int i=index;i<a+b;i++)
	{
		if(i<index+a)
			str1[i]=str5[i-index];
		else
			str1[i]=ch[i-a];	
	}
	
 } 
int main() 
{
	char str1[20]="hello PKU";
	int index=6;
	char str5[]="my";
	  str_insert(str1,index,str5); 
  //【str_insert功能：在下标index处插入str5】改变的str1 
   
  cout<<str1<<endl;  //输出： hello myPKU
	return 0;
}
