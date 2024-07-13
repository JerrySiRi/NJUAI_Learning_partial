#include <iostream>
using namespace std;
/*
题目：幸运的囚犯 (用数组实现）
题目描述：
m个囚犯围坐成一个圈，按照顺时针方向从1到m编号。然后从1号开始顺时针报数，报到n的囚犯出局
然后再从刚出局的囚犯下一个位置开始重新从1报数，如此重复，直到只剩下最后一个囚犯，这个幸运的囚犯将获得释放。(1<=n<=m)
输入：
输入包括两行。第一行是囚犯数目m和出局的报数n；第二行是编号为1到m的每个囚犯名字（不一定只是一个字母哦） 
输出：
幸运囚犯的名字
样例输入：
8 3
A B C D E F G H
样例输出：
G
*/
int main() 
{
	int a,b;//a是囚犯数目，b是出局的报数 
	cin >> a >> b;
	typedef char A[10];//A有9个元素，即每一个char[i]都得满足有不超过9个字符串长度呢！ 
	A ch[a+1];//A=char类型的数组 ，这个数组有a个元素 
	/*
	typedef的 
	*/
	for(int i=0;i<a;i++)
		cin >> ch[i];
	/*char ch[a+1];
	cin.getline(ch,a+1);//已经输入 ,ch[i]就是每个囚犯的姓名了 
	cin >> ch[a+1];
	*/
	//step1:所有人都在圈子里，全部赋值为true
	bool zaibuzai[a];
	for(int i=0;i<a;i++)
		 zaibuzai[i]=true;
	//step2:判断下一个报数的人是谁，是index+1再对a取余数 
	//如果下一个人在圈子里边（true），计数器+1，什么时候计数器达到n了，（计数器需要更新的！）变成false 
	//缺少了重要一步-循环条件==啥时候圈子里只剩下一个人了就不循环，大于一个人就循环
	int index=a-1;
	int shengyu=a;
	int c;
	while(shengyu>1)
	{
		int count=0;
		while(count<b)
		{
			c=(index+1)%a;
			if(zaibuzai[c])
				count++;
			index++;
		}
		//给出局的定义成false
		zaibuzai[c]=false;
		shengyu--;
	}
	//step3：完成之后只有一个人在里边，判断是谁
	int d;
	for(int i=0;i<a;i++)
		 {
		 if(zaibuzai[i])
		 	d=i;//下标是d的囚犯在圈子之中 
		 }
	cout << ch[d]; 
	return 0;
}








