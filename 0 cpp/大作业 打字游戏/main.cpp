#include <iostream>
#include <fstream>
#include <cstring>
#include <iomanip>
#include <ctime>
using namespace std;
/*
��ϰС������Ҫ��ɵĻ�������Ҫ��

1���������к���ʾ�˵����û���¼��1�����û�ע�᡾2����
 
2���û���¼����ʾ�˵���3�� 

ѡ����ϰ�Ѷȡ�4����ѡ���Ѷȵȼ�����ʾ��Ӧ���н��桾4������ϰ�����󣬱�����ϰ��¼��5��
�û������ٴ���ϰ�������˳����򡣡�5�� 

�鿴��ϰ��¼��������Ƽ�¼���ݺ���ʽ��

3���û�ע����棺�������

�������ܣ����ɹ���������ͨ�����Գ�����ս�����磺�Ƿ���ƹ���Ա��ɫ����ʾ�û���ϰ�Ĵ������ڡ���ʱ��ϰ......

��ʾ����1���ļ����ݵĶ�д���ս̲�332ҳ��9.3.3�ڣ���ҵ�����ļ����ļ���д��sample

      ��2����ʵ��ģ�黯���
*/


/*
������ĸ�ʽ�� 
	��ifstream infile("1.txt",ios::in);
	if(!infile.is_open()) 
	{
		cout << "�ļ�������";
		exit(-1);
	}
	char name[20], psw[10];//һ��Ҫ�ȶ���������˿ռ䣬���������Ŷ**** 
   infile>>name>>psw;//�����ʱ��Ҳ���ǿ��Զ���һ���ṹ���ͱ�����***�����ɻ����ߵ�**��
   for(int i=0;i<20;i++)
   infile >> user.name[i] >> user.password[i];
   infile.close();   
	�ڴ󲿷��������Ҫѭ�������**
	while(!infile.eof())ѭ�����򿪲��ɹ���ʱ��Ŷ 
	{
		infile>>list[num].name >> list[num].password;
		num++;
	} 
	 


������ĸ�ʽ�� 
	ofstream outfile("1.txt",ios::app)
	if(!outfile.is_open())
		{
			cout << "�ļ��򿪲��ɹ�";
			exit(-1);
		}
		char ch[1000];
	outfile << ch << endl;
	outfile.close();
*/
extern void deng(char name[]);
extern void fresh();
extern void log(char name[]);
extern void easy(char name[]); 
extern void average(char name[]);
extern void hard(char name[]);
extern void record(char name[]);
int main() 
{
	char name [10];//Ҫ��ס�ɹ���¼�û������ֵ�** 
	deng(name);
	L1:
	A:
	cout <<"��ӭ������������Ϸ����ѡ����Ҫ������ϰ���Ѷȣ�easy��average��hard��"<<endl;
	cout<< "�������鿴֮ǰ����Ϸ��¼�������� record"<< endl;
	char choice[10];
	cin >>choice;
	if(strcmp("easy",choice)==0)
			easy(name);
	else if (strcmp("average",choice)==0)
		average(name);
	else if (strcmp("hard",choice)==0)	
		hard(name);
	else if(strcmp("record",choice)==0)
		{
			record(name);
			goto A;
		}
	
	cout << "������������Ϸ��������yes����������˳���Ϸ��������������"<<endl;
	char ch[10];
	cin >> ch;
	if(strcmp("yes",ch)==0)
		goto L1;
	return 0;
}

//step1:��ɲ˵�����ơ��û���¼���û�ע��
/*
�˵����������������û����Լ����루���û���һ�����룩+���δע��-��ע�᡾Ҳ���Է�ģ�����С� 
*/ 
void deng(char name[])//�û���¼ 
{
	char ch1[10];
	cout <<"����������û��������롰yes����������Ѿ�ע�ᣬ�����롰no��"<<endl;
	cin >> ch1;
	if(strcmp("yes",ch1)==0)//�����û�
	{
		fresh();//�����ע�� 
		log(name);//��¼ 
	}
	else
		log(name);//��¼ 
}

void fresh()//�����û�ע�᡿ 
{ 
	cout << endl; 
	cout << "~~~~~~~~~~[���û�ע��]~~~~~~~~~~"<< endl;
	char ch3[10];
	L2:
	cout << "�����������û��������루���벻����8λ������8λ�Զ�����ǰ8λ��"<<endl;
	ifstream infile("users.txt",ios::in);
	if(!infile.is_open()) 
	{
		cout << "�ļ�������";
		exit(-1);
	} 
	
	cin >> ch3;//������2�� �ַ������룬������[]!!!!! 
	//���û��������롿	
	char ch2[10];
	infile >> ch2;//������1�� 
	/*
	���infile.ios::eof�ĺ�������һ����һ����û�ж����ġ�
	������Ҫ������ȶ�infile��һ�и�ֵ��� 
	��Ȼ�����������ѭ���ģ���һ�������ֵ�������ǿ���*** 
	*/
	while(infile.ios::eof()==0)
	{
		if(strcmp(ch3,ch2)==0)
			{	
				cout << "���û����ѱ�ע�ᣬ�������������û���";
				goto L2;
			}
		infile >> ch2;
	}
//����ch3�д�ľ����û����û�����**�������ͬһ���뵽�ļ�֮��*** 
	//����������롿 
	char ch1[10];//infile�Ǵ��ļ������뵽����֮�е�*** 
	L1:
	cin>>setw(9)>>ch1; 
	int i=0;
	while(ch1[i]!='\0')
	{
		if((ch1[i]<='z'&&ch1[i]>='a')||(ch1[i]<='9'&&ch1[i]>='0')||(ch1[i]<='Z'&&ch1[i]>='A'))
   			;
   		else
   		{
   			cout <<"���벻�Ϸ���������������������";
   			goto L1;
		}
		i++;
	}
	infile.close();
	ofstream outfile("users.txt",ios::app);	
	outfile << endl;
	outfile << ch3<< ' ' << ch1;

	outfile.close();
}

