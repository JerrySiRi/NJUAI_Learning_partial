#include"stdio.h"
#include"string.h"
int main()
{
    char str1[80],str2[80],*p1,*p2;
    gets(str1);//可以包含空格的，接进来一个字符串
    p1=str1;
    p2=str2;
    while((*p2=*p1)!='\0')//此时这个语句之中①完成了赋值 ②完成了条件判断！
    {
        p1++;p2++;
    }
    printf(str2);

}