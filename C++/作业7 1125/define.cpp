#include <iostream>
#include <ctime>
#include <cstring>
using namespace std;

/*
1 把小型车和大型车都放到结构类型之中去
2 时间可以按照秒来计，而不是小时 
*/ 
struct Car//结构类型的定义 
{
	bool da;
	bool xiao;
} ;
	//函数1：汽车进场，判断有没有空余的车位
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
	 
	//函数2：判断是不是周末，如果是周末钱数各加0.001
	bool weekend(char arr[])
	{
		if(arr=="Sat"||arr=="Sun")
			return true;
		else
			return false;
	 } 

