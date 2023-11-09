#include "stdio.h"

char * weekday[8]={"monday","tuesday","wednesday","thursday","friday","saturday","sunday",NULL};

int main()
{
    char string[20];
    scanf("%s",string);
    printf("%d",which(string));
}
int which(char ch[])
{
    int j;
    //发现问题，如果在for循环进行初始化的时候有多个变量，那么就不能直接创建+赋值了！
    char *p;//进行一个一个字符判断的
    for (int i=1;weekday[i]!=NULL;i++)
    {
        //C语言中两个字符串常量不能直接相等比较，只能一个一个字符进行判断！
        for(p=weekday[i], j=0;*p==ch[j];j++,p++)
        if(*p=='\0') return i;
    }


}