#!/usr/bin/perl
#【TODO：把一个小于512字节的文件，制作成MBR】
#Lab1.1中为了把mbr.bin制作成一个真正的MBR（磁盘的（0，0，0））
#Lab1.3中cat bootloader/bootloader.bin app/app.bin > os.img
#cat命令把两个文件合成了一个os.img文件！



open(SIG, $ARGV[0]) || die "open $ARGV[0]: $!";

$n = sysread(SIG, $buf, 1000);#读取文件大小

if($n > 510){#判断文件大小是不是大于510字节，最后得剩下两个字节给魔数呢！
	print STDERR "ERROR: boot block too large: $n bytes (max 510)\n";
	exit 1;
}

print STDERR "OK: boot block is $n bytes (max 510)\n";

$buf .= "\0" x (510-$n);#把510-n字节的地方都放上\0
#OK: boot block is 310 bytes (max 510)---bootloader.bin的大小是310字节，被放到了0x8c00的位置
$buf .= "\x55\xAA";#MBR的魔数

open(SIG, ">$ARGV[0]") || die "open >$ARGV[0]: $!";
print SIG $buf;
close SIG;
