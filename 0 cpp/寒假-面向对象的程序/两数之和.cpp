#include <iostream>
using namespace std;
/* 
给定一个整数数组 nums和一个整数目标值 target
你在该数组中找出 【和】为目标值 target的那两个整数，并返回它们的数组下标。
你可以假设每种输入只会对应一个答案。
但是，数组中同一个元素在答案里不能重复出现。
你可以按任意顺序返回答案。
【最后以-1结束！！！】 
示例 1：
输入：nums = [2,7,11,15], target = 9
输出：[0,1]
解释：因为 nums[0] + nums[1] == 9 ，返回 [0, 1] 。
示例 2：
输入：nums = [3,2,4], target = 6
输出：[1,2]
示例 3：
输入：nums = [3,3], target = 6
输出：[0,1]

提示：

2 <= nums.length <= 104
-109 <= nums[i] <= 109
-109 <= target <= 109
只会存在一个有效答案
进阶：你可以想出一个时间复杂度小于 O(n2) 的算法吗？

*/

/*
题目思路：没有给定数组确定的大小》》用链表。
第一个函数，往链表里边增加节点，并给他们的“下标”进行定义
第二个函数，多次循环，返回他们的下标 




*/	
struct Node
{
	int index; 
	int content;
	Node *next;
};
		
//【错误1】如果在public之中有返回值是Node类型的，一定在类定义外定义struct!不然无法识别呢！
 
class Stack
{
	public:
		Stack()//【构造函数之中可以多个数据成员同时定义的哦】 
			{head=NULL;tail=NULL;}//构造函数，给头结点和尾结点初始化 
		Node* insert();//往链表中添加新东西 
	//	void search(Node *head);//从链表之中寻找目标“下标” 
	private:
		Node *head,*tail;//指向头结点和尾结点的指针，得从尾部添加新节点 
		//【错误2：多个连续定义要小心！！！
		//尤其是指针类型的情况捏！如果tail前面不加上*，tail就只是一个Node类型的变量，而不是指针！】 
};

Node* Stack::insert()//从尾指针的位置插入节点 
{
	Node *p=new Node;
	int x;
	cin >> x;
	int xiabiao=0;
	while(x!=-1)
	{
		if(head==NULL)//一个元素都没有
		{
			head=p;
			p->content=x;
			p->next=NULL;	
			tail=p;
			p->index=xiabiao;
			xiabiao++;
		} 
		else//有一些元素了 
		{
			p->content=x;
			p->index=xiabiao;
			tail->next=p;
			p->next=NULL;
			tail=p;
			xiabiao++; 
		}
		cin >> x;
	}
	return head;
}
int main() 
{
	
	Stack a;
	a.insert();

	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	return 0;
}
