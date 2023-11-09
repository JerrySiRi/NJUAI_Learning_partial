#include <iostream>
#include <stack>
#include<string>
using namespace std;

inline int kuohao_ru(stack<int> *s1,stack<int> *s2,int i,string express)
//多个括号的情况，把所有的(,)都加入进来，遇到)的时候向左删除并加入s2，直到删除到遇到第一个（为止
{
    (*s1).push('(');
    i++;
    while(express[i]!=')')
    {
            if(express[i]<= '9' && express[i]>= '0')//括号中是数字
                (*s2).push(express[i]);
            else if((express[i]=='+'||express[i]=='*'))//&&flag==true
                {
                    R:
                        if((*s1).empty()==true || (*s1).top()=='(')
                        {
                            (*s1).push(express[i]);
                            i++;
                            continue;
                        }
                        if((*s1).top()=='+' && express[i]=='*')
                            (*s1).push(char(express[i]));
                        else
                            {
                                (*s2).push(char((*s1).top()));
                                (*s1).pop();
                                goto R;
                            }//bug,这里只进行了一步呀！！！
                }
            else
                //括号之中嵌套括号
                {
                    i=kuohao_ru(&(*s1),&(*s2),i,express);
                    i--;
                }
        i++;
    }
    
    while((*s1).top()!='(')//逐步让s1中括号内的元素进入s2之中
    {
        (*s2).push((*s1).top());
        (*s1).pop();
    }
    (*s1).pop();//去除左括号
    i++;//不让右括号进栈
    return i;//下一次操作的下标
}

int main()
{
    stack<int> s1;
    stack<int> s2;
    string express;
    cin>>express;
    int i=0;
    while(express[i]!='\0')
    {
        if(express[i]=='(')
            {i=kuohao_ru(&s1,&s2,i,express);continue;}
        if(express[i]<= '9' && express[i]>= '0')//输入时数字的情况
            s2.push(char(express[i]));
        else //输入是运算符的情况
            {
                if(express[i]=='(')
                    {i=kuohao_ru(&s1,&s2,i,express);continue;}
                if(s1.empty()== true )//s1中没有元素
                    s1.push(char(express[i]));
                else //输入的是括号或者+或*的时候
                    {
                        L:
                        if(s1.empty()==true)
                        {
                            s1.push(express[i]);
                            i++;
                            continue;
                        }
                        if(s1.top()=='+' && express[i]=='*')
                        {
                            s1.push(char(express[i]));
                        }
                            
                        else
                            {
                                s2.push(char(s1.top()));
                                s1.pop();
                                goto L;
                            }//bug,这里只进行了一步呀！！！

                    }
            }
        i++;
    }

    while(s2.empty()!=true)
    {s1.push(char(s2.top()));s2.pop();}
    while(s1.empty()!=true)
    { cout << char(s1.top());s1.pop();}
    return 0;
}