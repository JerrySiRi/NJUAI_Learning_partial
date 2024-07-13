#include <iostream>
using namespace std;
//加密规则是，单词中的每个字母用字母表中该字母后的第四个字母替代。
//例如：小写字母a用e替换，z用d替换，大写字母F用J替换，W用A替换。
//输入单词用’#’结束，在同一行输出就行，输出加密后的结果，并且结果后不用输出换行。
//找到循环：输入以字符串的形式输入，每次都会输入的，而且输入的个数不定 
int main()
{
 	char ch,ch1,ch2;
 	for(cin>>ch;ch!='#';cin >> ch)
 		{
		 	if('a'<=ch && ch <='v')
		 		ch1=ch + 4;
			else if('w'<=ch && ch <='z')
				ch1=ch -'z'+'a'+3;
			else if('A'<=ch && ch <='V')	
		 		ch1=ch + 4;
		 	else if('W'<=ch && ch <='Z')
				 ch1=ch-'Z'+'a'+3;
		 	cout << ch1;
		} 
	return 0;
}

/*ASCII码！a并不是从0开始的哦 
①把z减掉之后再把a加上来
②一定要仔细的！ +3还是+4
-z+a之后是在a之前的东西呢，找个例子试一下就知道是+3啦！ 
