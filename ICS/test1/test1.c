#include <stdarg.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
int vsn(char *out, size_t n, const char *fmt, va_list ap) {
	size_t sum=0;//返回写入的字符总数
	//switch中的变量定义
	char hex_num[20]="0123456789ABCDEF";
	
	
	while(*fmt!='\0' && n>1 ){
		if(*fmt=='%'){//此时fmt后面跟着的要输入的格式
			fmt++;
			char ch_temp=*fmt;
				//[%d]
			if(ch_temp=='d'){
				int current = va_arg(ap,int);
    				if (current == 0){
     					*out = '0';
     					out++;//已经更新了out的位置啦
     					sum++;
     					n--;
    				}
    				else{//正数和负数（通过一个开关来看看啦！--导论的minmax的想法！）
    					int index=0;
    					char temp[1024];
    					if(current<0){
    						*out='-';
    						sum++;
    						out++;
    						n--;
    					}
    					current = (current>0)?(current):(-current);
     					while (current!=0){
      						temp[index] = current % 10 + '0';
      						current = current/ 10;
      						index++;
     					}
     					sum+=index;
     					index--;
     					while (index>=0 && n>1){
      						*out = temp[index];
      						index--;out++;//已经更新了out的位置啦
      						n--;
     					}
    				}
				}
			//[%s]
			if(ch_temp=='s'){
   				char *str = va_arg(ap,char*);
   				while(*str!='\0' && n>1){
   					*out=*str;
   					str++;
   					out++;
   					sum++;
   					n--;
     				}
			}
			//[%c]	
			//可以把输入的数字按照ASCII码相应转换为对应的字符
			if(ch_temp=='c'){//【可能的bug，如果真的是一个字符，‘c’输出的也应该是一个字符】
				char temp_c=(char)va_arg(ap,int);
				*out=temp_c;
				out++;
				sum++;
			}
			//[%x]
			//以十六进制输出		
			if(ch_temp=='x'){
				int current=va_arg(ap,int);
				int index=0;
				char temp[1024];
				//同样通过temp这个中间数组变量先存高位-》低位
				while (current!=0){
      				temp[index] = hex_num[current % 16];
      				current = current / 16;
      				index++;
     			}
     			sum+=index;
     			index--;
     			while (index>=0 && n>1){
      				*out = temp[index];
      				index--;out++;//已经更新了out的位置啦
      				n--;
     			}
			}		
		}
		
		//不是%开头的，直接放入数组之中就可以啦！
		else {
			*out=*fmt;
   			out++;
   			sum++;
   			n--;
		}

  	
  	//每次while循环的变化,把n--放在switch之中拉，每在out中加入一个就把n--呢！
	fmt++;
	
	}
	//整个循环结束啦！
	*out = '\0';
     return sum;
}

int s_p(char *out, const char *fmt, ...) {
 	va_list vap;//后面的变长参数列表
 	va_start(vap,fmt);//先让fmt不是引号
 	int sum = vsn(out,-1,fmt,vap);
 	va_end(vap);
 	return sum;
}

int main()
{
    char target1[128];
    s_p(target1, "%s", "Hello world!\n");
    printf("%s",target1);
    s_p(target1, "%d + %d = %d\n", 1, 1, 2);
    printf("%s",target1);
    s_p(target1, "%d + %d = %d\n", 2, 10, 12);
    printf("%s",target1);


}