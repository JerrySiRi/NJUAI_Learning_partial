#include <iostream>
using namespace std; 
/* run this program using the console pauser or add your own getch, system("pause") or input loop */
/*
用递归的方法编程实现：用1~4这4个数字中，组成4位数，每位数字不重复，输出所有符合的数。
》》进阶版：用1-n这n个数字，组成n位数，每位数字不重复，输出所有符合条件的数字
 
大概思路：
1、需要多次输出的，肯定不能用int了哦，一定要用void的呢
2、这道题每次调用需要输出多种情况，之前递归函数调用的时候每次调用只需要输出一种结果！【如果采用插空的方法】
 
3、采用的方法不能产生重复，递归规律的设定就应该满足不重复（排除重复可不容易！） 
*/
void queue(int arr[],int low,int high)//数组中下标最小的是low，下标最大的是high（本题是0和3） 
{
    if(low==high)
	{
        for(int i=0;i<=low;i++)
            cout<<arr[i];
        cout<<endl;
    }
	else
	{
        for(int i=low;i<=high;i++)//在此循环之中，high的值不发生改变***
		{
			int temp=arr[low];//交换数组中两个元素的值 
			arr[low]=arr[i];
			arr[i]=temp;
			
            queue(arr,low+1,high); 

            int temp1=arr[low];//交换数组中两个元素的值,一定不要出现重载的行为，能重新定义就一定重新定义一个！ 
			arr[low]=arr[i];
			arr[i]=temp1;
        }
    }
}

int main() 
{
	int arr[4];
	for(int i=1;i<5;i++)
		arr[i-1]=i; 
	queue(arr,0,3);
	return 0;
}






