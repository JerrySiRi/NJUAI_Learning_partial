#include"stdio.h"
#include"string.h"
struct person
{
    char name[20];
    int count;
};    
struct person leader[4]={{"Li",0},{"Wang",0},{"Ma",0},{"Zhu",0}};
int main()
{
    int i,j;
    char vote_name[20];
    for(i=1;i<=3;i++)
    {
        scanf("%s",vote_name);
        for(j=0;j<4;j++)
            if(strcmp(vote_name,leader[j].name)==0)
                leader[j].count++;
    }
    for(i=0;i<4;i++)
        printf("%5s:%d\n",leader[i].name,leader[i].count);
}