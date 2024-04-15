#ifndef BOOT_H
#define BOOT_H

struct ELFHeader {
	unsigned int   magic;
	unsigned char  elf[12];
	unsigned short type;
	unsigned short machine;
	unsigned int   version;
	unsigned int   entry;//可执行程序的入口地址
	unsigned int   phoff;//Program头表的偏移地址
	unsigned int   shoff;
	unsigned int   flags;
	unsigned short ehsize;
	unsigned short phentsize;
	unsigned short phnum;
	unsigned short shentsize;
	unsigned short shnum;
	unsigned short shstrndx;
};

/* ELF32 Program header */
struct ProgramHeader {
	unsigned int type;
	unsigned int off;//Segment在ELF文件中的偏移量
	unsigned int vaddr;
	unsigned int paddr;
	unsigned int filesz;
	unsigned int memsz;
	unsigned int flags;
	unsigned int align;
};

void waitDisk(void);

void readSect(void *dst, int offset);

/* I/O functions */
static inline char inByte(short port) {
	char data;
	asm volatile("in %1,%0" : "=a" (data) : "d" (port));
	return data;
}

static inline int inLong(short port) {
	int data;
	asm volatile("in %1, %0" : "=a" (data) : "d" (port));
	return data;
}

static inline void outByte(short port, char data) {
	asm volatile("out %0,%1" : : "a" (data), "d" (port));
}

#endif
