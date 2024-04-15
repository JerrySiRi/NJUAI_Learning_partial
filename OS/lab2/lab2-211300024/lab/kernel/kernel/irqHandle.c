#include "x86.h"
#include "device.h"

extern int displayRow;
extern int displayCol;

extern uint32_t keyBuffer[MAX_KEYBUFFER_SIZE];
extern int bufferHead;
extern int bufferTail;


void GProtectFaultHandle(struct TrapFrame *tf);

void KeyboardHandle(struct TrapFrame *tf);

void syscallHandle(struct TrapFrame *tf);
void syscallWrite(struct TrapFrame *tf);
void syscallPrint(struct TrapFrame *tf);
void syscallRead(struct TrapFrame *tf);
void syscallGetChar(struct TrapFrame *tf);
void syscallGetStr(struct TrapFrame *tf);

int tail;//指示当前用户输入的位置

void irqHandle(struct TrapFrame *tf) { // pointer tf = esp
	/*
	 * 中断处理程序
	 */
	/* Reassign segment register */
	asm volatile("movw %%ax, %%ds"::"a"(KSEL(SEG_KDATA)));
	//asm volatile("movw %%ax, %%es"::"a"(KSEL(SEG_KDATA)));
	//asm volatile("movw %%ax, %%fs"::"a"(KSEL(SEG_KDATA)));
	//asm volatile("movw %%ax, %%gs"::"a"(KSEL(SEG_KDATA)));
	switch(tf->irq) {//【【【step1:对中断向量号进行查询后，确定了中断处理程序 step2:再在中断处理程序中，对调用号进行分发】】】
		// TODO: 填好中断处理程序的调用，目前只有两种系统调用可用【KeyboardHandle和syscallHandle，完成他们后调用即可】
		case 0xd://此时本.c文件中新增了80386的通用保护异常的中断处理程序
			GProtectFaultHandle(tf);
			break;
		case 0x21:
			KeyboardHandle(tf);
			break;
		case 0x80:
			syscallHandle(tf);
			break;
		case -1://【梳理：一直是在运行汇编程序doIrq.S的，在得到是出错码的时候什麼都不作（汇编中定义的出错玛的中断向量号是-1）】
			break;
		default:assert(0);
	}
}

void GProtectFaultHandle(struct TrapFrame *tf){
	assert(0);
	return;
}

//功能：对用户不同的输入作出相应.利用【键盘驱动接口】and【串口输出接口】完成键盘按键的串口回显，之后就可以在stdio中显示自己按的键！
void KeyboardHandle(struct TrapFrame *tf){
	uint32_t code = getKeyCode();
	int pos=0;
	uint16_t data=0;
	if(code == 0xe){ // 退格符
		//  要求只能退格用户键盘输入的字符串，且最多退到当行行首
		if(displayCol>0&&displayCol>tail){
			displayCol-=1;
			data = 0 | (0x0c << 8);
			pos = (80*displayRow+displayCol)*2;
			asm volatile("movw %0, (%1)"::"r"(data),"r"(pos+0xb8000));
			
		}
	}else if(code == 0x1c){ // 回车符
		// 处理回车情况
		keyBuffer[bufferTail++]='\n';//在qemu中进行换行
		displayRow+=1;
		displayCol=0;
		tail=0;
		if(displayRow==25){
			displayRow=24;
			displayCol=0;
			scrollScreen();
		}
		putChar('\n');//在串口进行换行
	}else if(code < 0x81){ // 正常字符
		// 注意输入的大小写的实现、不可打印字符的处理
		char character=getChar(code);
		if(character!=0){
			putChar(character);//向串口中进行输出字符
			keyBuffer[bufferTail++]=character;//向keyuffer中存字符，未来向qemu中输入
			bufferTail%=MAX_KEYBUFFER_SIZE;
			data=character|(0x0c<<8);
			pos=(80*displayRow+displayCol)*2;
			asm volatile("movw %0, (%1)"::"r"(data),"r"(pos+0xb8000));
			displayCol+=1;
			if(displayCol==80){
				displayCol=0;
				displayRow++;
				if(displayRow==25){
					displayRow=24;
					displayCol=0;
					scrollScreen();
				}
			}
		}
	}
	updateCursor(displayRow, displayCol);
	
}
void syscallHandle(struct TrapFrame *tf) {
	switch(tf->eax) { // syscall number
		case 0:
			syscallWrite(tf);
			break; // for SYS_WRITE
		case 1:
			syscallRead(tf);
			break; // for SYS_READ
		default:break;
	}
}

