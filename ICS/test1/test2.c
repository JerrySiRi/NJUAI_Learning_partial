#include<stdio.h>
#include<stdlib.h>

  int main()
  {
	int n;
	char str[20]="0x88";
  	sscanf(str,"%x",&n);
	printf("%d",n);
  }
