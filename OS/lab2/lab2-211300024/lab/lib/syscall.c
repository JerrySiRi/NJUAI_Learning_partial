#include "lib.h"
#include "types.h"
/*
 * io lib here
 * 库函数写在这
 */
//static inline int32_t syscall(int num, uint32_t a1,uint32_t a2,
int32_t syscall(int num, uint32_t a1,uint32_t a2,
		uint32_t a3, uint32_t a4, uint32_t a5)
{
	int32_t ret = 0;
	//Generic system call: pass system call number in AX
	//up to five parameters in DX,CX,BX,DI,SI
	//Interrupt kernel with T_SYSCALL
	//
	//The "volatile" tells the assembler not to optimize
	//this instruction away just because we don't use the
	//return value
	//
	//The last clause tells the assembler that this can potentially
	//change the condition and arbitrary memory locations.

	/*
	XXX Note: ebp shouldn't be flushed
	    May not be necessary to store the value of eax, ebx, ecx, edx, esi, edi
	*/
	uint32_t eax, ecx, edx, ebx, esi, edi;
	uint16_t selector;
	
	asm volatile("movl %%eax, %0":"=m"(eax));
	asm volatile("movl %%ecx, %0":"=m"(ecx));
	asm volatile("movl %%edx, %0":"=m"(edx));
	asm volatile("movl %%ebx, %0":"=m"(ebx));
	asm volatile("movl %%esi, %0":"=m"(esi));
	asm volatile("movl %%edi, %0":"=m"(edi));

	asm volatile("movl %0, %%eax"::"m"(num));
	asm volatile("movl %0, %%ecx"::"m"(a1));
	asm volatile("movl %0, %%edx"::"m"(a2));
	asm volatile("movl %0, %%ebx"::"m"(a3));
	asm volatile("movl %0, %%esi"::"m"(a4));
	asm volatile("movl %0, %%edi"::"m"(a5));
	asm volatile("int $0x80");

	asm volatile("movl %%eax, %0":"=m"(ret));
	asm volatile("movl %0, %%eax"::"m"(eax));
	asm volatile("movl %0, %%ecx"::"m"(ecx));
	asm volatile("movl %0, %%edx"::"m"(edx));
	asm volatile("movl %0, %%ebx"::"m"(ebx));
	asm volatile("movl %0, %%esi"::"m"(esi));
	asm volatile("movl %0, %%edi"::"m"(edi));
	
	asm volatile("movw %%ss, %0":"=m"(selector)); //XXX %ds is reset after iret
	//selector = 16;
	asm volatile("movw %%ax, %%ds"::"a"(selector));
	
	return ret;
}

char getChar(){ // 对应SYS_READ STD_IN
	// TODO: 实现getChar函数，方式不限
	//可以等按键输入完成的时候，将末尾字符通过eax寄存器传递回来【注意：eax在用户态向内核态传递参数的过程中，既扮演了参数的角色，又扮演了返回值的角色！】
	//【使用通用寄存器作为中间桥梁就可以】
	return syscall(SYS_READ,STD_IN,0,0,0,0);
}

void getStr(char *str, int size){ // 对应SYS_READ STD_STR
	// TODO: 实现getStr函数，方式不限【涉及字符串的传递】
	//【用通用寄存器作为中间桥梁不可以，因为字符串地址作为参数仍然涉及到了不同的数据段】
	//【再看看lab2-ppt这个文件最后两页吧】
	syscall(SYS_READ,STD_STR,(uint32_t)str,(uint32_t)size,0,0);
	return;
}

int dec2Str(int decimal, char *buffer, int size, int count);
int hex2Str(uint32_t hexadecimal, char *buffer, int size, int count);
int str2Str(char *string, char *buffer, int size, int count);


