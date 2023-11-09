#include <iostream>
using namespace std;
//【没有自环的简单、有向图！】
int main(){
    int n;
    cin>>n;//一共多少个节点


    //【BUG！如果上来第一个结点就是没有任何出边呢？需要再来一个循环判断呢！】
    int target=1;
    for(int i=1;i<n;i++){
        cout<<'?'<<' '<<0<<' '<<i<<' '<<flush;
        int temp;
        cin >> temp;
        int flag=1;
        if(temp==1){//当前位置有边了 , i
            target=0;
            for(int j=1;j<n;j++){
                if(i!=j){
                    cout<<'?'<<' '<<j<<' '<<i<<' '<<flush;
                    int whe;
                    cin >> whe;
                    if(whe==0){
                        flag=0;
                        break;
                    }
                }
            }
            if(flag==1){//当前位i，满足入度为n-1的条件，再来看出度为0的时候呢！
                for(int j=0;j<n;j++){
                    if(i!=j){
                        cout<<'?'<<' '<<i<<' '<<j<<' '<<flush;
                        int if_0;
                        cin >> if_0;
                        if(if_0==1){
                            flag=0;
                            break;
                        }
                    }
                }
            }

            if(flag==1){
                cout<<'!'<<' '<<i<<' '<<flush;
                return 0;
            }
        }
    }
    if(target==1){//第一个结点没有出边
        for(int j=1;j<n;j++){
            cout<<'?'<<' '<< j<<' '<<0<<' '<<flush;
            int tempp;
            cin >>tempp;
            if(tempp==0){
                cout << '!' <<' '<< -1 <<' '<<flush;
                return 0;
            }
        }
        cout << '!' << ' ' << 0 <<' '<<flush;
        return 0;
    }
    cout << '!' <<' '<< -1 <<' '<<flush;
    return 0;
}