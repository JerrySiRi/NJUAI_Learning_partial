#include<iostream>
#include<cmath>
using namespace std;
const int n=8;
void shier(double a)
{
    cout <<"0.";
    for(int i=1; i<=5; i++)
    {
        a=a+a;
        if(a>=1)
        {
            cout << "1";
            a=a-1;
        }
        else
            cout << "0";
    }
}
void ershi(char m[])//①：把字符串传给函数的时候不需要给出字符串的长度，函数可以根据/0自己计算长度 
{
    int sum=0,d[8];
    for(int j=0; j<n; j++)	//②：当调用函数的时候，不能在新定义的函数之中给输进来的数组赋值 
    {
    	d[j]=(m[j]-'0')*pow(2,8-j-1);//从左到右输入的，应该是2的8-j-1的次方 
									 //m[j]进行隐式转换是转换成了ASCII码！而不是它本身的数字！ 
        sum=sum+d[j];
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
    for (int k=0;k<8;k++)
        cin>>c[k];
    ershi(c);
    return 0;
}
