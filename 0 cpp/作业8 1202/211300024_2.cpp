#include <iostream>
using namespace std; 
/* run this program using the console pauser or add your own getch, system("pause") or input loop */
/*
�õݹ�ķ������ʵ�֣���1~4��4�������У����4λ����ÿλ���ֲ��ظ���������з��ϵ�����
�������װ棺��1-n��n�����֣����nλ����ÿλ���ֲ��ظ���������з�������������
 
���˼·��
1����Ҫ�������ģ��϶�������int��Ŷ��һ��Ҫ��void����
2�������ÿ�ε�����Ҫ������������֮ǰ�ݹ麯�����õ�ʱ��ÿ�ε���ֻ��Ҫ���һ�ֽ������������ò�յķ�����
 
3�����õķ������ܲ����ظ����ݹ���ɵ��趨��Ӧ�����㲻�ظ����ų��ظ��ɲ����ף��� 
*/
void queue(int arr[],int low,int high)//�������±���С����low���±�������high��������0��3�� 
{
    if(low==high)
	{
        for(int i=0;i<=low;i++)
            cout<<arr[i];
        cout<<endl;
    }
	else
	{
        for(int i=low;i<=high;i++)//�ڴ�ѭ��֮�У�high��ֵ�������ı�***
		{
			int temp=arr[low];//��������������Ԫ�ص�ֵ 
			arr[low]=arr[i];
			arr[i]=temp;
			
            queue(arr,low+1,high); 

            int temp1=arr[low];//��������������Ԫ�ص�ֵ,һ����Ҫ�������ص���Ϊ�������¶����һ�����¶���һ���� 
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






