#include <iostream>
using namespace std;
//函数1：str_len计算字符串长度，并返回他的长度（不算\0）
int str_len(char str[])
{
	int count=0;
	while(str[count]!='\0')
		count++;
	return count;
} 
 
 //函数2：str_cat连接字符串（加一个空格）,如str_cat(str1,str2),把连接之后的赋给str1
 void str_cat(char str1[],char str2[])
{
	int a;
	int len_1=str_len(str1),len_2=str_len(str2);
	a=len_1+len_2;//总长度
	for(int i=len_1;i<a;i++)
		str1[i]=str2[i-len_1];
	str1[a]='\0'; 
} 



//函数3：str_cpy往str3中拷贝str1的前len个字符，如str_cpy(str3,str1,len);前-新的串 中-被拷贝的 后-拷贝的长度
void str_cpy(char str3[],char str1[],int len)
{
	for(int i=0;i<len;i++)
		str3[i]=str1[i];
} 

//函数4：str_cmp功能：比较str2和str4的大小，如果前面字符串小于后面的字符串，那就是大于0的
bool str_cmp(char str2[],char str4[])
{
	int a=str_len(str2);//只需要把最小的字符串作为循环上限就可以啦 
	int b=str_len(str4);
	int c;
	if(a>b)
		c=b;
	else
		c=a;
	for(int i=0;i<c;i++)
	{
		if(str2[i]==str4[i])
			;
		else if(str2[i]>str4[i])
			return true;
		else
			return false;
	}
	if((str2[c-1]==str4[c-1])||(b>a))
		return false;
}

//函数5：str_replace功能：注意存在多个str2（在str1之中可能有多个str2），在str1中找到str2，并用str4替换
//str_replace(str1,str2,str4)，最后变的是str1的值
void str_replace(char str1[],char str2[],char str4[])
{
	int a=str_len(str1),b=str_len(str2);
	int i;
	for(i=0;i<=a-b;i++)
	{
		if(str1[i]==str2[0])//目前的i=6，进if 
			{
				for(int j=0;j<b;j++)
				{
					if(str1[i+j]==str2[j])
						;
					else if(str1[i+j]!=str2[j])	
						break;
				}
				if(str1[i+b-1]==str2[b-1])
					break;		
			}	
	}	
	//如果找到了，在str1中的下标就是i，从第i为开始替换成str4（str1的长度已知足够长）
	for(int k=i;k-i<str_len(str4);k++)
	{
		str1[k]=str4[k-i];	
	} 
} 


 
 //函数6：str_find功能：找到str4的第一个字符在str1中的位置，保证str1中一定有str4的存在 
 //str_find(str1,str4)，要有返回值的
 int str_find(char str1[],char str4[])
{
	int i=0;
	while(str1[i]!=str4[0])
	{
		i++;
	}
	return i;
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
 
 //函数8：to_lower功能： 将str1中的所有大写字母改为小写
 //to_lower(str1); 
 void to_lower(char str1[])
 {
 	int a=str_len(str1);
 	for(int i=0;i<a;i++)
 	{
 		if(str1[i]>='A'&&str1[i]<='Z')
		 	str1[i]=str1[i]-'A'+'a';	
	}
 }
  

/*
函数五： 
出现的错误原因：
①字符串个数太多，容易混淆，把str2写成了str4啦
②循环条件可不可以等于没有搞清楚！下次尽量不要依靠调试来解决，争取想清楚，拿笔写一写，一次搞定！
③多次循环要用到上一次循环后的结果，需要搞清楚下一次的循环条件是什么，是k-i小于还是k小于呢！ 
*/  

/*
函数二：
出现的错误原因：
①如果调用函数返回的是一个不变量--不应该重复调用函数，如果调用函数在循环体之中发生了变化，
  那这个常数也就不再是常数了。
  ------尽量少调用函数（就像求sin的级数的时候，多次调用函数也会让执行时间延长非常多的！） 
②多模块也是可以测试的！在调试的时候选定了一定长度的代码，那他进行的调试也只发生在这个区间内的呢！不必担心！ 
*/




 
  
