
#include <iostream>
#include <vector>
#include <cassert>
using namespace std;

/*
1
3 10
100 1 1
3 3 3

1
3 0
1 1 1
1 1 1

1
3 2
100 100 1
0 1 1


1
3 2
100 100 100
3 3 3

1 
5 20
23 32 43 1 53
5 5 5 5 5 


1
3 172635
87263525 8463525 72635362
3 3 3

3
3 10
100 1 1
3 3 3
3 0
1 1 1
1 1 1
3 2
100 100 1
0 1 1


1
3 10
1 1 1
3 3 3 
*/


typedef struct{
    long long int value=0;//当前位置的最优解的值
    bool valid_bit=true;
} Pro;


typedef struct{
    long long int temp_value=0;
    bool revised=false;
} Re;



int main(){
    int t,n,c;
    cin>>t;//测试的数量一共t个
    for(int l=0;l<t;l++){
        cin>>n>>c;//当前测试  【绳子的长度为n】 【每次切割消耗c】

        long long int price[n+1];
        int limit[n+1];
        price[0]=0;limit[0]=0;
        for(int p=1;p<n+1;p++)//每段长度为0,1,2，。。。，n的绳子的收益
            cin>>price[p];
        for(int p=1;p<n+1;p++)//每段长度为0,1,2,..,n的绳子的收益
            cin>>limit[p];
        Pro r[n+1][n+1];//参数1：可以使用前i中长度拼长度为j  参数2：拼成长度为j的


        //step1：初始化
        for(int i=1;i<n+1;i++)//第一行初始化
            r[0][i].valid_bit=false;

        for(int j=0;j<n+1;j++){//第二行初始化
            if(j<=limit[1])
                r[1][j].value=j*(price[1]-c);
            else
                r[1][j].valid_bit=false;
        }

        //step2：动态规划啦
        for(int i=2;i<n+1;i++){
            for(int j=0;j<n+1;j++){
                int range_up=(j/i<limit[i])?(j/i):limit[i];
                Re q;
                q.temp_value = -c;
                for(int k=0;k<=range_up;k++){
                    if(r[i-1][j-k*i].valid_bit==false)
                        continue;
                    if(k*(price[i]-c)+r[i-1][j-k*i].value >= q.temp_value){
                        q.temp_value=k*(price[i]-c)+r[i-1][j-k*i].value;
                        q.revised=true;
                    }
                }
                if(q.revised==false)
                    r[i][j].valid_bit=false;
                else
                    r[i][j].value=q.temp_value;
            }
        }

        cout<< r[n][n].value+c << endl;
    }

}