#include <iostream>
using namespace std;
/* 
����һ���������� nums��һ������Ŀ��ֵ target
���ڸ��������ҳ� ���͡�ΪĿ��ֵ target�����������������������ǵ������±ꡣ
����Լ���ÿ������ֻ���Ӧһ���𰸡�
���ǣ�������ͬһ��Ԫ���ڴ��ﲻ���ظ����֡�
����԰�����˳�򷵻ش𰸡�
�������-1������������ 
ʾ�� 1��
���룺nums = [2,7,11,15], target = 9
�����[0,1]
���ͣ���Ϊ nums[0] + nums[1] == 9 ������ [0, 1] ��
ʾ�� 2��
���룺nums = [3,2,4], target = 6
�����[1,2]
ʾ�� 3��
���룺nums = [3,3], target = 6
�����[0,1]

��ʾ��

2 <= nums.length <= 104
-109 <= nums[i] <= 109
-109 <= target <= 109
ֻ�����һ����Ч��
���ף���������һ��ʱ�临�Ӷ�С�� O(n2) ���㷨��

*/

/*
��Ŀ˼·��û�и�������ȷ���Ĵ�С����������
��һ��������������������ӽڵ㣬�������ǵġ��±ꡱ���ж���
�ڶ������������ѭ�����������ǵ��±� 




*/	
struct Node
{
	int index; 
	int content;
	Node *next;
};
		
//������1�������public֮���з���ֵ��Node���͵ģ�һ�����ඨ���ⶨ��struct!��Ȼ�޷�ʶ���أ�
 
class Stack
{
	public:
		Stack()//�����캯��֮�п��Զ�����ݳ�Աͬʱ�����Ŷ�� 
			{head=NULL;tail=NULL;}//���캯������ͷ����β����ʼ�� 
		Node* insert();//������������¶��� 
	//	void search(Node *head);//������֮��Ѱ��Ŀ�ꡰ�±ꡱ 
	private:
		Node *head,*tail;//ָ��ͷ����β����ָ�룬�ô�β������½ڵ� 
		//������2�������������ҪС�ģ�����
		//������ָ�����͵���������tailǰ�治����*��tail��ֻ��һ��Node���͵ı�����������ָ�룡�� 
};

Node* Stack::insert()//��βָ���λ�ò���ڵ� 
{
	Node *p=new Node;
	int x;
	cin >> x;
	int xiabiao=0;
	while(x!=-1)
	{
		if(head==NULL)//һ��Ԫ�ض�û��
		{
			head=p;
			p->content=x;
			p->next=NULL;	
			tail=p;
			p->index=xiabiao;
			xiabiao++;
		} 
		else//��һЩԪ���� 
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
