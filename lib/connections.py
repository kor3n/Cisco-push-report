import paramiko, time
from options.settings import *
from lib.readfiles import *

def connect(device, user, passw, encon):
	# Connect to device via SSH.
	connect.hasconnected = True
	global ssh
	global chan

	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(device, username=user, password=passw)
	chan = ssh.invoke_shell()
	#logging into enable console
	if encon == 1:
		chan.send('enable\n')
		chan.send('%s\n' % passw)
	elif encon == 0:
		pass
	else:
		pass

connect.hasconnected = False

def disconnect():
	if connect.hasconnected: # Disconnect from a device.
		chan.close()
		ssh.close()
		print('[+] Disconnected :)\n')

def exeCommand(command):
	# Execute command on a device.
	chan.send('%s\n' % command)
	time.sleep(SLEEP_TIME)
	resp = chan.recv(RECV_SIZE)
	if 'Invalid input detected at' in resp.decode():
		print('[+] Error with command: '.format(str(resp.decode())))
		return resp
	print('[+] {}'.format(command))

	return resp
