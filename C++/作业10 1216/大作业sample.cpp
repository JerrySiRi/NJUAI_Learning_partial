#include<iostream>
#include <fstream>//�ļ��������ļ���Ϊһ���������ļ������ݣ� 
using namespace std;
int main()
{   ifstream infile("user.txt",ios::in);   
	//Դ�ļ���user.txt��ͬһ���ļ����С�inf�������ļ���infile����ifstream��һ���ࡣ
	//�����ǹ��캯������ʼ�����infile
	//��������cpp����һ���ļ��У���Ҫָ������·���ġ�D:\\���ļ��һ���꣬�ѵ�ַ���Ƴ��ı�**
	//��Ҫ�Ѹ���������һ��\�ټ�һ��\����һ��ת�����е� 
     char name[20], psw[10];
     
    if(!infile) //�����ļ���ʱ�򣬷�ֹ�ļ����ڡ����ж�����ļ��ǲ�����Ĵ��� 
   {  cout<<"�ļ�������";
      return 0;
   }
   infile>>name>>psw;    // ����user.txt�ļ����һ���û���������
   //�ļ��л��ж���û���***����ѭ�������
   /*��һ���ȿ��ж��ٸ��û���������100����
   user list[100]
   int num=0;
   while(!infile.eof())��ʧ��
   ������ 
    
    ������
	�򿪵��ļ�֮�е�һ�е��������û��ĸ���
	��֮��
	
	
	������
	�ǲ����û������ظ�
	�ǲ���������Ч
	
	ʱ���¼
	��ͣ������ʱ���¼���� 
   */ 
   //infile�����ú�cin������һ���������ǰ����Ӧ��֪���ļ��д�ŵ���ʲô**
   //���ļ�����nju 21130000000  nju 211409999 ��name+password�� 
   cout<<name<<"  "<<psw<<endl;
   infile.close();
   char newname[20],newpsw[10];
   cin>>newname>>newpsw;
   ofstream outfile("user.txt",ios::app);   //���ļ�β������   appendix�����ļ�β���������û� 
   //outfile�����ļ���д�� Ҳ��һ�����캯�����¶��� 
   outfile<<endl<<newname<<" " <<newpsw;  //��user.txt�ļ��е����һ��д��
   outfile.close();//������߶�������֮����Ҫ�رա���ȣ�ָ�롣�����ļ���֮��Ҳ��Ҫ�رյ�
    
    //д��ϰ��¼ 
    //����м�¼�Ļ������ȹر������´򿪡����û�м�¼����ֱ�Ӵ� 
   ofstream recodefile("recode.txt",ios::out);   //��recode�ļ�д����Ϣ
   
   int time = 10;
   double accuracy = 0.98;
   recodefile<<"Training time :"<<time<<" ; "<<"accuracy : "<<accuracy<<endl;
   recodefile.close();
   return 0;
}
