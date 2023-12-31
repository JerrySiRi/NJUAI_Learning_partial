#include "x86.h"
#include "device.h"


//显示的行、列数。qumu屏幕能显示80*25大小的数据
int displayRow = 0;
int displayCol = 0;
uint16_t displayMem[80*25];
int displayClear = 0;

void initVga() {
	displayRow = 0;
	displayCol = 0;
	displayClear = 0;
	clearScreen();
	updateCursor(0, 0);
}

//80*25大小的屏幕被清空
void clearScreen() {
	int i = 0;
	int pos = 0;
	uint16_t data = 0 | (0x0c << 8);
	for (i = 0; i < 80 * 25; i++) {
		pos = i * 2;
		asm volatile("movw %0, (%1)"::"r"(data),"r"(pos+0xb8000));
	}
}


//更新光表的位置
void updateCursor(int row, int col){
	int cursorPos = row * 80 + col;
	outByte(0x3d4, 0x0f);
	outByte(0x3d5, (unsigned char)(cursorPos & 0xff));

	outByte(0x3d4, 0x0e);
	outByte(0x3d5, (unsigned char)((cursorPos>>8) & 0xff));
}


//滚屏
void scrollScreen() {
	int i = 0;
	int pos = 0;
	uint16_t data = 0;
	for (i = 0; i < 80 * 25; i++) {
		pos = i * 2;
		asm volatile("movw (%1), %0":"=r"(data):"r"(pos+0xb8000));
		displayMem[i] = data;
	}
	for (i = 0; i < 80 * 24; i++) {
		pos = i * 2;
		data = displayMem[i+80];
		asm volatile("movw %0, (%1)"::"r"(data),"r"(pos+0xb8000));
	}
	data = 0 | (0x0c << 8);
	for (i = 80 * 24; i < 80 * 25; i++) {
		pos = i * 2;
		asm volatile("movw %0, (%1)"::"r"(data),"r"(pos+0xb8000));
	}
}
