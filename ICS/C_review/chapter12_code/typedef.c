#include "stdio.h"
typedef char ch[20];
int main()
{
    ch ch1[3];//有3个可以存放20个字符的字符串数组
    for(int i=0;i<3;i++)
    {
        scanf("%s",&ch1[i]);
    }
    for(int i=0;i<3;i++)
    {
        printf("%s",ch1[i]);
    }
}