void syscallWrite(struct TrapFrame *tf) {
	switch(tf->ecx) { // file descriptor
		case 0:
			syscallPrint(tf);
			break; // for STD_OUT
		default:break;
	}
}

//把结果显示到用户屏幕上，写显存
void syscallPrint(struct TrapFrame *tf) {
	int sel = USEL(SEG_UDATA); //TODO:和idt初始化selector一样的，可以利用定义的宏啦。 segment selector for user data, need further modification
	char *str = (char*)tf->edx;
	int size = tf->ebx;
	int i = 0;
	int pos = 0;
	char character = 0;
	uint16_t data = 0;
	asm volatile("movw %0, %%es"::"m"(sel));
	for (i = 0; i < size; i++) {
		asm volatile("movb %%es:(%1), %0":"=r"(character):"r"(str+i));//功能：把printf的字符串的str的第i个字符赋值给character

//data = character | (0x0c << 8);
//pos = ( 80 * displayRow+displayCol)*2;
//asm volatile("movw %0, (%1)"::"r"(data),"r"(pos+0xb8000));
//要注意---碰到\n,换行，滚屏的处理，qemu模拟的屏幕的大小是80*25
//以上三行代码会用到的，用户调用printf之后就能在屏幕上进行输出啦

		// TODO: 完成光标的维护和打印到显存
		if(character == '\n'){
			displayRow += 1;
			displayCol = 0;
			if(displayRow == 25){//当前屏幕满啦。就要进行滚屏幕，依据函数，每次只往下更新一行
				displayRow =24;
				displayCol =0;	
				scrollScreen();//没有进行屏幕的显示,但没必要显示，下一行是空的
			}
		}
		else{//不是换行，是character的正常字符
			data = character | (0x0c << 8);
			pos = ( 80 * displayRow+displayCol)*2;
			asm volatile("movw %0, (%1)"::"r"(data),"r"(pos+0xb8000));
			displayCol += 1;
			if(displayCol == 80){
				displayRow += 1;
				displayCol = 0;
			}
			if(displayRow == 25){
				displayRow=24;
				displayCol=0;
				scrollScreen();
			}
		}
	}
	tail=displayCol;
	updateCursor(displayRow, displayCol);
}

void syscallRead(struct TrapFrame *tf){
	switch(tf->ecx){ //file descriptor
		case 0:
			syscallGetChar(tf);
			break; // for STD_IN
		case 1:
			syscallGetStr(tf);
			break; // for STD_STR
		default:break;
	}
}


void syscallGetChar(struct TrapFrame *tf){
	bufferHead=0;
	bufferTail=0;
	keyBuffer[bufferHead]=0;
	keyBuffer[bufferHead+1]=0;
	char c=0;
	
	while(c == 0){//一直等待用户输入，只有用户输入了c才不是0！
		enableInterrupt();
		c = keyBuffer[bufferHead];
		disableInterrupt();
	}

	tf->eax=c;//保存到tf【也就是函数的返回值-eax中！】

	char wait_enter=0;
	while(wait_enter==0){//如果下一次拿到的keyBuffer中的内容是0，那么就不输出（用户输入完成但没有按enter呢！）
			     //如果下一次拿到了enter，那么就关闭中断，直接让printf输出（中断的嵌套）
		enableInterrupt();
		wait_enter = keyBuffer[bufferHead+1];
		disableInterrupt();
	}
	return;

}

void syscallGetStr(struct TrapFrame *tf){
	// TODO: 自由实现
	char* str=(char*)(tf->edx);//用一个新指针str保存读入的信息，而且和trapframe中的位置保持一致》》trapframe也可以得到同步的信息
	int size=(int)(tf->ebx);//trapframe最多可以容纳的字符串数组的大小
	bufferHead=0;
	bufferTail=0;
	for(int j=0;j<MAX_KEYBUFFER_SIZE;j++)
		keyBuffer[j]=0;//init
	
	int i=0;
	char tpc=0;
	while(tpc!='\n' && i<size){//同getChar-一直等待enter或者读到大小的上限【中断一直是开-关-开-关-开-关......】
		while(keyBuffer[i]==0)
			enableInterrupt();
		tpc=keyBuffer[i];
		i++;
		disableInterrupt();
	}
	//此时已经拿到了输入完成的keyuffer（大小不超上限）
	int selector=USEL(SEG_UDATA);
	asm volatile("movw %0, %%es"::"m"(selector));
	int k=0;
	for(int p=bufferHead; p<i-1; p++){
		asm volatile("movb %0, %%es:(%1)"::"r"(keyBuffer[p]),"r"(str+k));
		k++;
	}
	asm volatile("movb $0x00, %%es:(%0)"::"r"(str+i));
	return;
}

