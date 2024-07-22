#include <iostream>
using namespace std;

	struct Node
{	int content;  //代表结点的数据
	Node *next;  //代表后一个结点的地址
}; 
extern Node *input(); //输入数据，建立链表，返回链表的头指针
extern void sort(Node *h); //排序
extern void output(Node *h); //输出数据
extern void remove(Node *h); //撤销链表

int main()//规律：链表的题目一般给函数的都是头指针*只要知道头指针在哪里，这个链表就都知道啦 
{  Node *head;
	head = input();
	sort(head);
	output(head);
	remove(head);
    return 0;
}

/*
Node *input() //从表尾插入数据【把链表从0》1++从1》更多的过程合二为一】 
{  Node *head=NULL, //头指针   
		  Node*tail=NULL; //尾指针
		  【现在链表为空】 
	int x;
	cin >> x;【开始输入数据**第一个数据的输入也得需要判断的】 
    while (x != -1)
	{ Node *p=new Node;
	   p->content = x; 
	   p->next = NULL;
	   if (head == NULL)【从0-1的过程】 
	      head = p;
       else
		tail->next = p;***else结束了* 
	
       tail = p;
       cin >> x;
	}
	return head;
}
*/
Node *input() //从表头插入数据【都采用这种方法哦***】 
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
	   //【包含了从0-1+1-更多的过程】
	   //最好是都给他拆开****从0-1再到1-更多，这样更加清楚*** 
	   /*
	   从0-1**
	   p中的next是NULL
	   head赋成了p
	   
	   从1-更多**
	    
	    。。。
		
		综上：只需要把head的初始值赋成NULL就可以啦*** 
	   */
	   head = p;
	}
       cin >> x;
	}
	return head;
} 

void sort(Node *h) //采用选择排序，小的往前放【进来的是头指针**】 
{  if (h == NULL || h->next == NULL) return;//【啥也没有*】 
    //从链表头开始逐步缩小链表的范围
	for (Node *p1=h; p1->next != NULL; p1 = p1->next)
	{ Node *p_min=p1; //p_min指向最小的结点，初始化为p1。【就是用来记住位置在哪的***】 
       //从p1的下一个开始与p_min进行比较 
	   for (Node *p2=p1->next; p2 != NULL; p2=p2->next)
	      if (p2->content < p_min->content)  p_min = p2;//【交换地址就好啦**】 
	    
	   if (p_min != p1) //交换结点的数据【只换数值不换位置】 
	   { int temp = p1->content;
          p1->content = p_min->content;
          p_min->content = temp;
	   }
	}
}

/*
上述循环中
初始化：给开始循环的节点以值
循环条件：一般循环到最后一个或者倒数第二个
循环更新：这个指针指向下一个指针** 

和数组中的选择排序不同的是：
①数组中如果选出来了最大的，放到最后，并且让n--

②但是链表中只取局部很困难***》》把小的往前放*** 
*/
void output(Node *h)
{ for (Node *p=h; p!=NULL; p=p->next)
	 cout << p->content << ',';
   cout << endl;
}

void remove(Node *h)
{	while (h != NULL)
	{	Node *p=h;
		h = h->next;
		delete p;
	}
}

