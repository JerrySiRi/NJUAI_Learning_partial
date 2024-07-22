#include <iostream>
using namespace std;
//����1��str_len�����ַ������ȣ����������ĳ��ȣ�����\0��
int str_len(char str[])
{
	int count=0;
	while(str[count]!='\0')
		count++;
	return count;
} 
 
 //����2��str_cat�����ַ�������һ���ո�,��str_cat(str1,str2),������֮��ĸ���str1
 void str_cat(char str1[],char str2[])
{
	int a;
	int len_1=str_len(str1),len_2=str_len(str2);
	a=len_1+len_2;//�ܳ���
	for(int i=len_1;i<a;i++)
		str1[i]=str2[i-len_1];
	str1[a]='\0'; 
} 



//����3��str_cpy��str3�п���str1��ǰlen���ַ�����str_cpy(str3,str1,len);ǰ-�µĴ� ��-�������� ��-�����ĳ���
void str_cpy(char str3[],char str1[],int len)
{
	for(int i=0;i<len;i++)
		str3[i]=str1[i];
} 

//����4��str_cmp���ܣ��Ƚ�str2��str4�Ĵ�С�����ǰ���ַ���С�ں�����ַ������Ǿ��Ǵ���0��
bool str_cmp(char str2[],char str4[])
{
	int a=str_len(str2);//ֻ��Ҫ����С���ַ�����Ϊѭ�����޾Ϳ����� 
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

//����5��str_replace���ܣ�ע����ڶ��str2����str1֮�п����ж��str2������str1���ҵ�str2������str4�滻
//str_replace(str1,str2,str4)���������str1��ֵ
void str_replace(char str1[],char str2[],char str4[])
{
	int a=str_len(str1),b=str_len(str2);
	int i;
	for(i=0;i<=a-b;i++)
	{
		if(str1[i]==str2[0])//Ŀǰ��i=6����if 
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
	//����ҵ��ˣ���str1�е��±����i���ӵ�iΪ��ʼ�滻��str4��str1�ĳ�����֪�㹻����
	for(int k=i;k-i<str_len(str4);k++)
	{
		str1[k]=str4[k-i];	
	} 
} 


 
 //����6��str_find���ܣ��ҵ�str4�ĵ�һ���ַ���str1�е�λ�ã���֤str1��һ����str4�Ĵ��� 
 //str_find(str1,str4)��Ҫ�з���ֵ��
 int str_find(char str1[],char str4[])
{
	int i=0;
	while(str1[i]!=str4[0])
	{
		i++;
	}
	return i;
} 

//����7��str_insert���ܣ����±�index������str5
//str_insert(str1,index,str5)
void str_insert(char str1[],int index,char str5[])
{
	char ch[20];//���ᱻ�ı���м��� 
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
 
 //����8��to_lower���ܣ� ��str1�е����д�д��ĸ��ΪСд
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
�����壺 
���ֵĴ���ԭ��
���ַ�������̫�࣬���׻�������str2д����str4��
��ѭ�������ɲ����Ե���û�и�������´ξ�����Ҫ�����������������ȡ��������ñ�дһд��һ�θ㶨��
�۶��ѭ��Ҫ�õ���һ��ѭ����Ľ������Ҫ�������һ�ε�ѭ��������ʲô����k-iС�ڻ���kС���أ� 
*/  

/*
��������
���ֵĴ���ԭ��
��������ú������ص���һ��������--��Ӧ���ظ����ú�����������ú�����ѭ����֮�з����˱仯��
  ���������Ҳ�Ͳ����ǳ����ˡ�
  ------�����ٵ��ú�����������sin�ļ�����ʱ�򣬶�ε��ú���Ҳ����ִ��ʱ���ӳ��ǳ���ģ��� 
�ڶ�ģ��Ҳ�ǿ��Բ��Եģ��ڵ��Ե�ʱ��ѡ����һ�����ȵĴ��룬�������еĵ���Ҳֻ��������������ڵ��أ����ص��ģ� 
*/




 
  
