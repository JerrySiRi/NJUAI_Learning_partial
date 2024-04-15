# TODO: This is lab1.1
# 【通过本文件开启保护模式】

/*【part1】-- Real Mode Hello World */
# .code16
# .global start
# start:
# 	movw %cs, %ax
# 	movw %ax, %ds
# 	movw %ax, %es
# 	movw %ax, %ss
# 	movw $0x7d00, %ax
# 	movw %ax, %sp # setting stack pointer to 0x7d00
# 	pushw $13 # pushing the size to print into stack
# 	pushw $message # pushing the address of message into stack
# 	callw displayStr # calling the display function
# loop:
# 	jmp loop

# message:
# 	.string "Hello, World!\n\0"

# displayStr:
# 	pushw %bp
# 	movw 4(%esp), %ax
# 	movw %ax, %bp
# 	movw 6(%esp), %cx
# 	movw $0x1301, %ax
# 	movw $0x000c, %bx
# 	movw $0x0000, %dx
# 	int $0x10
# 	popw %bp
# 	ret

#【1.1完成版本】

# .code16
# .global start
# start:
# 	movw %cs, %ax
# 	movw %ax, %ds
# 	movw %ax, %es
# 	movw %ax, %ss 			#【以上，用cs来初始化段寄存器ds、es、ss】
# 	movw $0x7d00, %ax
# 	movw %ax, %sp 			# 【setting stack pointer to 0x7d00-栈指针指向7d00】
# 	pushw $13 			# 【pushing the size to print into stack】
# 	pushw $message 			# 【pushing the address of message into stack】
#	callw displayStr	        # 【calling the display function】
# loop:
# 	jmp loop

# message:
# 	.string "Hello, World!\n\0"	#【要放入战区中的字符串信息】

# displayStr:				#【用来显示在屏幕上的函数，其中包含系统调用int $0x10-BIOS来在实模式下相应中断】
# 	pushw %bp
# 	movw 4(%esp), %ax
# 	movw %ax, %bp
# 	movw 6(%esp), %cx
# 	movw $0x1301, %ax
# 	movw $0x000c, %bx
# 	movw $0x0000, %dx
# 	int $0x10
# 	popw %bp
# 	ret







# TODO: This is lab1.2
/* 【part2】-- Protected Mode Hello World  保护模式下的hello world*/
/*
  .code16
  .global start
  start:
      cli                             #关闭中断
      inb $0x92,%al		      #【TODO】
      orb $0x02,%al                   #【端口最后一位和倒数第二位都设置成1--可能有问题，最后一位快速启动是1是什么意思？】
      outb %al,$0x92
                                      #启动A20总线，开启A20的地址线【以上三条均是】
    
    
      data32 addr32 lgdt gdtDesc      #加载GDTR
      movl %cr0,%eax		      #【TODO】
      orl  $0x00000001,%eax
      movl %eax,%cr0
			                #启动保护模式【CR0是32位的】，即设置CR0的PE位（第0位）为1【PE从0设置到1】
    
                                      
      data32 ljmp $0x08, $start32       #长跳转切换至保护模式

  .code32
  start32:
      					#【TODO】在保护模式下，段寄存器就是段选择器，也就是段选择子                            
					#初始化DS ES FS GS SS 初始化栈顶指针ESP
	movw $0x0010,%ax
	movw %ax,%ds
	movw %ax,%es
	movw %ax,%fs
	movw %ax,%ss
	movw $0x0018,%ax  		 #【gs是视频段的起始】
	movw %ax,%gs
#没做完


  	pushl $13 # pushing the size to print into stack
  	pushl $message # pushing the address of message into stack
  	calll displayStr # calling the display function
 loop:
  	jmp loop

 message:
 	.string "Hello, World!\n\0"

 displayStr:
 	movl 4(%esp), %ebx
 	movl 8(%esp), %ecx
 	movl $((80*5+0)*2), %edi
 	movb $0x0c, %ah
 nextChar:
 	movb (%ebx), %al
 	movw %ax, %gs:(%edi)
 	addl $2, %edi
 	incl %ebx
 	loopnz nextChar       # loopnz decrease ecx by 1
 	ret

 gdt:
     .word 0,0                          #GDT第一个表项必须为空
     .byte 0,0,0,0
     .word 0xffff,0                          #代码段描述符
     .byte 0,0x9a,0xcf,0
        
     .word 0xffff,0                          #数据段描述符
     .byte 0,0x92,0xcf,0
        
     .word 0xffff,0x8000                     #视频段描述符
     .byte 0x0b,0x92,0xcf,0
     

 gdtDesc:
     .word (gdtDesc - gdt -1)
     .long gdt

*/








# TODO: This is lab1.3
/* 【part3】-- Protected Mode Loading Hello World APP 保护模式下加载hello worldAPP功能模块*/
  .code16
  .global start
  start:
      cli                             #关闭中断
      inb $0x92,%al		      #【TODO】
      orb $0x02,%al                   #【端口倒数第二位设置成1】
      outb %al,$0x92
                                      #启动A20总线，开启A20的地址线【以上三条均是】
    
    
      data32 addr32 lgdt gdtDesc      #加载GDTR
      movl %cr0,%eax		      #【TODO】
      orl  $0x00000001,%eax
      movl %eax,%cr0
			                #启动保护模式【CR0是32位的】，即设置CR0的PE位（第0位）为1【PE从0设置到1】
    
                                      
      data32 ljmp $0x08, $start32       #长跳转切换至保护模式

  .code32
  start32:
      					#【TODO】在保护模式下，段寄存器就是段选择器，也就是段选择子                            
					#初始化DS ES FS GS SS 初始化栈顶指针ESP
	movw $0x0010,%ax
	movw %ax,%ds
	movw %ax,%es
	movw %ax,%fs
	movw %ax,%ss
	movw $0x0018,%ax  		 #【gs是视频段的起始】
	movw %ax,%gs
#没做完


  	pushl $13 # pushing the size to print into stack
  	pushl $message # pushing the address of message into stack
  	calll displayStr # calling the display function
 Sloop:
  	jmp bootMain # jump to bootMain in boot.c

 message:
 	.string "Hello, World!\n\0"

 displayStr:
 	movl 4(%esp), %ebx
 	movl 8(%esp), %ecx
 	movl $((80*5+0)*2), %edi
 	movb $0x0c, %ah
 nextChar:
 	movb (%ebx), %al
 	movw %ax, %gs:(%edi)
 	addl $2, %edi
 	incl %ebx
 	loopnz nextChar       # loopnz decrease ecx by 1
 	ret

 gdt:
     .word 0,0                          #GDT第一个表项必须为空
     .byte 0,0,0,0
     .word 0xffff,0                          #代码段描述符
     .byte 0,0x9a,0xcf,0
        
     .word 0xffff,0                          #数据段描述符
     .byte 0,0x92,0xcf,0
        
     .word 0xffff,0x8000                     #视频段描述符
     .byte 0x0b,0x92,0xcf,0
     

 gdtDesc:
     .word (gdtDesc - gdt -1)
     .long gdt
