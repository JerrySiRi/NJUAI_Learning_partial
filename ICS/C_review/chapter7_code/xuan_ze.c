#include <stdio.h>
int main()
{
    int num;
    scanf("%d",&num);
    int str[num];
    for(int i=0;i<num;i++)
        scanf("%d",&str[i]);
    for (int i=0;i<num;i++)//从第一个位置开始，寻找是哪个是最小元素，并且和第一个位置换
        {
            int min=i;
            for(int j= i+1;j<num;j++)//内层循环用来找到最小元素，找到了之后，就用外层循环换位置！
            {//【bug：j必须能找到所有i之后的元素！】
                if (str[min]>str[j])
                    min=j;
            }
            //把min的位置和i的位置进行互换
            int temp=str[i];
            str[i]=str[min];
            str[min]=temp;
        }
    for(int i=0;i<num;i++)
        printf("%d ",str[i]);

}