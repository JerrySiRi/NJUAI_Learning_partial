#include <iostream>
#include "mystring.h"
using namespace std;
int main()
{ 
  char str1[20] = "hello ";//有空格了 
  char str2[4] = "NJU";
  str_cat(str1,str2);                               
  //把连接之后的给前面的str1       //【str_cat功能：连接字符串】
   
  cout<<str1<<endl; //输出: hello NJU
  
  int len = str_len(str1);                           
            //【str_len功能：字符串长度】
  char str3[len+1];
  str_cpy(str3,str1,len);									   
  // 前-新的串 中-被拷贝的 后-拷贝的长度//【str_cpy功能：往str3中拷贝str1的前len个字符】
   
  cout<<str3<<endl; // 输出：hello NJU 
  char str4[4] = "PKU";
  if(str_cmp(str2,str4)>0) 
  //【str_cmp功能：比较str2和str4的大小，如果前面字符串小于后面的字符串，那就是小于0的】
   
     cout<<str2;
  else
     cout<<str4;  //输出:  PKU
     
  str_replace(str1,str2,str4); 
  //【str_replace功能：注意存在多个str2（在str1之中可能有多个str2），在str1中找到str2，并用str4替换】
   
  cout<<str1<<endl; // 输出: hello PKU
  char str5[3] = "my";
  int index = str_find(str1,str4); 
  //【str_find功能：找到str4的第一个字符在str1中的位置】
   
  str_insert(str1,index,str5); 
  //【str_insert功能：在下标index处插入str5】改变的str1 
   
  cout<<str1<<endl;  //输出： hello myPKU
  to_lower(str1); 
  //【to_lower功能： 将str1中的所有大写字母改为小写】 
  
  cout<<str1<<endl; //输出: hello mypku
  return 0;
}
