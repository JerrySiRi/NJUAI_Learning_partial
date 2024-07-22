#include <iostream>
using namespace std;
/*
用链表实现插入排序。
把待排序的数分成两个部分：A为已排好序的数，B为未排好序的数。
初始状态下，A中没有元素。该算法依次从B中取数插入到A中的相应位置，直到B中的数取完为止。
将排序算法用一个函数实现**，自定义main函数完成对该函数的调用测试。

思路：
①依次插入到对应位置 
先在B中找到最大的元素，给到A链表中。并且把B中元素的content改掉（最后用一个循环看还有没有元素） 
*/

/*
错误总结：
①二级指针的运用【在原来的链表之中进行删减**】
只要在原来已知的链表中操作都应该用二级指针的**

②重载与否【如果需要每次重置内容就应该放在循环内进行重载**】
本题中p_max没有放到循环之内
那么第一次找到链表中最大的节点之后，之后把这个节点删掉之后。
p_max这个指针没有定义了，所以无法访问p->content和循环中的content进行比较啦
所以p_max也无法被赋予新的值*
》》指针指向无效区间**

③寻找节点是第几个【i++的位置】
弄清if条件是干什么的：值相等之后再出循环的
弄清i++是干什么的：只要循环移动一次，就往后移了以为，那么他就位置一定要加一个的** 
*/
struct Node
{
	int content;
	Node* next;
};
extern Node *input();
extern Node *pai(Node **head1);
extern void output(Node *h);

int main() 
{
	cout << "请输入待排序的数字序列（以-1结束）"<<endl;
	Node *head1=input();//完成对B链表的输入操作**
						//完成对A中元素的插入 
	Node*head2=pai(&head1);
	output(head2);
	return 0;
}


Node *input() //从表头插入数据
{  Node *head=NULL; //头指针
	int x;
	cin >> x;
    while (x != -1)
	{ Node *p=new Node;
	   p->content = x;
	   if(head==NULL)
	   {
	   	p->next=NULL;
	    head=p;
	   }
	   else
	   {
	   p->next = head;
	   head = p;
	}
       cin >> x;
	}
	return head;
} 


Node *pai(Node **head1)
{
	Node *head2=NULL;
	while(*head1!=NULL)
	{Node *p_max=*head1;//【错误2：没有每次重载***】 
		//step1:找到最大的元素 
		for(Node *s=*head1;s!=NULL;s=s->next)//判断一下还有没有元素 
		{
		     //p_max指向最大的结点，初始化为p1。【就是用来记住位置在哪的***】 
			if (s->content > p_max->content)  p_max = s;//【交换地址就好啦**】 
	    //现在最大的元素就是p_max啦*
		}
		int i=0;
		for(Node *s=*head1;s!=NULL;s=s->next)
		{	i++;//【错误3：i++的位置是不是能在if里边】 
			if(s->content==p_max->content)
				break;
		}
		//step2: 进行新链表的赋值
		if(head2==NULL)
		{
			Node *t=new Node;
			t->content=p_max->content;
			t->next=NULL;
			head2=t;
		} 
		else
		{
			Node*t=new Node;
			t->content=p_max->content;
			t->next=head2;
			head2=t;
		}
		//step3:删除节点--循环的条件改变 
		if (i == 1) //要删除的结点是链表的第一个结点。
		{	
		Node *p=*head1; //p指向第一个结点。
		*head1 = (*head1)->next; //head指向第一个结点
						//的下一个结点。
		delete p; //归还被删除结点的空间。
		}
	else //要删除的结点不是链表的第一个结点。【删除最后一个和不是最后一个是一样的
											//最后一个的next被赋值成为了NULL了！】 
	{	
		Node *p=*head1; //p指向第一个结点。
		int j=1; //当前结点的序号，初始化为1
		while (j<i-1) //循环查找第i-1个结点
		{	p = p->next; //p指向下一个结点
			j++; //结点序号加1
		}
			Node *q=p->next; //q记住第i个结点。
			p->next = q->next; //把第i-1个结点的next
						  //指向第i+1个结点
			delete q;  //归还第i个结点的空间。
	}
	}	 
	return head2; 
}



void output(Node *h)//输出函数 
{ for (Node *p=h; p!=NULL; p=p->next)
	 cout << p->content << " ";
   cout << endl;
}