//printf在用户态对参数进行处理，并进行系统调用传入参数和调用号（下面调用了syscall函数）
void printf(const char *format,...){
	int i=0; // format index
	char buffer[MAX_BUFFER_SIZE];
	int count=0; // buffer index
	//int index=0; // parameter index-----好像也用不到诶
	void *paraList=(void*)&format; // address of format in stack【是format指针本身自己的地址，在栈中！】
//【【Review：调用函数的时候所有的参数都压入栈中了！所以printf可以不光使用PA中的va_list数据类型，更可以使用栈中参数的位置来进行访问参数！】】
	//int state=0; // 0: legal character; 1: '%'; 2: illegal format-------没必要用
	//以下是传入的四种类型的参数来让printf解析，且下面的都是参数的值或开始位置
	int decimal=0;
	uint32_t hexadecimal=0;
	char *string=0;
	char character=0;
	while(format[i]!=0){
		// TODO:在count达到MAX_BUFFER_SIZE的时候就要进行一次显示，而不一定是最终解析完成才全部解释
		// TODO-在用户态【对参数进行处理】，并进行系统调用传入参数和调用号，并如下，系统调用向内核发送软中断请求。
		buffer[count] = format[i];
		count++;//默认都给count++啦
		if(format[i] == '%'){//【【【BUG！C语言中字符串和字符是不一样的！字符可以表示成数字！字符串只能是指针！】】】
			count--;//原来被放到buffer[count]位置的是%，不能被输出，得被覆盖
			i++;//判断%后面的是什么，如%d，%s
			//只有遇到了%，才会使用参数呢！
			paraList +=sizeof(format);//把下一个被输出的字符串、十进制、十六进制的位置准备好
			switch(format[i]){
				case 'd':
					decimal = *(int*)paraList;
					count = dec2Str(decimal, buffer, MAX_BUFFER_SIZE, count);
					break;
				case 'x':
					hexadecimal = *(uint32_t*)paraList;
					count = hex2Str(hexadecimal, buffer, MAX_BUFFER_SIZE, count);
					break;
				case 's':
					string = *(char**)paraList;//此时paralist被解读一个指向char*的指针【二重指针啦】
					count = str2Str(string, buffer, MAX_BUFFER_SIZE, count);
					break;
				case 'c':
					character = *(char*)paraList;
					buffer[count] = character;
					count ++;
					break;
			}
			
		}
		if(count == MAX_BUFFER_SIZE){
			syscall(SYS_WRITE,STD_OUT,(uint32_t)buffer,(uint32_t)MAX_BUFFER_SIZE,0,0);
			count=0;//count已经到达最大啦，输出后清0
		}

		i++;//当前遇到的format不是%的情况，比如乘法*，加法+等
	}//while的结束
		
	if(count!=0)
		syscall(SYS_WRITE, STD_OUT, (uint32_t)buffer, (uint32_t)count, 0, 0);
}




int dec2Str(int decimal, char *buffer, int size, int count) {
	int i=0;
	int temp;
	int number[16];

	if(decimal<0){
		buffer[count]='-';
		count++;
		if(count==size) {
			syscall(SYS_WRITE, STD_OUT, (uint32_t)buffer, (uint32_t)size, 0, 0);
			count=0;
		}
		temp=decimal/10;
		number[i]=temp*10-decimal;
		decimal=temp;
		i++;
		while(decimal!=0){
			temp=decimal/10;
			number[i]=temp*10-decimal;
			decimal=temp;
			i++;
		}
	}
	else{
		temp=decimal/10;
		number[i]=decimal-temp*10;
		decimal=temp;
		i++;
		while(decimal!=0){
			temp=decimal/10;
			number[i]=decimal-temp*10;
			decimal=temp;
			i++;
		}
	}

	while(i!=0){
		buffer[count]=number[i-1]+'0';
		count++;
		if(count==size) {
			syscall(SYS_WRITE, STD_OUT, (uint32_t)buffer, (uint32_t)size, 0, 0);
			count=0;
		}
		i--;
	}
	return count;
}

int hex2Str(uint32_t hexadecimal, char *buffer, int size, int count) {
	int i=0;
	uint32_t temp=0;
	int number[16];

	temp=hexadecimal>>4;
	number[i]=hexadecimal-(temp<<4);
	hexadecimal=temp;
	i++;
	while(hexadecimal!=0){
		temp=hexadecimal>>4;
		number[i]=hexadecimal-(temp<<4);
		hexadecimal=temp;
		i++;
	}

	while(i!=0){
		if(number[i-1]<10)
			buffer[count]=number[i-1]+'0';
		else
			buffer[count]=number[i-1]-10+'a';
		count++;
		if(count==size) {
			syscall(SYS_WRITE, STD_OUT, (uint32_t)buffer, (uint32_t)size, 0, 0);
			count=0;
		}
		i--;
	}
	return count;
}

int str2Str(char *string, char *buffer, int size, int count) {
	int i=0;
	while(string[i]!=0){
		buffer[count]=string[i];
		count++;
		if(count==size) {
			syscall(SYS_WRITE, STD_OUT, (uint32_t)buffer, (uint32_t)size, 0, 0);
			count=0;
		}
		i++;
	}
	return count;
}
