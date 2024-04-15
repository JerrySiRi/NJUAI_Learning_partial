#include <stdio.h>
void han_nuo_ta(char ini, char vis,char dis, int n)//起始、途径、结束、挪动盘数
{
    if(n!=1)
    {
    
    han_nuo_ta(ini , dis, vis, n-1);
    printf("%c -> %c\n",ini, dis);
    han_nuo_ta(vis, ini, dis, n-1);
    }
    else
       printf("%c -> %c\n",ini, dis);
}
int main()
{
    char x='a',y='b',z='c';
    int n=3;
    han_nuo_ta(x,y,z,n);
}
