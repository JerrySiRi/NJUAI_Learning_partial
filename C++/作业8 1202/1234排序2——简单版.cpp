#include <iostream>
using namespace std;
void swap(int &a,int &b)//
{
    int temp=a;
    a=b;
    b=temp;
}
void perm(int list[],int low,int high)
{
    if(low==high)
	{
        for(int i=0;i<=low;i++)
            cout<<list[i];
        cout<<endl;
    }
	else
	{
        for(int i=low;i<=high;i++)
		{
            swap(list[i],list[low]); 
            perm(list,low+1,high); 
            swap(list[i],list[low]);
        }
    }
}
int main()
{
	int list[]={1,2,3,4};
	perm(list,0,3);
	return 0;
}

