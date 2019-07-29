//gcc heap.c -o inode_heap -z noexecstack -fstack-protector-all -fPIE -pie -z now
#include<stdio.h>
#include<stdlib.h>
#include <unistd.h>
#include <sys/prctl.h>
#include <linux/filter.h>
#include <fcntl.h>

int *int_pt=0;
short int *short_pt=0;
int _bool=0;
int show_time=3;
void Sandbox_Loading()
{
	prctl(PR_SET_NO_NEW_PRIVS,1,0,0,0);
	struct sock_filter sfi[] = {
		{0x20,0x00,0x00,0x00000004},
		{0x15,0x00,0x05,0xc000003e},
		{0x20,0x00,0x00,0x00000000},
		{0x35,0x00,0x01,0x40000000},
		{0x15,0x00,0x02,0xffffffff},
		{0x15,0x01,0x00,0x0000003b},
		{0x06,0x00,0x00,0x7fff0000},
		{0x06,0x00,0x00,0x00000000},
	};
	struct sock_fprog sfp = {8,sfi};
	prctl(PR_SET_SECCOMP,2,&sfp);
}
void init()
{
	int fd = open("flag",O_RDONLY);
	if(fd==-1)
	{
		printf("no such file :flag\n");
		exit(-1);
	}
	dup2(fd,666);
	close(fd);
	setvbuf(stdout,0LL,2,0LL);
	setvbuf(stdin,0LL,1,0LL);
	setvbuf(stderr, 0LL, 2, 0LL);
	alarm(0x3c);
}
void menu()
{
	puts("------------------------");
	puts("1: add an inode ");
	puts("2: remove an inode ");
	puts("3: show an inode ");
	puts("4: leave message and exit. ");
	puts("------------------------");
	printf("which command?\n> ");
}
void bye_bye()
{
	char buf[100];
	puts("what do you want to say at last? ");
	scanf("%99s",buf);
	printf("your message :%s we have received...\n",buf);
	puts("have fun !");
	exit(0);
}
int get_atoi()
{
	char buf[16];
	read(0,buf,16);	
	return atoi(buf);
}
void show()
{
	if(show_time--)
	{
		printf("TYPE:\n1: int\n2: short int\n>");
		int choose=get_atoi();
		if (choose==1 && int_pt)
			printf("your int type inode number :%d\n",*int_pt);
		if (choose==2 && short_pt)
			printf("your short type inode number :%d\n",*short_pt);
	}
}
void allocate()
{
	printf("TYPE:\n1: int\n2: short int\n>");
	int choose=get_atoi();
	if (choose==1)
	{
		int_pt =(int *)malloc(0x20);
		if (!int_pt)
			exit(-1);
		_bool=1;
		printf("your inode number:");
		*int_pt=get_atoi();
		*(int *)((char *)int_pt+8)=*int_pt;
		puts("add success !");
	}
	if (choose==2)
	{
		short_pt =(short *)malloc(0x10);
		if (!short_pt)
			exit(-1);
		_bool=1;
		printf("your inode number:");
		*short_pt=get_atoi();
		*(short int *)((char *)short_pt+8)=*short_pt;
		puts("add success !");
	}
}
void delete()
{
	if(_bool)
	{
		printf("TYPE:\n1: int\n2: short int\n>");
		int choose=get_atoi();
		if (choose==1 && int_pt)
		{
			free(int_pt);
			_bool=0;
			puts("remove success !");
		}
		if (choose==2 && short_pt)
		{
			free(short_pt);
			_bool=0;
			puts("remove success !");
		}
	}
	else
		puts("invalid !");
}
int main(void)
{
	init();
	Sandbox_Loading();
	while(1)
	{
		int choose;
		menu();
		choose=get_atoi();
		switch(choose)
		{
			case 1:
				allocate();
				break;
			case 2:
				delete();
				break;
			case 3:
				show();
				break;
			case 4:
				bye_bye();
		}
	}
	return 0;
}
