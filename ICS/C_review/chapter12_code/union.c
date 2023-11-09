#include"stdio.h"
int main()
{
    union emp
    {
        struct{
            int y;
            int x;
        }stc;
        int a;
        int b;
    }u;
    u.a=1;u.b=2;
    printf("a=%d b=%d",u.a,u.b);
    u.stc.x=u.a+u.b;
    printf("a=%d b=%d x=%d",u.a,u.b,u.stc.x);
    u.stc.y=u.a+u.b;
    printf("a=%d b=%d x=%d y=%d",u.a,u.b,u.stc.x,u.stc.y);
}