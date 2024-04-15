#include<stdio.h>
#include<stdlib.h>
#include<string.h>
int main()
{
    char args_2[50]="0x55\0";
    char *args_1="10";
   int current;int i;
		char strr[20];
		strcpy(strr,args_2);
		sscanf(strr,"%x",&current);//【强制把输入的16进制的当前位置转化为十进制】
		int ultimate=current+atoi(args_1);
	printf("%d,%d",current,ultimate);
    char testhere[6]={0x31,0x38,0x34,0x32,0x36,0x33};
        unsigned int a[3];
        sscanf(testhere,"%2x%2x%2x",&a[0],&a[1],&a[2]);
        printf("%d,%d,%d",a[1],a[2]);
    char str[10]="0x55";
    char str1[10];
    sprintf(str1,"%x",atoi(str));
    printf()
}