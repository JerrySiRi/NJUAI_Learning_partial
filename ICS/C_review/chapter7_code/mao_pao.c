#include <stdio.h>
int main()
{
    int num;
    scanf("%d",&num);
    int str[num];//创建了数组
    for(int i=0;i<num;i++)
        scanf("%d",&str[i]);//给数组赋值
    for (int i=0;i<num;i++)
        for (int j=0;j<num-1-i;j++)//举一个例子，就知道j是到多大就可以不用比较啦！
        {
            if(str[j]>str[j+1])
            {
                int temp;
                temp=str[j];
                str[j]=str[j+1];
                str[j+1]=temp;
            }
        }
    for (int i=0;i<num;i++)
        printf("%d ",str[i]);

}