void log(char name[])//���û���¼�� 
{
	cout << "~~~~~~~~~~[��¼]~~~~~~~~~~" << endl;
	L3:
	cout << "�����������û����Լ�����"<<endl;
	char ch1[10],ch2[10];
	cin>>ch1>>ch2;
	char have1[10],have2[10];
	ifstream infile("users.txt",ios::in);
	infile >> have1>>have2;	
	while(infile.ios::eof()==0)//��eof�տ�ʼ���ص�ֵ��0��ֱ���ļ�β�ŷ����桿 
	{
		if(strcmp(ch1,have1)==0&&strcmp(ch2,have2)==0)
			{
				cout << "��¼�ɹ�"<<endl;//Ҫ��ס����û����ֵ�**֮��Ҫ�����¼��
				strcpy(name,ch1);
				break;
			} 
		infile >> have1 >> have2;
		if(strcmp(ch1,have1)==0&&strcmp(ch2,have2)==0)
			{
				cout << "��¼�ɹ�"<<endl;//Ҫ��ס����û����ֵ�**֮��Ҫ�����¼��
				strcpy(name,ch1);
				goto L0;//Q��breakֻ�ܴ���if��������ţ�����gotoΪʲô��������if�� 
			}
	}	
	if(infile.ios::eof()!=0)
	//�����ǣ��������е����������룬��û���ҵ�ƥ��ģ��Ż�����if 
	//������������һ���ҵ��� 
		{
			cout <<"�û���������������������������";
			goto L3;
		}
	L0:
	;
}
/*
eof�ĺ����ǣ�����ļ�û���κ��ַ����Ա��������ˡ����ֻ�����һ�е�ǰһ����ַ���eof���Ǳ�������0
			������һ�е������ַ���������ˣ���ôeof������1��
������β�����ʱ�򣬰����һ�е����ж���������ˣ���ôeof������1���������һ��ѭ����

infileû�б�Ҫ�����룬eofֻҪ���ļ����ж���û�б��������һ��ָ�룩��ʱ�򶼻����0�ģ� 
*/	
void easy(char name[])
{
	cout << "��ѡ���Ϊeasyģʽ������Ϊ ��Ӣ����ĸ��" << endl;
	cout <<"���ڿ�ʼ��ʱ"<<endl;
	ifstream infile("easy.txt",ios::in);
	char a[20];
	infile >> a;
	while(infile.ios::eof()==0)
	{
		cout << a << " ";
		infile >>a;
	}
	infile.close();//�������رա������Ѿ����ĵ������һ������֮��ֱ�Ӳ���ѭ����** 
	cout << endl;
	char user[20];
	double accuracy;
	double count=0;
	time_t before = time(0);  //��ȡ��ǰʱ��
	ifstream infile1("easy.txt",ios::in);//��һ��Ҫ��һ���������ء� 
	cout << endl;
	infile1 >> a ;//�����ǵ�������һ������ 
	while(infile1.ios::eof()==0)
	{	
		cin >> user;
		if(strcmp(a,user)==0)
			count++;		
		infile1 >> a;	
	}
	infile1.close();
	accuracy=count/20;
	time_t now = time(0);     //�ٴλ�ȡʱ��
	cout<<"���ܹ���ʱ"<<now-before<<"s"<<endl;    //�������ʱ���������
	cout << "������ȷ��Ϊ"<< (accuracy)*100 << '%' <<endl;
	cout << "����ѵ����¼�ѱ���"<<endl;
	//ѵ����¼��ѵ��ʱ�䡢��ȷ�ʡ�����ʱ 
	char dt[26];  
    strcpy(dt, ctime(&now));   //vs  ctime_s(dt,26,&now) ��ȡʱ���ַ���
	ofstream outfile("usersrecords.txt",ios::app);
	if(!outfile.is_open())
	{
		cout << "�ļ��򿪲��ɹ�";
		exit(-1);
	}
	outfile << name << " "<< "mode:easy"<<" "<< "accuracy:"<<accuracy*100 << '%' << " " <<"span:" <<now-before <<" "<< dt;
	outfile << endl;
	outfile.close();
}
	
