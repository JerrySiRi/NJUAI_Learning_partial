#include <iostream>
#include <cstring>
using namespace std;
/* run this program using the console pauser or add your own getch, system("pause") or input loop */

class A
{
	public:
		A()
		{
			a=b=0;
			strcpy(c,"aaa");
		}
		A(int x1)
		{
			a=x1;
			b=0;
			strcpy(c,"bbb");
		}
		A(const char *p)
		{
			a=b=0;
			strcpy(c,p);
			//һ����дp�أ�pָ���λ�������ַ����ĵ�һ���ַ���ַ*** 
			//������p���Դ����������顣 
		}
		//�����1��[�����β���char *p��ʱ����о���ģ�ԭ��char *����ĺ����ǣ����Ҹ��ַ�������Ҫ�޸�����]
		//�������ϣ����Ǵ������������泣����û�����޸ĵġ����������ǿ���̨�����ѽ 
		//����˵���ȽϺ���İ취�ǰѲ��������޸�Ϊconst char *��
		// �����2�� strcpy��cstring���еĵڶ����βα�������const���͵ġ��������ָ��ҲӦ����const
		//��Ȼ��������Ϊ��strcoy֮�о��п��ܰѵڶ����ַ������޸���** 
		//�������˵����ĺ����ǣ����Ҹ��ַ�������ֻҪ��ȡ����
		void print();
		
	private:
		int a,b;
		char c[10];
};

void A::print()
{
	cout << a << b << c;
}

int main() 
{
	A b[5]={A(),A(1),A("abcd"),A(2),"xyz"};
	//�����еĶ�д��A(������)�ѣ����ᱨ���ա� 
	for(int i=0;i<5;i++)
		{b[i].print();cout <<endl;
		}
		
	return 0;
}
