#include <iostream>
#include <cstring>
using namespace std;
/*
��Ŀ��ɾ���Ӵ�

��Ŀ������

���ʵ�֣����ַ�����ʵ�֣�������string�ࣩ��
���������ַ���A,B��
1���A�а���B��[����Ӵ�]��A���޳�B�����������B�Ľ����
2���A��û�а���B�����A��
˵������1�������ַ����������հ׷�����2�����ս���в�����B��

����˵������һ��������A,B�����ַ�����A��B֮���ÿո�ָ���

���˵��������޳�����ַ���


Sample:

input:

abcdabcd abc

output:

dd

����һ��������
bbcc bc 
*/
int main()
{
	char ch1[100],ch2[100];
	cin >>ch1;
	cin >>ch2;
	int a=strlen(ch1);
	int b=strlen(ch2);
	for(int i=0;i<=a-b;i++)	
	{
		bool huan=false;
		if(ch1[i]==ch2[0])
		{
			int j;
			for(j=1;j<b;j++)
			{
				if(ch1[i+j]==ch2[j])	
					;
				else break;
			}
			//��ѭ�����ֿ��ܣ���һ��j=b�����������ҵ����Ӵ��ˡ��ڶ���û���ҵ���j������b 
			if(j==b)//��ʱi���±��ˣ�
			{
				huan=true;
						//�������±괢����ch3���� 
						//�뷨һ�������±�
						//�뷨����ֱ�ӽ���ɾ������,���ø��ǵķ������������Ƶ����һ��λ��
				for(int p=i;p<=a-b;p++)
				{
					ch1[p]=ch1[p+b];
				}
				a=a-b;
				if(a==0)
					ch1[0]='\0';
			}
		}
		if(huan)
			i=-1;
	}
	cout <<ch1;
	return 0;
}
/*
����
������ 
*/
