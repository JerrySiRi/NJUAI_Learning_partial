#include <iostream>
#include <stack>
#include<string>
using namespace std;


/*
【另外的方法】使用struct+迭代的方法，把递归转化成迭代
*/
struct Frame{
    stack<int> *s1;
    stack<int> *s2;
    int i;
    string express;
    Frame *prevFrame;//指向前一个函数栈的指针
};


int kuohao_ru(stack<int> *s1,stack<int> *s2,int i,string express)
{
    stack<Frame> han;
    struct Frame temp = {s1,s2,i,express,NULL};//还是得用指针，引用原来的那两个栈呢！
    (*temp.s1).push('(');
    han.push(temp);
    i++;
    int target=0;
    while(!han.empty())
    {
        struct Frame peek=han.top();
        if(peek.express[i]==')')//situation1:遇到了右括号了！，此时不需要创建新的frame，直接调用栈顶的即可
        {
            while((*peek.s1).top()!='(')//逐步让s1中括号内的元素进入s2之中
            {
                (*peek.s2).push((*peek.s1).top());
                (*peek.s1).pop();
            }
            (*peek.s1).pop();//去除左括号
            i++;//不让右括号进栈
            target=i;
            if ((peek.prevFrame)!=NULL)
                (peek.prevFrame)->i=i;//到上一个栈之中，修改他的i，并且把栈顶栈给去掉
            han.pop();
            continue;
        }
        else if(peek.express[i]!='('&&peek.express[i]!=')'){//situation2:下一个元素是既不是左括号也不是有括号，在当前frame直接操作就行！
            if(peek.express[i]<= '9' && peek.express[i]>= '0')//括号中是数字
                (*peek.s2).push(peek.express[i]);
            else if((peek.express[i]=='+'||peek.express[i]=='*'))
                {
                    R:
                        if((*peek.s1).empty()==true || (*peek.s1).top()=='(')
                        {
                            (*peek.s1).push(peek.express[i]);
                            i++;
                            continue;
                        }
                        if((*peek.s1).top()=='+' && peek.express[i]=='*')
                            (*peek.s1).push(char(peek.express[i]));
                        else
                            {
                                (*peek.s2).push(char((*peek.s1).top()));
                                (*peek.s1).pop();
                                goto R;
                            }//bug,这里只进行了一步呀！！！
                }
            }
        else//下一个元素是(，创建新栈
        {
            struct Frame newone = {s1,s2,i,express,&peek};
            (*newone.s1).push('(');
            han.push(newone);
        }
    i++;
    }
    return target;
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