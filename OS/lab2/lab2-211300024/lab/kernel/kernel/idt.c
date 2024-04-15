#include "x86.h"
#include "device.h"

#define INTERRUPT_GATE_32   0xE
#define TRAP_GATE_32        0xF

/* IDT表的内容 */
struct GateDescriptor idt[NR_IRQ]; // NR_IRQ=256, defined in x86/cpu.h

/* 初始化一个中断门(interrupt gate) */
static void setIntr(struct GateDescriptor *ptr, uint32_t selector, uint32_t offset, uint32_t dpl) {
	// TODO: 初始化interrupt gate
	// ptr是指向这个256个门描述符中的某一个元素，使用传进来的三个参数来初始化它。除此之外其他信息是固定的
	ptr->offset_15_0 = offset & 0xFFFF;//类型是unit32_t，右移动高位补0.----------------自己写的：(offset<<16)>>16;
	ptr->offset_31_16 = (offset>>16)&0xFFFF;//通过与上一个长度更小的【显示地把】长度给截断-------自己写的，不加0xfffff
	ptr->segment = selector<<3;//自动截断，回顾lab1中的gdt表，选择子存入寄存器后，低三位是留给特权级的！！！
	ptr->present = 0x1;
	ptr->privilege_level = dpl;
	ptr->system = 0;
	ptr->type = 0xE;//也就是上面定义的INTERRUPT_GATE_32
	ptr->pad0 = 0;


}

/* 初始化一个陷阱门(trap gate) */
static void setTrap(struct GateDescriptor *ptr, uint32_t selector, uint32_t offset, uint32_t dpl) {
	// TODO: 初始化trap gate
	ptr->offset_15_0 = offset & 0xFFFF;//类型是unit32_t，右移动高位补0.----------------自己写的：(offset<<16)>>16;
        ptr->offset_31_16 = (offset>>16)&0xFFFF;//通过与上一个长度更小的【显示地把】长度给截断-------自己写的，不加0xfffff
        ptr->segment = selector<<3;//自动截断，回顾lab1中的gdt表，选择子存入寄存器后，低三位是留给特权级的！！！
        ptr->present = 0x1;//在memory.h文件中，定义了宏来完成selector的处理呢！
        ptr->privilege_level = dpl;
        ptr->system = 0;
        ptr->type = 0xF;//也就是上面定义的TRAP_GATE_32
        ptr->pad0 = 0;
}

/* 声明函数，这些函数在汇编代码里定义 */
void irqEmpty();
void irqErrorCode();

void irqDoubleFault(); // 0x8
void irqInvalidTSS(); // 0xa
void irqSegNotPresent(); // 0xb
void irqStackSegFault(); // 0xc
void irqGProtectFault(); // 0xd
void irqPageFault(); // 0xe
void irqAlignCheck(); // 0x11
void irqSecException(); // 0x1e
void irqKeyboard(); 

void irqSyscall();

void initIdt() {
	int i;
	/* 为了防止系统异常终止，所有irq都有处理函数(irqEmpty)。 */
	for (i = 0; i < NR_IRQ; i ++) {
		setTrap(idt + i, SEG_KCODE, (uint32_t)irqEmpty, DPL_KERN);
	}
	/*
	 * init your idt here
	 * 初始化 IDT 表, 为中断设置中断处理函数
	 */
	/* Exceptions with error code 【针对某些特定的中断向量，压入error code】*/
	//static void setTrap(struct GateDescriptor *ptr, uint32_t selector, uint32_t offset, uint32_t dpl)函数声明

	setTrap(idt + 0x8, SEG_KCODE, (uint32_t)irqDoubleFault, DPL_KERN);
	//offset是在对应的段中找到偏移量，而在汇编.S中的标记就是位置，可以认为是偏移量拉！
	// TODO: 填好剩下的表项
       	setTrap(idt + 0x8, SEG_KCODE, (uint32_t)irqDoubleFault, DPL_KERN);
	 setTrap(idt + 0xa, SEG_KCODE, (uint32_t)irqInvalidTSS, DPL_KERN);
	 setTrap(idt + 0xb, SEG_KCODE, (uint32_t)irqSegNotPresent, DPL_KERN);
	 setTrap(idt + 0xc, SEG_KCODE, (uint32_t)irqStackSegFault, DPL_KERN);
	 setTrap(idt + 0xd, SEG_KCODE, (uint32_t)irqGProtectFault, DPL_KERN);
	 setTrap(idt + 0xe, SEG_KCODE, (uint32_t)irqPageFault, DPL_KERN);
	 setTrap(idt + 0x11, SEG_KCODE, (uint32_t)irqAlignCheck, DPL_KERN);
	 setTrap(idt + 0x1e, SEG_KCODE, (uint32_t)irqSecException, DPL_KERN);
	
	/* Exceptions with DPL = 3 */
	// TODO: 填好剩下的表项 
	 setTrap(idt + 0x21, SEG_KCODE, (uint32_t)irqKeyboard, DPL_KERN);//irqKeyboard的调用号是0x21
	 setIntr(idt + 0x80, SEG_KCODE, (uint32_t)irqSyscall, DPL_USER); //irqSyacall的调用号是0x80
	 //系统调用的 int 0x80, 中断向量是 0x80, 在用户态，ring3发出的中断》DPL_USER=3
	/* 写入IDT */
	saveIdt(idt, sizeof(idt));
}
