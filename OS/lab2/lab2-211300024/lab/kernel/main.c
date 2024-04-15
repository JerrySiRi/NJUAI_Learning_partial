#include "common.h"
#include "x86.h"
#include "device.h"

void kEntry(void) {

	// Interruption is disabled in bootloader

	initSerial();// initialize serial port
	//TODO：【TASK2】装载内核-完善中断机制，提供系统服务函数
	initIdt();      // initialize idt【idt中断描述符表】
	initIntr();	// iniialize 8259a
	initSeg();	// initialize gdt, tss【gdt-全局描述符表】【tss-任务状态段】
	initVga(); 	// initialize vga device
	initKeyTable();	// initialize keyboard device
	loadUMain(); 	// load user program, enter user space

	while(1);
	assert(0);
}
