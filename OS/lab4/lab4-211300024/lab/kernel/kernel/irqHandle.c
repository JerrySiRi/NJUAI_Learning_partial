#include "x86.h"
#include "device.h"

#define SYS_WRITE 0
#define SYS_READ 1
#define SYS_FORK 2
#define SYS_EXEC 3
#define SYS_SLEEP 4
#define SYS_EXIT 5
#define SYS_SEM 6

#define STD_OUT 0
#define STD_IN 1

#define SEM_INIT 0
#define SEM_WAIT 1
#define SEM_POST 2
#define SEM_DESTROY 3

extern TSS tss;

extern ProcessTable pcb[MAX_PCB_NUM];
extern int current;

extern Semaphore sem[MAX_SEM_NUM];
extern Device dev[MAX_DEV_NUM];

extern int displayRow;
extern int displayCol;

extern uint32_t keyBuffer[MAX_KEYBUFFER_SIZE];
extern int bufferHead;
extern int bufferTail;

void GProtectFaultHandle(struct StackFrame *sf);
void timerHandle(struct StackFrame *sf);
void keyboardHandle(struct StackFrame *sf);
void syscallHandle(struct StackFrame *sf);

void syscallWrite(struct StackFrame *sf);
void syscallRead(struct StackFrame *sf);
void syscallFork(struct StackFrame *sf);
void syscallExec(struct StackFrame *sf);
void syscallSleep(struct StackFrame *sf);
void syscallExit(struct StackFrame *sf);
void syscallSem(struct StackFrame *sf);

void syscallWriteStdOut(struct StackFrame *sf);

void syscallReadStdIn(struct StackFrame *sf);

void syscallSemInit(struct StackFrame *sf);
void syscallSemWait(struct StackFrame *sf);
void syscallSemPost(struct StackFrame *sf);
void syscallSemDestroy(struct StackFrame *sf);

void irqHandle(struct StackFrame *sf) { // pointer sf = esp
	/* Reassign segment register */
	asm volatile("movw %%ax, %%ds"::"a"(KSEL(SEG_KDATA)));
	/* Save esp to stackTop */
	uint32_t tmpStackTop = pcb[current].stackTop;
	pcb[current].prevStackTop = pcb[current].stackTop;
	pcb[current].stackTop = (uint32_t)sf;

	switch(sf->irq) {
		case -1:
			break;
		case 0xd:
			GProtectFaultHandle(sf);
			break;
		case 0x20:
			timerHandle(sf);
			break;
		case 0x21:
			keyboardHandle(sf);
			break;
		case 0x80:
			syscallHandle(sf);
			break;
		default:assert(0);
	}
	/* Recover stackTop */
	pcb[current].stackTop = tmpStackTop;
}

void GProtectFaultHandle(struct StackFrame *sf) {
	assert(0);
	return;
}

void timerHandle(struct StackFrame *sf) {
	int i;
	uint32_t tmpStackTop;
	i = (current+1) % MAX_PCB_NUM;
	while (i != current) {
		if (pcb[i].state == STATE_BLOCKED && pcb[i].sleepTime != -1) {
			pcb[i].sleepTime --;
			if (pcb[i].sleepTime == 0)
				pcb[i].state = STATE_RUNNABLE;
		}
		i = (i+1) % MAX_PCB_NUM;
	}

	if (pcb[current].state == STATE_RUNNING &&
		pcb[current].timeCount != MAX_TIME_COUNT) {
		pcb[current].timeCount++;
		return;
	}
	else {
		if (pcb[current].state == STATE_RUNNING) {
			pcb[current].state = STATE_RUNNABLE;
			pcb[current].timeCount = 0;
		}
		
		i = (current+1) % MAX_PCB_NUM;
		while (i != current) {
			if (i !=0 && pcb[i].state == STATE_RUNNABLE)
				break;
			i = (i+1) % MAX_PCB_NUM;
		}
		if (pcb[i].state != STATE_RUNNABLE)
			i = 0;
		current = i;
		/* echo pid of selected process */
		//putChar('0'+current);
		pcb[current].state = STATE_RUNNING;
		pcb[current].timeCount = 1;
		/* recover stackTop of selected process */
		tmpStackTop = pcb[current].stackTop;
		pcb[current].stackTop = pcb[current].prevStackTop;
		tss.esp0 = (uint32_t)&(pcb[current].stackTop); // setting tss for user process
		asm volatile("movl %0, %%esp"::"m"(tmpStackTop)); // switch kernel stack
		asm volatile("popl %gs");
		asm volatile("popl %fs");
		asm volatile("popl %es");
		asm volatile("popl %ds");
		asm volatile("popal");
		asm volatile("addl $8, %esp");
		asm volatile("iret");
	}
}

