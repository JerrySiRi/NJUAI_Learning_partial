#include "x86.h"
#include "device.h"

SegDesc gdt[NR_SEGMENTS];       // the new GDT, NR_SEGMENTS=7, defined in x86/memory.h
TSS tss;

void initSeg() { // setup kernel segements
	gdt[SEG_KCODE] = SEG(STA_X | STA_R, 0,       0xffffffff, DPL_KERN);
	gdt[SEG_KDATA] = SEG(STA_W,         0,       0xffffffff, DPL_KERN);
	//gdt[SEG_UCODE] = SEG(STA_X | STA_R, 0,       0xffffffff, DPL_USER);
	gdt[SEG_UCODE] = SEG(STA_X | STA_R, 0x00200000,0x000fffff, DPL_USER);
	//gdt[SEG_UDATA] = SEG(STA_W,         0,       0xffffffff, DPL_USER);
	gdt[SEG_UDATA] = SEG(STA_W,         0x00200000,0x000fffff, DPL_USER);
	gdt[SEG_TSS] = SEG16(STS_T32A,      &tss, sizeof(TSS)-1, DPL_KERN);
	gdt[SEG_TSS].s = 0;
	setGdt(gdt, sizeof(gdt)); // gdt is set in bootloader, here reset gdt in kernel

	/*
	 * 初始化TSS：不需要初始化esp1，esp2，esp3呢！
	 */
	tss.esp0 = 0x1fffff;
	tss.ss0 = KSEL(SEG_KDATA);
	asm volatile("ltr %%ax":: "a" (KSEL(SEG_TSS)));

	/*设置正确的段寄存器*/
	asm volatile("movw %%ax,%%ds":: "a" (KSEL(SEG_KDATA)));
	//asm volatile("movw %%ax,%%es":: "a" (KSEL(SEG_KDATA)));
	//asm volatile("movw %%ax,%%fs":: "a" (KSEL(SEG_KDATA)));
	//asm volatile("movw %%ax,%%gs":: "a" (KSEL(SEG_KDATA)));
	asm volatile("movw %%ax,%%ss":: "a" (KSEL(SEG_KDATA)));

	lLdt(0);
	
}

void enterUserSpace(uint32_t entry) {
	/*
	 * Before enter user space 
	 * you should set the right segment registers here
	 * and use 'iret' to jump to ring3
	 */
	uint32_t EFLAGS = 0;
	asm volatile("pushl %0":: "r" (USEL(SEG_UDATA))); // push ss
	asm volatile("pushl %0":: "r" (0x2fffff)); 
	asm volatile("pushfl"); //push eflags, sti
	asm volatile("popl %0":"=r" (EFLAGS));
	asm volatile("pushl %0"::"r"(EFLAGS|0x200));
	asm volatile("pushl %0":: "r" (USEL(SEG_UCODE))); // push cs
	asm volatile("pushl %0":: "r" (entry)); 
	asm volatile("iret");
}

/*
kernel is loaded to location 0x100000, i.e., 1MB
size of kernel is not greater than 200*512 bytes, i.e., 100KB
user program is loaded to location 0x200000, i.e., 2MB
size of user program is not greater than 200*512 bytes, i.e., 100KB
*/

/*---自己写的
void loadUMain(void) {
	// TODO: 在内核中加载用户程序，参照bootloader加载内核的方式
	int i = 0;
	int phoff = 0x34;//elf头的大小是52字节，要先偏52。之后就是程序头表啦
	int offset = 0x1000;//.text节的偏移
	unsigned int elf = 0x200000;//ppt中说用户程序的.text段的起始是0x200000，也就是elf文件的起始啦
	//【函数指针！下面相当于告诉这个函数指针的位置，用两外一个什麼都不做，只有位置的函数来赋予它】
	uint32_t uMainEntry=0x200000;

	for (i = 0; i < 200; i++) {//磁盘分布：0号-bootloader。1-200号是内核部分。201-之后是用户程序部分
		readSect((void*)(elf + i*512), 1+i);
	}
	uMainEntry =((struct ELFHeader*)elf)->entry;//内核程序的入口地址,函数的入口地址
	phoff =((struct ELFHeader*)elf)->phoff;//程序头表的较elf的偏移位置
	offset =((struct ProgramHeader *)(elf+phoff))->off;//【Segment在ELF文件中的偏移量】先找到程序头表的位置(elf+phoff)，再引用它。

	for (i = 0; i < 200 * 512; i++) {
		*(unsigned char *)(elf + i) = *(unsigned char *)(elf + i + offset);
	}
	enterUserSpace(uMainEntry);
}
*/

void loadUMain(void) {
	// TODO: 参照bootloader加载内核的方式
	uint32_t elf = 0x200000;
	for (int i = 0; i < 200; i++) {
		readSect((void*)(elf + i*512), 201+i);
	}
	// TODO: 填写kMainEntry、phoff、offset
	struct ELFHeader * eh = (struct ELFHeader *)elf;
	struct ProgramHeader *ph = (struct ProgramHeader *)(elf + eh->phoff);
	struct ProgramHeader *eph = (struct ProgramHeader *)(ph + eh->phnum);
	int j = 0;
	for(;ph < eph;ph++)
	{
		if(ph->type == 1)
		{
			for(j = 0;j < ph->filesz;j++)
			{
				*(unsigned char*)(ph->paddr+j) = *(unsigned char*)(elf+ph->off+j);
			}
			for(;j < ph->memsz;j++)
			{
				*(unsigned char*)(ph->paddr+j) = (unsigned char)0;
			}
		}
	}
	uint32_t uMainEntry = ((struct ELFHeader *)elf)->entry - 0x200000;
	enterUserSpace(uMainEntry);
}



/*【bootloader记载内核的情况】
void bootMain(void) {
	int i = 0;
	int phoff = 0x34;//elf头的大小是52字节，要先偏52。之后就是程序头表啦
	int offset = 0x1000;
	unsigned int elf = 0x100000;//内核.text段在编译的时候的起始地址是0x100000。加载到物理内存0x100000开始的位置.//Elf文件也被放到了0x100000的位置！！！
	
	void (*kMainEntry)(void);//【函数指针！】
	kMainEntry = (void(*)(void))0x100000;//tip：此时kMainEntry、phoff、offset的值只是初始化一下,不是准确的

	for (i = 0; i < 200; i++) {//磁盘分布：0号-bootloader。1-200号是内核部分。201-之后是用户程序部分
		readSect((void*)(elf + i*512), 1+i);
	}
	//本质上就是从kernel elf文件中解析出【程序入口】，【偏移量】等信息。【利用ELF头的数据结构以及程序头表对应的数据结构来进行解析】
	// TODO: 填写kMainEntry、phoff、offset

	kMainEntry =(void(*)(void))((struct ELFHeader*)elf)->entry;//内核程序的入口地址,函数的入口地址
	phoff =((struct ELFHeader*)elf)->phoff;//程序头表的较elf的偏移位置
	offset =((struct ProgramHeader *)(elf+phoff))->off;//先找到程序头表的位置，再引用它。

	for (i = 0; i < 200 * 512; i++) {
		*(unsigned char *)(elf + i) = *(unsigned char *)(elf + i + offset);
	}

	kMainEntry();//同lab1，一个什麼都不作的函数完成了地址跳转！
}


*/
