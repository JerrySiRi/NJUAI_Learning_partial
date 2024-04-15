/*
otherwise need to reassign esp0 of tss in task switching for each user process
note that for conforming code OR same PRL, no need to switch task
that is TSS doesn't work
1. Trap Gate, IF won't be set
2. Interrupt Gate, IF is set automatically
3. System Gate
*/

.code32

.global irqEmpty
irqEmpty:
	pushl $0 // push dummy error code
	pushl $-1 // push interruption number into kernel
	jmp asmDoIrq

.global irqErrorCode
irqErrorCode:
	pushl $-1 // push interruption number into kernel
	jmp asmDoIrq

.global irqDoubleFault
irqDoubleFault:
	pushl $-1
	jmp asmDoIrq

.global irqInvalidTSS
irqInvalidTSS:
	pushl $-1
	jmp asmDoIrq

.global irqSegNotPresent
irqSegNotPresent:
	pushl $-1
	jmp asmDoIrq

.global irqStackSegFault
irqStackSegFault:
	pushl $-1
	jmp asmDoIrq

.global irqGProtectFault
irqGProtectFault:
	pushl $0xd
	jmp asmDoIrq

.global irqPageFault
irqPageFault:
	pushl $-1
	jmp asmDoIrq

.global irqAlignCheck
irqAlignCheck:
	pushl $-1
	jmp asmDoIrq

.global irqSecException
irqSecException:
	pushl $-1
	jmp asmDoIrq

//【【【键盘中断的处理函数！！！】】】
//以下irqKeyboard对应的是irqHandle.c中的Keyboardandle函数的位置--->经历jmp一些列动作后，最后会到keyboardHandle函数中呢！
//每次按键后，内核都会调用irqKeyboard进行处理
.global irqKeyboard
irqKeyboard:
	pushl $0
	pushl $0x21		// TODO: 将irqKeyboard的中断向量号压入栈（0x21?在ppt47页中）---done
	jmp asmDoIrq



//【【【系统调用的中断处理函数！！！】】】
//以下irqSyscall在经过一系列调用后会到syscallPrint函数---是一个写显存相关的内容！
.global irqSyscall
irqSyscall:
	pushl $0 // push dummy error code
	pushl $0x80 // push interruption number into kernel stack
	jmp asmDoIrq

//.extern irqHandle //defined in irq_handle.c


//【【【是上面多个中断的最终集合的地方，最终会调用irqHandle函数进行分发！！！】】】
.global asmDoIrq
asmDoIrq:
	pushal // push process state into kernel stack
	pushl %esp //esp is treated as a parameter
	call irqHandle
	addl $4, %esp //esp is on top of kernel stack
	popal
	addl $4, %esp //interrupt number is on top of kernel stack
	addl $4, %esp //error code is on top of kernel stack
	iret
