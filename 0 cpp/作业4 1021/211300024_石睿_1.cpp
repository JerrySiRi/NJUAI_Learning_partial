#include <iostream>
using namespace std;
/* run this program using the console pauser or add your own getch, system("pause") or input loop */
//  ���ʵ�֣��Ӽ�������һ���ַ����У����ַ���#���������������еġ�>=�����м�����
int main()
{
	cout << "������һ���ַ����У���#������" << endl;
	char xulie,arr1,arr2;int i=0;
	cin  >> xulie;										//��Ҫ������һ��xulie��������while���жϡ�
	while(xulie !='#')									//����Ȼ�����ѭ���ж������cin����һ�ε�xuelie�޷��жϣ�  
	{
		arr1 = xulie;
		cin  >> xulie;
		arr2 = xulie;									//��ʱ���Բ���Ҫ�ٶ����ˣ�ֱ����arr1���������xulie�ж� 
		if(arr2 == '#') break;
		else if(arr1 == '>'&& arr2 == '=')				//��������һ��arr=='#'��Ϊ��������ֻ���ж���xulie==arr1�ǲ���#����� 
			    i++;
		cin >> xulie;									//��Ҫ������һ��cin���͵�һ�ε�cin������ͬ�������ж�+��arr1��ֵ�� 
	}	
	cout << "����ַ�������>=�ĸ���Ϊ" << i << "��" << endl;
	return 0;
	
														//�޸�֮����Ҫ����һ��.exe�ļ��ص�����Ȼ���еĻ�����һ�ε��ļ� 
}


/*
����һ��˼·��
int main()
{
	char ch; int count=0        ���õ�ϰ�ߣ���Ҫ��ÿһ������ı������и�ֵ
	for(cin >> ch;ch != '#'; cin >> ch)      �����е�ѭ����������ֵ��ֵ��ÿ��ѭ����׼������for����������� 
		{
		if(ch =='>')						
		{cin >> ch;
		if(ch =='=')
			count ++;
		else if(ch =='#')break;}
		
		} 
	cout << "����������ĿΪ"  << count ;
	return 0;
}
*/
