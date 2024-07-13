#include<iostream>
#include<cmath>
using namespace std;
const int n=8;
void shier(double a)//①出现小数的情况的时候，一定要定义double的！如果定义成了int型的0.几的都是0啦 
{
    cout <<"0.";
    for(int i=1; i<=5; i++)
    {
        a=a+a;    //放心写2*a，问题一定不会出现在这个位置的 
        if(a>=1)
        {
            cout << "1";
            a=a-1;
        }
        else
            cout << "0";
    }
}
void ershi(char m[])   //②把非字符串类型的数组传给函数的时候，需要定义一个数组+他其中有多少元素 
{					   //  但如果是字符串类型的数组的，就只能写数组类型+名称，不能给个数
					   //（编译器会根据/0自动得出个数） 
    int sum=0,d[8];
    for(int j=0; j<n; j++)//③数组用函数的时候一定是已经定义好的呢，不会在函数之中定义的
						  //函数直接认为这个数组已知啦，可以直接访问的! 
    {
    	d[j]=(m[j]-'0')*pow(2,8-j-1);//④输入的顺序是从最高位到最低位输入的 
        sum=sum+d[j];				   //小心要用+=的哦，逻辑要清晰 
    }
    cout<<sum;
}
int main()
{
    double b;
    char c[8];
    cin >> b;
    shier(b);
    cout << " ";
    for (int k=0;k<8;k++)  //⑤要对数组进行赋值的！ 
        cin>>c[k];
    ershi(c);				//访问字符串数组的时候只给有函数名就可以啦
							//访问int类型或者其他类型数组的情况的时候给出函数名以及他的个数就可以啦如sort(a,N) 
    return 0;
}
