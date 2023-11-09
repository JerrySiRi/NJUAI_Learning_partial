#include "boot.h"

#define SECTSIZE 512

//【通过本文件加载app，即微型OS.在保护模式下加载app，使用readSect函数进行磁盘扇区的读取】
//1、把app.bin的内容读到0x8c00中，app.bin长度为58字节
//2、跳转到0x8c00【使用内联汇编】
void bootMain(void) {
//【法一：可以通过函数指针，通过执行一个什麼都不作的函数，其函数首地址在0x8c00(Hello World程序的首地址)，来完成地址的跳转！】
	//void(*dest)(void)=(void(*))0x8c00;
	//readSect((void*)dest,1);
	//dest();
	
//【法二：通过内联汇编来无条件跳转】
	void(*dest)(void)=(void(*))0x8c00;
	readSect((void*)dest,1);
	asm(
	"mov $0x8c00,%ax \n\t"
	"jmp  *%ax"
	);
	//【【jmp后面跟符号、寄存器（编译自动补全*）、*寄存器都可以呢！！！】】
}

void waitDisk(void) { // waiting for disk
	while((inByte(0x1F7) & 0xC0) != 0x40);
}

void readSect(void *dst, int offset) { // reading a sector of disk
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
