#include <iostream>
#include <ctime>
#include <cstring>
using namespace std;

/*
1 ��С�ͳ��ʹ��ͳ����ŵ��ṹ����֮��ȥ
2 ʱ����԰��������ƣ�������Сʱ 
*/ 
struct Car//�ṹ���͵Ķ��� 
{
	bool da;
	bool xiao;
} ;
	//����1�������������ж���û�п���ĳ�λ
	 int free(char arr[],Car zaibuzai[]) 
	 {
	 		if(strcmp(arr,"d")==0)
	 		{
	 			for(int j=0;j<50;j++)
				{	
				 	if(zaibuzai[j].da==true)
						{return j+1;break;}
					else
						return 0;		
				}	
			}
	 		else if(strcmp(arr,"x")==0)
	 		{
	 			for(int j=0;j<50;j++)
	 			{
	 				if(zaibuzai[j].xiao==true)
	 					{return j+1;break;}	 
	 				else
	 					return 0 ;
				 }
			}
	 }
	 
	//����2���ж��ǲ�����ĩ���������ĩǮ������0.001
	bool weekend(char arr[])
	{
		if(arr=="Sat"||arr=="Sun")
			return true;
		else
			return false;
	 } 

