#include <iostream>
#include "mystring.h"
using namespace std;
int main()
{ 
  char str1[20] = "hello ";//�пո��� 
  char str2[4] = "NJU";
  str_cat(str1,str2);                               
  //������֮��ĸ�ǰ���str1       //��str_cat���ܣ������ַ�����
   
  cout<<str1<<endl; //���: hello NJU
  
  int len = str_len(str1);                           
            //��str_len���ܣ��ַ������ȡ�
  char str3[len+1];
  str_cpy(str3,str1,len);									   
  // ǰ-�µĴ� ��-�������� ��-�����ĳ���//��str_cpy���ܣ���str3�п���str1��ǰlen���ַ���
   
  cout<<str3<<endl; // �����hello NJU 
  char str4[4] = "PKU";
  if(str_cmp(str2,str4)>0) 
  //��str_cmp���ܣ��Ƚ�str2��str4�Ĵ�С�����ǰ���ַ���С�ں�����ַ������Ǿ���С��0�ġ�
   
     cout<<str2;
  else
     cout<<str4;  //���:  PKU
     
  str_replace(str1,str2,str4); 
  //��str_replace���ܣ�ע����ڶ��str2����str1֮�п����ж��str2������str1���ҵ�str2������str4�滻��
   
  cout<<str1<<endl; // ���: hello PKU
  char str5[3] = "my";
  int index = str_find(str1,str4); 
  //��str_find���ܣ��ҵ�str4�ĵ�һ���ַ���str1�е�λ�á�
   
  str_insert(str1,index,str5); 
  //��str_insert���ܣ����±�index������str5���ı��str1 
   
  cout<<str1<<endl;  //����� hello myPKU
  to_lower(str1); 
  //��to_lower���ܣ� ��str1�е����д�д��ĸ��ΪСд�� 
  
  cout<<str1<<endl; //���: hello mypku
  return 0;
}
