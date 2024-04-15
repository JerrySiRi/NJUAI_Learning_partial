
#include <iostream>
#include <vector>
using namespace std;

/*

*/

typedef struct{
    long long int value=0;//当前位置的最优解的值
    int num=0;//r[i][j]的时候，长度j切了几刀【唯一会有重叠的地方！！！】
    bool valid_bit=true;
} Pro;


int main(){
    int t,n,c;
    cin>>t;//测试的数量一共t个
    for(int l=0;l<t;l++){
        cin>>n>>c;//当前测试  【绳子的长度为n】 【每次切割消耗c】

        //step1:初始化--price、limit、r
        vector<long long int> price(n+1),limit(n+1);
        price[0]=0;limit[0]=0;
        for(int p=1;p<n+1;p++)//每段长度为0,1,2，。。。，n的绳子的收益
            cin>>price[p];
        for(int p=1;p<n+1;p++)//每段长度为0,1,2,..,n的绳子的收益
            cin>>limit[p];
        Pro r[n+1][n+1];//当前长度是0,1,2,...,n.当前可切长度是0,1,2,...,n【保证可切长度小于当前长度】
        //for(int a=0;a<n;a++)
            //for(int b=a+1;b<n;b++)
                //r[a][b].valid_bit=false;



        for(int i=1;i<n+1;i++){//【求解r[i][j]的问题】   i-当前长度  j-当前可以切完产生的最大长度
    
            for(int j=1;j<=i;j++){
                long long int q=-1;//初始化
                int target=-1;//最好收益切的长度 target=0代表不切。其他时候产生两段长度分别为target和i-target

                //situation1:不切的时候,只有i==j的时候才可以不切
                if(limit[i]>=1 && i==j){
                    q=price[i];
                    target=0;
                }

                //situation2：k-当前选择切的长度  k=1，，，j
                //for循环条件
                /*
                 1- 当前切完产生的长度小于j  
                 2- 切完之后有一段不能再切了，他的limit一定>1  
                 3- k尽管可以等于j，j可以等于i，但是k==j==i的情况不能出现。即切了一段长度为i的。
                    下面都是要-c的，不能混入不切割的！
                */
               //【【【【【【修改valid-bit】】】】】】
                for(int k=1; k<=j&&k!=i ;k++){
                    if(i-k<k && (limit[k]<1 || r[i-k][i-k].valid_bit==false))//交叉的长度，之前使用次数+本次的一次
                        continue;
                    else if(i-k>=k&& (limit[k]<1 || r[i-k][k].num+1>limit[k] || r[i-k][k].valid_bit==false) )
                        continue;
                    long long int temp=0;
                    if(k>i-k)
                        temp=price[k]+r[i-k][i-k].value-c;
                    else
                        temp=price[k]+r[i-k][k].value-c;//切的时候--此时才-c
                    if(q<temp){//此时新的切法带来的收益更高
                        q=temp;
                        target=k;
                    }         
                }
                if(target==-1){
                    r[i][j].valid_bit=false;//【前面的if条件没有一个能进去的】
                }
                else{
                    //所有情况判断完了，更新输入r。更新limit数组
                    r[i][j].value=q;
                    if(target==0)//切了长度的最大值,且本身长度就是就是j
                        r[i][i].num=1;
                    else if(target==j)//切了一段不能再被切的长度target【只要新的长度不是可以达到的长度上限--就无须更新】
                        r[i][j].num+=(r[i-j][j].num+1);
                }               
            }

        }
        
        cout << r[n][n].value <<endl;

    }

}