void average(char name[])
{
	cout << "��ѡ���Ϊaverageģʽ������Ϊ ��Ӣ�����ԡ�" << endl;
	cout << "��ȷ�ʱ�׼Ϊ��һ������ȫ��������ȷ�ż���Ϊ��ȷ�������Ŷ��"<<endl;
	cout <<"���ڿ�ʼ��ʱ"<<endl;
	ifstream infile("average.txt",ios::in);
	char a[15];
	infile >> a;
	while(infile.ios::eof()==0)
	{
		cout << a << " ";
		infile >>a;
	}
	infile.close();//�������رա������Ѿ����ĵ������һ������֮��ֱ�Ӳ���ѭ����** 
	cout << endl;
	char user[15];
	double accuracy;
	double count=0;
	time_t before = time(0);  //��ȡ��ǰʱ��
	ifstream infile1("average.txt",ios::in);//��һ��Ҫ��һ���������ء� 
	cout << endl;
	infile1 >> a ;//�����ǵ�������һ������ 
	while(infile1.ios::eof()==0)
	{	
		cin >> user;
		if(strcmp(a,user)==0)
			count++;		
		infile1 >> a;	
	}
	infile1.close();
	accuracy=count/17;
	time_t now = time(0);     //�ٴλ�ȡʱ��
	cout<<"���ܹ���ʱ"<<now-before<<"s"<<endl;    //�������ʱ���������
	cout << "������ȷ��Ϊ"<< (accuracy)*100 << '%' <<endl;
	cout << "����ѵ����¼�ѱ���"<<endl;
	//ѵ����¼��ѵ��ʱ�䡢��ȷ�ʡ�����ʱ 
	char dt[26];  
    strcpy(dt, ctime(&now));   //vs  ctime_s(dt,26,&now) ��ȡʱ���ַ���
	ofstream outfile("usersrecords.txt",ios::app);
	if(!outfile.is_open())
	{
		cout << "�ļ��򿪲��ɹ�";
		exit(-1);
	}
	outfile << name << " "<<"mode:average" << "accuracy:"<<accuracy*100 << '%' << " " <<"span:" <<now-before <<" "<< dt;
	outfile << endl;
	outfile.close();
}
	
	
/*
I will greet this day with love in my heart.
Do what you say,say what you do.
I can make it through the rain. I can stand up once again on my own.
*/ 
	

void hard(char name[])
{
	cout << "��ѡ���Ϊhardģʽ������Ϊ ��Ӣ��ʫ�衿" << endl;
	cout << "��ȷ�ʱ�׼Ϊ��һ������ȫ��������ȷ�ż���Ϊ��ȷ�������Ŷ��"<<endl;
	cout <<"���ڿ�ʼ��ʱ"<<endl;
	ifstream infile("hard.txt",ios::in);
	char a[15];
	infile >> a;
	while(infile.ios::eof()==0)
	{
		cout << a << " ";
		infile >>a;
	}
	infile.close();//�������رա������Ѿ����ĵ������һ������֮��ֱ�Ӳ���ѭ����** 
	cout << endl;
	char user[15];
	double accuracy;
	double count=0;
	time_t before = time(0);  //��ȡ��ǰʱ��
	ifstream infile1("hard.txt",ios::in);//��һ��Ҫ��һ���������ء� 
	cout << endl;
	infile1 >> a ;//�����ǵ�������һ������ 
	while(infile1.ios::eof()==0)
	{	
		cin >> user;
		if(strcmp(a,user)==0)
			count++;		
		infile1 >> a;	
	}
	infile1.close();
	accuracy=count/146;
	time_t now = time(0);     //�ٴλ�ȡʱ��
	cout<<"���ܹ���ʱ"<<now-before<<"s"<<endl;    //�������ʱ���������
	cout << "������ȷ��Ϊ"<< (accuracy)*100 << '%' <<endl;
	cout << "����ѵ����¼�ѱ���"<<endl;
	//ѵ����¼��ѵ��ʱ�䡢��ȷ�ʡ�����ʱ 
	char dt[26];  
    strcpy(dt, ctime(&now));   //vs  ctime_s(dt,26,&now) ��ȡʱ���ַ���
	ofstream outfile("usersrecords.txt",ios::app);
	if(!outfile.is_open())
	{
		cout << "�ļ��򿪲��ɹ�";
		exit(-1);
	}
	outfile << name << " "<<"mode:hard" << " " << "accuracy:"<<accuracy*100 << '%' << " " <<"span:" <<now-before <<" "<< dt;
	outfile << endl;
	outfile.close();
}

void record(char name[])
{
	ifstream infile("usersrecords.txt",ios::in);
	char ch1[20],ch2[20],ch3[20],ch4[20],ch5[20],ch6[20],ch7[20],ch8[20],ch9[20];
	while(infile.ios::eof()==0)
	{
		infile >> ch1>>ch2>>ch3>>ch4>>ch5>>ch6>>ch7>>ch8>>ch9;
		if(strcmp(ch1,name)==0)
		{
			cout << ch1<<" "<<ch2<<" "<<ch3<<" "<<ch4<<" "<<ch5<<" "<<ch6<<" "<<ch7<<" "<<ch8<< " "<<ch9;
			cout <<endl;
		}
	}
}
//Q:�ظ�������� 



	

