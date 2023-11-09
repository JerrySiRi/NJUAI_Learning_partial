#include "stdio.h"
int main()
{
    int a[30][5];
    double b[30];
    int (*pa)[5];//此时只定义了一个指针哦！
    int i,j,sum;
    double *p;//【不用这个指针也是可以的，直接用下标访问呢！更加直观！！！】
    pa=a;p=b;//指针的赋值
    for(i=0;i<30;i++)
        for(j=0;j<5;j++)
            scanf("%d",*(pa+i)+j);
    //太巧妙啦！二维数组的指针访问方式，*(pa+i)是第几个“一维”数组，j是这个一维数组中第几个
    for(i=0;i<30;i++,p++)
    {
        for(j=0,sum=0;j<5;j++) 
            sum+=*(*(pa+i)+j);
        *p=(double)(sum/5);
    }
    for(i=0,p=b;i<30;i++,p++)
        printf("lf",*p);

}