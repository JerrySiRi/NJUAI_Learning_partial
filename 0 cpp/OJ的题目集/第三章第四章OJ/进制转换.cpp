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
void ershi(char m[])//�٣����ַ�������������ʱ����Ҫ�����ַ����ĳ��ȣ��������Ը���/0�Լ����㳤�� 
{
    int sum=0,d[8];
    for(int j=0; j<n; j++)	//�ڣ������ú�����ʱ�򣬲������¶���ĺ���֮�и�����������鸳ֵ 
    {
    	d[j]=(m[j]-'0')*pow(2,8-j-1);//����������ģ�Ӧ����2��8-j-1�Ĵη� 
									 //m[j]������ʽת����ת������ASCII�룡����������������֣� 
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
