#include "device.h"
#include "x86.h"
#include "common.h"
extern TSS tss;
extern int displayRow;
extern int displayCol;

extern ProcessTable pcb[MAX_PCB_NUM];
extern int current; // current process

void GProtectFaultHandle(struct StackFrame *sf);

void timerHandle(struct StackFrame *sf);

void syscallHandle(struct StackFrame *sf);

void syscallWrite(struct StackFrame *sf);
void syscallPrint(struct StackFrame *sf);
void syscallFork(struct StackFrame *sf);
void syscallExec(struct StackFrame *sf);
void syscallSleep(struct StackFrame *sf);
void syscallExit(struct StackFrame *sf);

void irqHandle(struct StackFrame *sf) {  // pointer sf = esp
    /* Reassign segment register */
    asm volatile("movw %%ax, %%ds" ::"a"(KSEL(SEG_KDATA)));
    /* Save esp to stackTop */
    uint32_t tmpStackTop = pcb[current].stackTop;
    pcb[current].prevStackTop = pcb[current].stackTop;
    pcb[current].stackTop = (uint32_t)sf;

    switch (sf->irq) {
        case -1:
            break;
        case 0xd:
            GProtectFaultHandle(sf);
            break;
        case 0x20:
            timerHandle(sf);
            break;
        case 0x80:
            syscallHandle(sf);
            break;
        default:
            assert(0);
    }

    /* Recover stackTop */
    pcb[current].stackTop = tmpStackTop;
}

void GProtectFaultHandle(struct StackFrame *sf) {
    assert(0);
    return;
}

void syscallHandle(struct StackFrame *sf) {
    switch (sf->eax) {  // syscall number
        case 0:
            syscallWrite(sf);
            break;  // for SYS_WRITE (0)
	case 1://fork
		syscallFork(sf);
		break;
	case 3://sleep
		syscallSleep(sf);
		break;
	case 4://exit
		syscallExit(sf);
		break;
        default:
            break;
    }
}


void memcpy(void* dst,void* buffer,size_t size){
	for(uint32_t j=0;j<size;j++){
		*(uint8_t*)(dst+j)=*(uint8_t*)(buffer+j);
	}
}


static int front=0;
static int rear=1;
static int tag=0;
static int ra_list[MAX_PCB_NUM]={1,0,0,0};//状态为STATE_RUNNABLE进程的下标，用循环数组来模拟链表的实现！
static int index;


void timerHandle(struct StackFrame *sf) {
    // TODO in lab3
	for(int i=0;i<MAX_PCB_NUM;i++){//【对阻塞态的进程操作】
		if(pcb[i].state==STATE_BLOCKED && pcb[i].sleepTime>1)
			pcb[i].sleepTime--;
		else if (pcb[i].state==STATE_BLOCKED && pcb[i].sleepTime==1){
			pcb[i].state=STATE_RUNNABLE;//[阻塞态->就绪态，装入ra_list中！！！]
			pcb[i].sleepTime=0;
			if(!(rear==front && tag)){//ra_list队列中没有满
				tag=1;
				ra_list[rear]=i;
				rear=(rear+1)%MAX_PCB_NUM;	
			}	
		}
	}

	if(pcb[current].state==STATE_RUNNING){//【对运行态的进程操作，也即current】
		pcb[current].timeCount++;
		if(pcb[current].timeCount == MAX_TIME_COUNT)
			return;
	}
	for(index=(current+1)%MAX_PCB_NUM; index!=current; index=(index+1)%MAX_PCB_NUM){
		if(pcb[index].state==STATE_RUNNABLE)//找到一个就绪态的进程为止,更新index！
			break;
	}
	if(pcb[current].state==STATE_RUNNING){//【【【BUG！！！！当前进程可能不是运行态的！！！这一条if判断不能去掉！！！】】】
		pcb[current].state=STATE_RUNNABLE;
		pcb[current].timeCount=0;
	}
	current=index;
	pcb[current].state=STATE_RUNNING;
	pcb[current].timeCount=0;
	uint32_t temp=pcb[current].stackTop;
	pcb[current].stackTop=pcb[current].prevStackTop;
	tss.esp0=(uint32_t)&(pcb[current].stackTop);
	asm volatile("movl %0, %%esp"::"m"(temp)); // switch kernel stack
	asm volatile("popl %gs");
	asm volatile("popl %fs");
	asm volatile("popl %es");
	asm volatile("popl %ds");
	asm volatile("popal");
	asm volatile("addl $8, %esp");
	asm volatile("iret");	

}



void syscallWrite(struct StackFrame *sf) {
    switch (sf->ecx) {  // file descriptor
        case 0:
            syscallPrint(sf);
            break;  // for STD_OUT
        default:
            break;
    }
}