void keyboardHandle(struct StackFrame *sf) {//【格式化读入---写buffer=键盘中断】
//每按下一个按键就会触发一次键盘中断，每次只需要把恩下的那一个键的keycode放入buffer之中即可！
	uint32_t keyCode = getKeyCode();
	if (keyCode == 0) // illegal keyCode
		return;
	//【功能1：把读取到的keycode放入keybuffer之中】------Lab2中的实现
	//putChar(getChar(keyCode));
	uint32_t code = getKeyCode();
	int pos=0;
	uint16_t data=0;
	if(code == 0xe){ // 退格符
		//  要求只能退格用户键盘输入的字符串，且最多退到当行行首
		if(displayCol>0){
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
	
	//【功能2：V()操作！1、唤醒阻塞在dev[STD_IN]上的一个进程 2、创建资源】最多只能有一个进程被阻塞在dev[STD_IN]上
	//此时有buffer的输入，有资源可以读入啦！
	if (dev[STD_IN].state == 1 && dev[STD_IN].value < 0) { // with process blocked,此时需要唤醒他
		// TODO: deal with blocked situation
		//【先把他从阻塞列表中拿出来】
		ProcessTable* pt;
		pt = (ProcessTable*)((uint32_t)(dev[STD_IN].pcb.prev) - (uint32_t)&(((ProcessTable*)0)->blocked));
		dev[STD_IN].pcb.prev = (dev[STD_IN].pcb.prev)->prev;
		(dev[STD_IN].pcb.prev)->next = &(dev[STD_IN].pcb);
		//【再对他的信息进行修改】
		pt->state=STATE_RUNNABLE;
		//pt->timecount=MAX_TIME_COUNT;这两行最好别加，为了保证唤醒后的运行逻辑不发生过改变，原来时间片剩多长时间就运行多久！
		//pt->sleeptime=0;--------------加这两行也不会错，只是调度会和期望的不同
		dev[STD_IN].value = 1;//【因为最多只能有一个线程被阻塞，唤醒了之后全部可以读！》》此时有一个字符可以由本读入！！！】
		asm volatile("int $0x20");//符合逻辑，此时有一个进程被唤醒，发时间中断，看调度器会不会调度他！---------不加应该也没事
	}
	
	return;
}

void syscallHandle(struct StackFrame *sf) {
	switch(sf->eax) { // syscall number
		case SYS_WRITE:
			syscallWrite(sf);
			break; // for SYS_WRITE
		case SYS_READ:
			syscallRead(sf);
			break; // for SYS_READ
		case SYS_FORK:
			syscallFork(sf);
			break; // for SYS_FORK
		case SYS_EXEC:
			syscallExec(sf);
			break; // for SYS_EXEC
		case SYS_SLEEP:
			syscallSleep(sf);
			break; // for SYS_SLEEP
		case SYS_EXIT:
			syscallExit(sf);
			break; // for SYS_EXIT
		case SYS_SEM:
			syscallSem(sf);
			break; // for SYS_SEM
		default:break;
	}
}

void syscallWrite(struct StackFrame *sf) {
	switch(sf->ecx) { // file descriptor
		case STD_OUT:
			if (dev[STD_OUT].state == 1)
				syscallWriteStdOut(sf);
			break; // for STD_OUT
		default:break;
	}
}

void syscallWriteStdOut(struct StackFrame *sf) {
	int sel = sf->ds; // segment selector for user data, need further modification
	char *str = (char*)sf->edx;
	int size = sf->ebx;
	int i = 0;
	int pos = 0;
	char character = 0;
	uint16_t data = 0;
	asm volatile("movw %0, %%es"::"m"(sel));
	for (i = 0; i < size; i++) {
		asm volatile("movb %%es:(%1), %0":"=r"(character):"r"(str+i));
		if(character == '\n') {
			displayRow++;
			displayCol=0;
			if(displayRow==MAX_ROW){
				displayRow=MAX_ROW-1;
				displayCol=0;
				scrollScreen();
			}
		}
		else {
			data = character | (0x0c << 8);
			pos = (MAX_COL*displayRow+displayCol)*2;
			asm volatile("movw %0, (%1)"::"r"(data),"r"(pos+0xb8000));
			displayCol++;
			if(displayCol==MAX_COL){
				displayRow++;
				displayCol=0;
				if(displayRow==MAX_ROW){
					displayRow=MAX_ROW-1;
					displayCol=0;
					scrollScreen();
				}
			}
		}
	}
	
	updateCursor(displayRow, displayCol);
	return;
}

void syscallRead(struct StackFrame *sf) {//【格式化读入---读buffer】
	switch(sf->ecx) {
		case STD_IN:
			if (dev[STD_IN].state == 1)
				syscallReadStdIn(sf);
			break; // for STD_IN
		default:
			break;
	}
}

void syscallReadStdIn(struct StackFrame *sf) {
	// TODO: complete `stdin`
	//1、P()操作，消耗资源 + 如果dev[STD_IN].value=0，当前进程阻塞
	//2、读keybuffer中的数据
	//dev[STD_IN].value--;【此时value>0的时候是可以读入的字符数量---可以全读完！！！！！value<0的时候是阻塞的数量】
	
	if(dev[STD_IN].state ==1 && dev[STD_IN].value < 0){//已经有一个进程阻塞！而且当前又有进程想读》》多个想读，阻塞 && 而且没有资源
        	pcb[current].regs.eax = -1;//XXX：如果多个进程想读，后来的进程(pcb[current])返回-1。【下面其他情况返回实际读取的字符数】
		//XXX:为了保证只有一个进程被阻塞在dev[STD_IN]之中，当前进程运行到这里，如果已经value<0就不会被加入到阻塞列表中，而直接给返回值-1！
        	return;
    	}
	else if(dev[STD_IN].state==1 && dev[STD_IN].value==0){//一个进程想读&& 而且没有资源。加入阻塞列表+修改信息
		pcb[current].blocked.next = dev[STD_IN].pcb.next;
		pcb[current].blocked.prev = &(dev[STD_IN].pcb);
		dev[STD_IN].pcb.next = &(pcb[current].blocked);
		(pcb[current].blocked.next)->prev = &(pcb[current].blocked);

		pcb[current].state = STATE_BLOCKED;
		pcb[current].sleepTime = 0;
		pcb[current].regs.eax = 0;//XXX：一个进程&没有资源，返回0（一个都读不出来）
		dev[STD_IN].value--;
		asm volatile("int $0x20");
		return ;
	}

	int sel = sf->ds;
	char *str = (char *)sf->edx;
	int size = sf->ebx;
	int i = 0;
	char character = 0;
	asm volatile("movw %0, %%es" ::"m"(sel));
	for (i = 0; i < size && bufferHead != bufferTail; i++){
		character = keyBuffer[bufferHead];
		bufferHead = (bufferHead + 1) % MAX_KEYBUFFER_SIZE;
		asm volatile("movb %0, %%es:(%1)" ::"r"(character), "r"(str + i));
	}
	asm volatile("movb $0x00, %%es:(%0)" ::"r"(str + i));
	pcb[current].regs.eax = i;//XXX：没有进程阻塞&有资源，返回读入的个数！
	dev[STD_IN].value=0;
	return ;


}

void syscallFork(struct StackFrame *sf) {
	int i, j;
	for (i = 0; i < MAX_PCB_NUM; i++) {
		if (pcb[i].state == STATE_DEAD)
			break;
	}
	if (i != MAX_PCB_NUM) {
		/* copy userspace
		   enable interrupt
		 */
		enableInterrupt();
		for (j = 0; j < 0x100000; j++) {
			*(uint8_t *)(j + (i+1)*0x100000) = *(uint8_t *)(j + (current+1)*0x100000);
			//asm volatile("int $0x20"); // Testing irqTimer during syscall
		}
		/* disable interrupt
		 */
		disableInterrupt();
		/* set pcb
		   pcb[i]=pcb[current] doesn't work
		*/
		pcb[i].stackTop = (uint32_t)&(pcb[i].stackTop) -
			((uint32_t)&(pcb[current].stackTop) - pcb[current].stackTop);
		pcb[i].prevStackTop = (uint32_t)&(pcb[i].stackTop) -
			((uint32_t)&(pcb[current].stackTop) - pcb[current].prevStackTop);
		pcb[i].state = STATE_RUNNABLE;
		pcb[i].timeCount = pcb[current].timeCount;
		pcb[i].sleepTime = pcb[current].sleepTime;
		pcb[i].pid = i;
		/* set regs */
		pcb[i].regs.ss = USEL(2+i*2);
		pcb[i].regs.esp = pcb[current].regs.esp;
		pcb[i].regs.eflags = pcb[current].regs.eflags;
		pcb[i].regs.cs = USEL(1+i*2);
		pcb[i].regs.eip = pcb[current].regs.eip;
		pcb[i].regs.eax = pcb[current].regs.eax;
		pcb[i].regs.ecx = pcb[current].regs.ecx;
		pcb[i].regs.edx = pcb[current].regs.edx;
		pcb[i].regs.ebx = pcb[current].regs.ebx;
		pcb[i].regs.xxx = pcb[current].regs.xxx;
		pcb[i].regs.ebp = pcb[current].regs.ebp;
		pcb[i].regs.esi = pcb[current].regs.esi;
		pcb[i].regs.edi = pcb[current].regs.edi;
		pcb[i].regs.ds = USEL(2+i*2);
		pcb[i].regs.es = pcb[current].regs.es;
		pcb[i].regs.fs = pcb[current].regs.fs;
		pcb[i].regs.gs = pcb[current].regs.gs;
		/* set return value */
		pcb[i].regs.eax = 0;
		pcb[current].regs.eax = i;
	}
	else {
		pcb[current].regs.eax = -1;
	}
	return;
}

void syscallExec(struct StackFrame *sf) {
	return;
}

void syscallSleep(struct StackFrame *sf) {
	if (sf->ecx == 0)
		return;
	else {
		pcb[current].state = STATE_BLOCKED;
		pcb[current].sleepTime = sf->ecx;
		asm volatile("int $0x20");
		return;
	}
}

void syscallExit(struct StackFrame *sf) {
	pcb[current].state = STATE_DEAD;
	asm volatile("int $0x20");
	return;
}

//信号量操作的分发

void syscallSem(struct StackFrame *sf) {
	switch(sf->ecx) {
		case SEM_INIT:
			syscallSemInit(sf);
			break;
		case SEM_WAIT:
			syscallSemWait(sf);
			break;
		case SEM_POST:
			syscallSemPost(sf);
			break;
		case SEM_DESTROY:
			syscallSemDestroy(sf);
			break;
		default:break;
	}
}


/*
XXX:以下所有的参数都是传的uint32_t，如果是*sem，就是当前信号量在sem数组中的下标！！！
int sem_init(sem_t *sem, uint32_t value) {
	*sem = syscall(SYS_SEM, SEM_INIT,  value, 0, 0, 0);------syscall中参数存放的位置 eax(系统调用号) ecx（参数1） edx（参数2）
	if (*sem != -1)
		return 0;
	else
		return -1;
}

int sem_wait(sem_t *sem) {
	return syscall(SYS_SEM, SEM_WAIT, *sem, 0, 0, 0);-----edx存放指针sem！
}

int sem_post(sem_t *sem) {
	return syscall(SYS_SEM, SEM_POST, *sem, 0, 0, 0);
}

int sem_destroy(sem_t *sem) {
	return syscall(SYS_SEM, SEM_DESTROY, *sem, 0, 0, 0);
}

*/

//XXX：以下调用这些函数的都是当前进程pcb[current]!!!返回值也是都针对当前进程而返回的！！！
void syscallSemInit(struct StackFrame *sf) {//从sem数组中拿一个出来进行初始化
	// TODO: complete `SemInit`
 disableInterrupt();

	int value = (int)sf->edx;//memory.h中定义的是uint32_t类型的,不改会报错
	int free;
    	for (free = 0; free < MAX_SEM_NUM; free++) {
        	if (sem[free].state == 0) 
			break;
    	}
   	if (free == MAX_SEM_NUM)
        	pcb[current].regs.eax = -1;//没有空位置能用来初始化，由定义返回-1
    	else {
        	sem[free].state = 1;
		sem[free].value= value;
        	sem[free].pcb.prev = &sem[free].pcb;//kernel初始化的时候两个前后指针都指向自己呢
        	sem[free].pcb.next = &sem[free].pcb;
       		pcb[current].regs.eax = free;//下标当作返回值，用户程序能找到
    	}	
enableInterrupt();
	return;
}

void syscallSemWait(struct StackFrame *sf) {
	// TODO: complete `SemWait` and note that you need to consider some special situations--输入的参数不合法！（信号量不可用或范围）
	//XXX 习惯！！！先考虑不合法的情况！！！XXX
 disableInterrupt();

	int index = (int)(sf->edx);
	if(index < 0 || index >= MAX_SEM_NUM || sem[index].state == 0)
		pcb[current].regs.eax=-1;
	else{//此时传入的下标满足。开始执行P操作
		sem[index].value--;
		if(sem[index].value<0){
			pcb[current].state=STATE_BLOCKED;
			pcb[current].sleepTime=0x7fffffff;//给他最大的睡眠时间，只有V操作的唤醒+时间中断重新调度会让他不再睡眠！
            		pcb[current].blocked.next = sem[index].pcb.next;
            		pcb[current].blocked.prev = &(sem[index].pcb);
            		sem[index].pcb.next = &(pcb[current].blocked);
            		(pcb[current].blocked.next)->prev = &(pcb[current].blocked);
            		pcb[current].regs.eax = 0;
			asm("int $0x20");//引发时间中断，重新调度
		}
	}
enableInterrupt();
	return ;
}

void syscallSemPost(struct StackFrame *sf) {

 disableInterrupt();
	int i = (int)sf->edx;
	ProcessTable *pt = NULL;
	if (i < 0 || i >= MAX_SEM_NUM || sem[i].state==0) {// TODO: complete other situations
		pcb[current].regs.eax = -1;
		return;
	}
	
	//可以执行V
	sem[i].value++;
	if(sem[i].value <= 0){
		pt = (ProcessTable*)((uint32_t)(sem[i].pcb.prev) -(uint32_t)&(((ProcessTable*)0)->blocked));//取出来的进程
		sem[i].pcb.prev = (sem[i].pcb.prev)->prev;
		(sem[i].pcb.prev)->next = &(sem[i].pcb);
		pt->state=STATE_RUNNABLE;
		pcb[current].regs.eax=0;
		asm("int $0x20");
	}
enableInterrupt();
	return ;

}

void syscallSemDestroy(struct StackFrame *sf) {//销毁下标是sf->edx的信号量，即恢复原样！
	// TODO: complete `SemDestroy`
 disableInterrupt();
	int index=(int)(sf->edx);
	if(index<0 || index >= MAX_SEM_NUM || sem[index].state==0)
		pcb[current].regs.eax=-1;
	else{
		sem[index].state = 0;
		sem[index].value =0;
		sem[index].pcb.next=&(sem[index].pcb);
		sem[index].pcb.prev=&(sem[index].pcb);
		pcb[current].regs.eax=0;
	} 
enableInterrupt();
	return;
}
