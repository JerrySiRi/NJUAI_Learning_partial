#include"stdio.h"
enum color{red=1,yellow,blue};
void print(enum color ball)
{
    switch(ball)
    {
        case red:printf("red");break;
        case yellow:printf("yellow");break;
        case blue:printf("blue");break;
    }
}
int main()
{
    enum color i,j,k;
    for(i=red;i<=blue;i=i+1)
    {
        for(j=red;j<=blue;j=(enum color)(j+1))
        {
            for(k=red;k<=blue;k=(enum color)(k+1))
            {
                if(i!=k&&k!=j&&j!=i)
                {
                    printf("%d",i+1);
                    print(i);printf("  ");print(j);printf("  ");print(k);
                    printf("\n");
                }
            }

        }


    }




}