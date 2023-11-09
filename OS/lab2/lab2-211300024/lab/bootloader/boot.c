#include "boot.h"

#define SECTSIZE 512

/*
void bootMain(void) {
	int i = 0;
	void (*elf)(void);
	elf = (void(*)(void))0x100000; // kernel is loaded to location 0x100000
	for (i = 0; i < 200; i ++) {
		//readSect((void*)elf + i*512, i+1);
		readSect((void*)elf + i*512, i+9);
	}
	elf(); // jumping to the loaded program
}
*/


/*
//【TASK1】加载程序装载内核
void bootMain(void) {
	int i = 0;
	int phoff = 0x34;
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

void bootMain(void) {
	unsigned int elf = 0x200000;
	for (int i = 0; i < 200; i++) {
		readSect((void*)(elf + i*512), 1+i);
	}
	// TODO: 填写kMainEntry、phoff、offset,加载Kernel
	struct ELFHeader * eh = (struct ELFHeader *)elf;
	struct ProgramHeader *ph = (struct ProgramHeader *)(elf + eh->phoff);
	struct ProgramHeader *eph = (struct ProgramHeader *)(ph + eh->phnum);
	int j = 0;
	for(; ph < eph; ph++){
		if(ph->type == 1){  //同PA啦，只装载可以装载的段！
			for(j = 0;j < ph->filesz;j++){
				*(unsigned char*)(ph->paddr+j) = *(unsigned char*)(elf+ph->off+j);
			}
			for(;j < ph->memsz;j++){//在上面可装入段所有内容完成装入后，内存中剩余的其它地方【.bss节】都初始化成0
				*(unsigned char*)(ph->paddr+j) = (unsigned char)0;
			}
		}
	}
	
	void (*kMainEntry)(void);
	kMainEntry = (void(*)(void))(((struct ELFHeader*)elf)->entry);
	kMainEntry();
}

void waitDisk(void) { // waiting for disk
	while((inByte(0x1F7) & 0xC0) != 0x40);
}

void readSect(void *dst, int offset) { // reading a sector of disk【从磁盘中读入offset号扇区的内容到*dst位置】
	int i;
	waitDisk();
	outByte(0x1F2, 1);
	outByte(0x1F3, offset);
	outByte(0x1F4, offset >> 8);
	outByte(0x1F5, offset >> 16);
	outByte(0x1F6, (offset >> 24) | 0xE0);
	outByte(0x1F7, 0x20);

	waitDisk();
	for (i = 0; i < SECTSIZE / 4; i ++) {
		((int *)dst)[i] = inLong(0x1F0);
	}
}
