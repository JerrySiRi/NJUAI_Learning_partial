#include <stdio.h>
int sum(int n)
{
    static int s = 0;
    s=s+n;
    return s;
}
int main()
{
    int i;
    for(i=1;i<=5;i++)
    {
        printf("%d ",sum(i));
    }
}