// Attention:【可选择性的作业，解决了syscallPrint的一致性问题】
// This is optional homework, because now our kernel can not deal with
// consistency problem in syscallPrint. If you want to handle it, complete this
// function. But if you're not interested in it, don't change anything about it
void syscallPrint(struct StackFrame *sf) {
    int sel = sf->ds;  // TODO segment selector for user data, need further
                       // modification
    char *str = (char *)sf->edx;
    int size = sf->ebx;
    int i = 0;
    int pos = 0;
    char character = 0;
    uint16_t data = 0;
    asm volatile("movw %0, %%es" ::"m"(sel));
    for (i = 0; i < size; i++) {
        asm volatile("movb %%es:(%1), %0" : "=r"(character) : "r"(str + i));
        if (character == '\n') {
            displayRow++;
            displayCol = 0;
            if (displayRow == 25) {
                displayRow = 24;
                displayCol = 0;
                scrollScreen();
            }
        } else {
            data = character | (0x0c << 8);
            pos = (80 * displayRow + displayCol) * 2;
            asm volatile("movw %0, (%1)" ::"r"(data), "r"(pos + 0xb8000));
            displayCol++;
            if (displayCol == 80) {
                displayRow++;
                displayCol = 0;
                if (displayRow == 25) {
                    displayRow = 24;
                    displayCol = 0;
                    scrollScreen();
                }
            }
        }
        // asm volatile("int $0x20"); //XXX Testing irqTimer during syscall
        // asm volatile("int $0x20":::"memory"); //XXX Testing irqTimer during
        // syscall
    }

    updateCursor(displayRow, displayCol);
    // TODO take care of return value
    //sf->eax=size;
    return;
}

void syscallFork(struct StackFrame *sf) {
	//TODO:
    // 把父进程的全部地址空间复制到子进程之中，设置【除了eax之外的】寄存器（如ebx ecx等）。eax要作为fork的返回值对父、子进程单独设置！！！
    // tip：复制父进程的pcb时不能完全复制，如ss、ds、cs不能完全copy！！！。eflags要通过复制而非汇编。要考虑fork失败的情况！！！
	//step1:从pcb数组中找到一个空的位置，给子进程分配【要考虑失败的情况！！！】
	//step2：把父进程的全部地址空间复制到子进程中去！
	//step3：设置子进程的pcb，部分可以拷贝父进程。部分不可以拷贝！！！【参考kvm.c中的实现】


	//XXX:step1:
	int child;
	for(child =0;child<MAX_PCB_NUM;child++){
		if(pcb[child].state==STATE_DEAD){//找到了空的位置（状态是dead呢！）
			break;
		}
	}
	if(child == MAX_PCB_NUM)//没有空位置
		{sf->eax=-1;return;}//此时fork失败了！在父进程处返回-1啦！ 

	//XXX:step2
	//【现在child就是子进程在pcb中的位置啦！】
	memcpy((void*)((child+1)*0x100000),(void*)((current+1)*0x100000),0x100000);
	
	//XXX:step3
	memcpy(&pcb[child],&pcb[current],sizeof(ProcessTable));//继承了父进程的信息
	pcb[child].regs.eax=0;//子进程调用fork之后的返回值
	sf->eax = child;//父进程调用fork之后的返回值

	//以下是对父进程pcb部分信息的修改！
	pcb[child].pid = child;
	pcb[child].sleepTime = 0;
	pcb[child].timeCount = 0;
	pcb[child].state = STATE_RUNNABLE;
	if(!(front==rear && tag)){//此时RUNNABLE列表没有满，当然，最多创建16个啦，不然就pcb没有空位置，直接fork失败返回啦！
		ra_list[rear]=child;
		rear=(rear+1)%MAX_PCB_NUM;
		tag=1;
	}
	//当前子进程在GDT中的下标为，  【代码段】 1（空）+ 2*child 【数据段】1（空）+2*child+1
	pcb[child].regs.cs = USEL(1+2*child);//代码
	pcb[child].regs.ds = USEL(2+2*child);//数据
	pcb[child].regs.es = USEL(2+2*child);
	pcb[child].regs.fs = USEL(2+2*child);
	pcb[child].regs.gs = USEL(2+2*child);
	pcb[child].regs.ss = USEL(2+2*child); 
	pcb[child].regs.eflags = pcb[current].regs.eflags | 0x200;
	pcb[child].stackTop = (uint32_t)&(pcb[child].regs);//本进程的上下文信息全在regs之中了
	pcb[child].prevStackTop = (uint32_t)&(pcb[child].stackTop);//中断嵌套时保存待恢复的栈顶信息（用不到呢！）

}

void syscallSleep(struct StackFrame *sf) {
    // TODO in lab3
	//在syscall中，第二个参数在ecx之中。current是pcb数组中当前进程的下标
	if(sf->ecx >= 0){
		pcb[current].state=STATE_BLOCKED;
		pcb[current].sleepTime=sf->ecx;
		asm volatile("int $0x20");//模拟时钟中断，通过系统调用号0x20进行系统调用，调用timerHandle进行进程切换。调度新的进程
	}	
}

void syscallExit(struct StackFrame *sf) {
    // TODO in lab3
    pcb[current].state=STATE_DEAD;
    asm volatile("int $0x20");
    
}
