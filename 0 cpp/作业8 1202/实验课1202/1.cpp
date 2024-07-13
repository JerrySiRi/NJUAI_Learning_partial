#include <iostream>
using namespace std;
/*
定1议2的思想别忘记啦，内层循环把外层循环的值当做定值的哦
空格和换行别多啦

题目描述：

某市按阶梯收取水费：
第一阶梯（每立方米1元）：年用水量小于等于200立方米；
第二阶梯（每立方米2元）：年用水量大于200，小于等于300立方米；
第三阶梯（每立方米4元）：年用水量大于300立方米。
输入一户人家2020年每个月的用水量，编程实现输出这户人家每月的水费是多少。说明：该户人家每月的用水量小于100立方米。

输入说明：在一行中输入12个月用水量，每月数据之间用空格分隔

输出说明：在一行中输出12个月的水费，每月费用之间用空格分隔

Sample:

input:

20 21 22 23 24 25 26 27 28 29 30 31

output:

20 21 22 23 24 25 26 27 44 58 60 74 
*/ 
int main()
{
	int arr[12];
	for(int i=0;i<12;i++)
		cin >> arr[i];

	int fee[12];
	for(int i=0;i<12;i++)
		fee[i]=arr[i];
	int sum=0;
	for(int i=0;i<12;i++)
	{
		sum+=arr[i];
		if(sum<=200) 
			fee[i]=arr[i];
		
		else if(sum>200&&sum<=300)
		{if(sum-arr[i]<200)
			fee[i]=(200-sum+arr[i])+2*(sum-200);
		else
			fee[i]=2*arr[i];
		}
		else if(sum>300)
		{	if(sum-arr[i]<300)
				fee[i]=2*(300-sum+arr[i])+4*(sum-300);
			else
				fee[i]=4*arr[i];
		}
			
	}
	for(int i=0;i<12;i++)
		cout << fee[i]<<" ";
	return 0;
}
