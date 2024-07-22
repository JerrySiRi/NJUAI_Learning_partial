'''
HTML是一种标记语言，浏览器可以通过解析HTML的关键字来控制网页展示的格式。
现在我们需要写一个简单的HTML浏览器，将HTML内容转换成对应格式的输出，只需要处理简单的<br>, <hr>两种关键字。
同时，将【所有的空格、制表符（tab）都当作空格】；【每行显示的字符个数不多于80个。】

输入：
输入包含词和HTML关键字，它们之间使用一个或多个空格或制表符分隔开。(如123, <hr> 456 <br> 6788,)
一个词由字母、数字或标点组成。例如， "abc,123"是一个词（没有空格或制表符），但"abc, 123"是两个词（有空格啦）， 分别是"abc,"和"123"。
每个词不超过80个字符，且不包含"<"和">"，HTML关键字仅包含"<br>"和"<hr>"。

输出规则：
（1）如果当前读取到一个词，若当前行加上该词汇不超过80个字符，则输出该词，否则，另起一行再输出该词；
（2）如果当前读取到<br>， 另起一行；
（3）如果当前读取到<hr>：
    1.当<hr>在行首，输出80个‘-’并另起一行，
    2.当<hr>不在行首，另起一行，输出80个‘-’，并另起一行。
（4）词与词之间用一个空格符分隔开。
（5）输出以换行符结尾。

123 789 <br>   <hr>    45678  789  <hr>  345
445566 <br>      hhh <hr>    999
'''
x=input().split(' ')
consta=x.count('')
for i in range(0,consta):#去掉多个空格（含水平制表符）
    x.remove('')
count=0
for i in x:
    if i!='<hr>' and i !='<br>':#不是HTML关键字，水平输出，隔一个空格‘ ’
        if count+len(i)<=80:#该行加上这个词不超过80个字符，水平输出
            count+=len(i)
            print(i,end=' ')
        else:
            count=len(i)
            print('\n',end='')
            print(i,end='')
    elif i =='<br>':#是<br>
        count=0
        print('\n',end='')
    elif i=='<hr>':
        if count==0:#<hr>在行首
            for j in range(0,80):
                print('-',end='')
            print('\n',end='')
        else:
            print('\n',end='')
            for j in range(0,80):
                print('-',end='')
            print('\n',end='')
            count=0
print('\n')




