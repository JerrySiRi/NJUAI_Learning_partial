#include <iostream>
using namespace std;
/*
m个囚犯围坐成一个圈，按照顺时针方向从1到m编号。
然后从1号开始顺时针报数，报到n的囚犯出局，然后再从刚出局的囚犯下一个位置开始重新从1报数.
如此重复，直到只剩下最后一个囚犯，这个幸运的囚犯将获得释放。(1<=n<=m)

输入：
输入包括两行。第一行是囚犯数目m和出局的报数n；第二行是编号为1到m的每个囚犯名字

输出：
幸运囚犯的名字[是一个字符串的，不一定是一个字母捏**]

样例输入：
8 3
A B C D E F G H

样例输出：
G
*/


//代码二：链表解决

struct Node
{	int no;  //小孩的编号
	Node *next; //指向下一个小孩的指针
};
int main()
{	int m, //用于存储要报的数
		n, //用于存储小孩的个数
		num_of_children_remained; //用于存储圈子里
						       //剩下的小孩个数
	cout << "请输入小孩的个数和要报的数：";
	cin >> n >> m;
 //构建圈子
	Node *first,*last; //first和last用于分别指向第一个和
				    //最后一个小孩
	first = last = new Node;  //生成第一个结点
	first->no = 0; //第一个小孩的编号为0
	for (int i=1; i<n; i++) //循环构建其它小孩结点
	{	Node *p=new Node;  //生成一个小孩结点
		p->no = i; //新的小孩结点的编号为i
		last->next = p; //最后一个小孩的next指向新生成
                                //的小孩结点
		last = p; //把新生成的小孩结点成为最后一个结点
	}
	last->next = first;  //把最后一个小孩的下一个小孩
 				      //设为第一个小孩，构成圈子

//【先创建一个单链表，最后再把圈子首尾连起来】***
//开始报数【只要链表中有这个节点，那么他就在***（如果出去了，删除节点就可以啦）】 
	num_of_children_remained = n;  //报数前的圈子中小孩个数
	Node *previous=last;  //previous指向开始报数的前一个小孩
	while (num_of_children_remained > 1)
	{	for (int count=1; count<m; count++)  //循环m-1次【注意count=1】【如果设置成释放previous指向的节点
	//下次循环previous就指向一个未知的空间了！！！！！！！！（所以释放的时候一定拿一个后面的指针指向要释放的*）】 
			previous = previous->next;
		//循环结束时，previous指向将要离开圈子的小孩的前一个小孩
		Node *p=previous->next;  //p指向将要离圈的小孩结点
		previous->next = p->next;  //小孩离开圈子
		delete p;  //释放离圈小孩结点的空间
		num_of_children_remained--;  //圈中小孩数减1
	}
	
	//输出胜利者的编号
	cout << "The winner is No." << previous->no << "\n";
	delete previous;  //释放胜利者结点的空间
	return 0;
}
 
 
 
 
 
 
 
 
 
 
 
 
 
 
//代码一：复习数组（数组做法**） 
/*
int main() 
{
	int m,n;
	cin >> m >> n;
	int k=m;
	typedef char A[10];
	A name[1][m];//一共有m个人***【此处二维数组不是很明显的***】 
	//现在其实也可以用结构类型数组jail A[m];来表示的**
	for(int i=0;i<m;i++)
		cin >> name[1][i];
	bool zai[m];//现在全都在 
	for(int i=0;i<m;i++)
		zai[i]=true;
		
	int index=m-1;
	//下一个要报数的位置是(index+1)%m 如果是ture就count++ 
	while(k>1)//m可不能动呢，下面每次计算0-m-1的范围都是需要原本的m呢 
	{
		int count=0;
		int b;
		while(count<n)
		{
			b=(index+1)%m;
			if(zai[b])  count++;
			index++;
		}
		zai[b]=false;
		k--;
	}
	int i;
	for(i=0;i<m;i++)
	{
		if(zai[i]==true) break;
	}
	cout<<name[1][i];

	return 0;
}
*/
