#include<iostream>
using namespace std;
/*
题目：判断矩阵是否存在鞍点（第五章练习）
题目描述：
输入一个n*n的矩阵（n<50），判断其是否包含鞍点。
鞍点是指矩阵中的一个位置，该位置上的元素在其所在行上最大**、列上最小**。
①需要用两个函数啦：先判断arr[i][j] 是不是第i行最大的
②是不是第j行最小的！ 
简单优化：效率更高--只有在行上是最大的，再进行判断列上是不是最小的 
矩阵的元素是整数。
输入说明：先输入n，随后是n*n个整数；
输出说明：存在鞍点，输出"yes"(直接不进行任何操作啦，就直接return 0喽)
没有鞍点，输出"no"
Sample 1:
Input:
5
2 6 87 78 89
1 7 45 94 65
3 8 98 34 88
10 9 65 67 50
3 10 3 5 49
Output:
yes

Sapmle 2 : 
Input:
2
1 4
5 3
Output:
no
*/

int main()
{
	int n;
	cin >> n;
	int arr[n][n];
	for(int i=0;i<n;i++)
		{
			for(int j=0;j<n;j++)
			{
				cin>>arr[i][j];//完成矩阵的输入 
			}
		}
	int i,j;
	for(i=0;i<n;i++)
		{
			for(j=0;j<n;j++)
			{
				int max=0;
				for(int p=1;p<n;p++)
				{
				if(arr[i][max]<=arr[i][p])	//判断第a行中最大的是谁，是不是p？ 
					max=p;					//现在最大值（可能会有重复）的下表是max了 
				}
				for(int p=0;p<n;p++)
				{
					if((arr[i][max]==arr[i][p])&&(p==j))
					{
						int min=0;
						for(int q=1;q<n;q++)
						{
							if(arr[min][j]>=arr[q][j])
								min=q;
						}
						for(int q=0;q<n;q++)
						{
							if((arr[min][j]==arr[q][j])&&(q==i))
								{
								cout <<"yes";
								return 0;
								}
						}
					}	
				}
			}
		}
	if((i==n)&&(j==n))
		cout <<"no";
	return 0;
}

/*
问题总结：
①现在还没有学指针，所以没有办法往函数里传入列不是常量的数组哦。哪怕n是已经输入的数字了也不可以
	只有const类型的才可以
②时刻想清楚：不满足循环的条件的时候是+1之后才出的循环
③！！思路错误修改代码的时候一定小心准确，在换思路的时候代码一定得微调，比如这道题之中的if一定要小心的
④如果历遍所有的情况都不成立，只需要在所有循环之外再来一次判断，是不是所有的都不成立才出来的，输出结果就可以啦！！ 


