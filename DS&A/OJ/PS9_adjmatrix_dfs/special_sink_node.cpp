#include <iostream>
#include <cassert>
using namespace std;
int main(){
    int n;
    cin >> n;

    int i=0,j=0;
    int temp=0;
    while((i<n) && (j<n)){//【现在BUG！频繁的cout和cin导致时间超时.而不是在while循环上】
        if(i!=j){
            cout<<'?'<<' '<<i<<' '<<j<<' ';
            cout.flush();
            cin >> temp;
            (temp==0)?(j++):(i++);
        }
        else
            j++;
        
    }
    
   // cout<<"okok"<<endl;
    //行溢出---所有行对应的顶点都被排除。---直接返回-1
    //列溢出---所有列对应的顶点都被排除。---需要再判断
    //【再判断 i 的时候是不是是目标结点就可以啦】
    if(i==n){
        cout << '!'<<' '<<-1<<' ';
        cout.flush();
        return 0;
    }

    for(int t=0;t<n;t++){
        if(t!=i){
            cout<<'?'<<' '<<i<<' '<< t<<' ';
            cout.flush();
            int temp1;
            cin >>temp1;
            if(temp1==1){
                cout << '!'<<' '<<-1<<' ';
                cout.flush();
                return 0;
            }


            cout << '?'<< ' '<<t<<' '<<i<<' ';
            cout.flush();
            int temp2;
            cin>>temp2;
            if(temp2==0){
                cout <<'!'<<' '<<-1<<' ';
                cout.flush();
                return 0;

            }
        }
    }
    
    cout <<'!'<<' '<<i<<' ';
    cout.flush();
    return 0;
}