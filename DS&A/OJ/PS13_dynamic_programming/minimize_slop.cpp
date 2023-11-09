#include <iostream>
using namespace std;

/*
1
3 5
2 3 1

1
3 6
2 3 1
*/
typedef struct{
    long long int value=0;
    bool revised=false;
}Property;

int main(){
    long long int t;
    cin>>t;
    for(long long int wai=0;wai<t;wai++){
        long long int n,L;
        cin >> n >> L;
        long long int l[n+1];
        l[0]=0;
        for(long long int p=1;p<n+1;p++)
            cin>>l[p];
        long long int cost[n+1];
        cost[0]=0;


        for(int k=n;k>=1;k--){//【没问题】
            long long int temp_1=0;
            for(int a=k;a<=n;a++)//算从k到n的所有单词长度【包含k的呢！】
                temp_1+=l[a];
            if(temp_1+n-k<=L){//step1：初始化1【k-n是这么多单词至少含有的空格数、temp_1是这些单词的长度】
                cost[k]=0;//此时的k，可以让从k-n的所有单词排在一行之中。而且在最后一行，消耗就是0啦！
                continue;
            }
            Property q;//初始化2：动态规划中的中间变量，保存最小值的。初始化revised是false！

            for(int j=0;j<n-k;j++){//【整个序列看成1-k-n。1-k是已经解决的了。k+1-n是将要解决的】
                long long int temp_2=0;
                for(int m=0;m<=j;m++)//
                    temp_2+=l[k+m];
                long long int temp_cost=temp_2+(j+1)-1;
                if(temp_cost<=L ){
                    if(q.revised==false)
                        {q.value=(L-temp_cost)*(L-temp_cost)*(L-temp_cost)+cost[k+j+1];q.revised=true;}
                    else if((L-temp_cost)*(L-temp_cost)*(L-temp_cost)+cost[k+j+1] < q.value )
                        q.value=(L-temp_cost)*(L-temp_cost)*(L-temp_cost)+cost[k+j+1];
                    

                }
            }
            cost[k]=q.value;//【可能有点问题，在j=1=n-k的时候，没有进for循环就直接赋值cost[k]了】
        }
        cout<<cost[1]<<endl;
    }

}