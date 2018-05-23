import paramiko, time, argparse, getpass, os, sys, csv
from options.settings import *
from report.checks import *

def parseArgs():
	# Parse arguments and display help
	parser = argparse.ArgumentParser(description='{}'.format(APP_NAME))
	parser.add_argument('-i', help='ip address', default='', required=True)
	parser.add_argument('-u', help='Username', default='')
	parser.add_argument('-p', help='Password - Use with caution, you type this in plain text!', default='')
	parser.add_argument('-e', help='Enable console usage: 1 = enabled, 0 = disabled', default='0')
	args = parser.parse_args()
	return args

def connect(device, user, passw, encon):
	# Connect to device via SSH.
	global ssh
	global chan

	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(device, username=user, password=passw)
	chan = ssh.invoke_shell()
	#logging into enable console
	if encon == 1:
		chan.send('enable\n')
		print('[+] sent - enable')
		chan.send('{}\n'.format(passw))
	elif encon == 0:
		pass
	else:
		pass

def disconnect():
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
	#print('[+] {}'.format(command))

	return resp

def getLog(command):
	# get Log - terminal length 0
	exeCommand("terminal length 0").decode()
	response = exeCommand(command).decode()
	return response

def mkdir_p(path):
	if not os.path.exists(path):
		os.makedirs(path)
	else:
		pass
outputDir = 'Output'
def saveLog(msg, svr_name, task, deviceIP):
	mkdir_p(outputDir + "/" + svr_name)
	file = open('output/{}/{}({}) - {}.txt'.format(svr_name, svr_name, deviceIP, task) , 'w')
	file.write(msg)
	file.close()
	print('[+] Saving log file: {}({}) - {}.txt - Done'.format(svr_name, deviceIP, task))

def saveReport(msg, reportName):
	mkdir_p(outputDir)
	file = open('output/{}.txt'.format(reportName) , 'a+')
	file.write('{}\n\n\n'.format(msg))
	file.close()
	print('[+] Saving Report file: {}.txt'.format(reportName))

def saveReportCSV(msg, reportName):
	mkdir_p(outputDir)
	with open('output/{}.csv'.format(reportName) , 'a+', newline='') as csvfile:
		writer = csv.writer(csvfile, quoting=csv.QUOTE_NONE, escapechar='\\')
		splitmgs = msg.splitlines()
		outp = []
		for line in splitmgs:
			line = line.replace("[+] - ", "")
			line = line.replace("[!] ", "")
			if line == '' or line == ' ' or line == 'Missing Commands' or line == 'Alert Commands':
				pass
			else:
				outp.append('{}'.format(line))
		writer.writerows([outp])
	print('[+] Saving Report file: {}.csv'.format(reportName))

def hostRes(device, encon):
	try:
		print('[+] Resolving Cisco Hostname...')
		hname = exeCommand('show run | inc hostname').decode()
		hname = hname.split('\n')
		if encon == 0:
			hname = hname[2].split('hostname ')
		elif encon == 1:
			print(str(hname))
			hname = hname[4].split('hostname ')
		hname = hname[1]
		hostname = str(hname).replace('\r', '')
		print('[+] Resolved hostname: {} - {}'.format(hostname, device))
		return hostname
	except Exception as e:
		hostname = device
		print('[+] Failed to resolved hostname...')
		print('[+] Using Device IP for output: {}'.format(hostname))
		print('\n\n[!] {} - please investigate\n\n'.format(e))
		return hostname


def main():
	args = parseArgs()
	clean = '{}'.format(args.i)
	if args.u == '':
		USERNAME = input('[+] Username: ')
	else:
		USERNAME = args.u
	if args.p == '':
		PASSWORD = getpass.getpass(prompt='[+] Password: ')
		print('')
	else:
		PASSWORD = args.p
	if args.e == '0':
		ENABLE_CONSOLE = 0
	elif args.e == '1':
		ENABLE_CONSOLE = 1

	try:
		connect(clean, USERNAME, PASSWORD, ENABLE_CONSOLE)
	except Exception as e:
		if 'Unable to connect to port 22' in str(e):
			print('\n\n[!] {} - please investigate\n\n'.format(e))		#contin write to file = unable to connect
			#saveReport('{}'.format('[!] {} - please investigate'.format(e)), 'Unable to connect')
			saveReportCSV('{},{}'.format(clean, '[!] {} - please investigate'.format(e)), 'Connection Error')
			sys.exit(0)
		else:
			print('\n\n[!] {} - please investigate\n\n'.format(e))		#contin write to file = unable to connect
			#saveReport('{}'.format('[!] {} - please investigate'.format(e)), 'Unable to connect')
			saveReportCSV('{},{}'.format(clean, '[!] {} - please investigate'.format(e)), 'Connection Error')
			sys.exit(0)
	# Unable to connect to port 22

	hostname = hostRes(clean, ENABLE_CONSOLE)
	print('\n\n{}\n'.format(HEADDER.format('Config Checks')))
	#start checks on runnin config
	run_conf = getLog('{}'.format('sh run'))
	run_conf2 = run_conf.split('\r\n')
	block = False
	prev = ''

	# single line comms - missing
	repeat = []
	newlist = []
	foundalert = []

	# single line commands
	slcom = []

	# display single line Commands
	dsingle = []

	# display block Commands
	dblock = []

	#interfaces
	intface = []

	# single line Commands
	for item in run_conf2:
		for alert in ALERT_COMS:
			if str(alert) in item:
				if item[:3] == 'no ':
					print('[!] {}'.format(item))
					slcom.append('[!] {}'.format(item))
				else:
					print('[-] {}'.format(item))
					slcom.append('[-] {}'.format(item))
			if str(alert) not in run_conf2:
				if str(alert) not in repeat:
					repeat.append('[!] {}'.format(alert))
		for alertor in ALERT_COMS_OR:
			if str(alertor[0]) in item or str(alertor[1]) in item:
				if item[:3] == 'no ':
					print('[!] {}'.format(item))
					slcom.append('[!] {}'.format(item))
				else:
					print('[-] {}'.format(item))
					slcom.append('[-] {}'.format(item))
			if str(alertor[0]) not in run_conf2 or str(alertor[1]) not in run_conf2:
				if str(alertor[0]) not in repeat or str(alertor[1]) not in repeat:
					repeat.append('[!] {}'.format(alert))
	for i in repeat:
		if i not in newlist:
			newlist.append(i)

	# Single line commands that start with 'no '
	for item in run_conf2:
		for alert in ALERT_COMS_NO:
			if str(alert) in item:
				if item[:3] == 'no ':
					print('[-] {}'.format(item))
					slcom.append('[-] {}'.format(item))
				else:
					print('[!] {}'.format(item))
					slcom.append('[!] {}'.format(item))
					repeat.append('[!] {}'.format(item))
			if str(alert) not in run_conf2:
				if str(alert) not in repeat:
					repeat.append('[!] {}'.format(alert))
	for i in repeat:
		if i not in newlist:
			newlist.append(i)

	print('\n\n\n')

	for item in run_conf2:
		for found in ALERT_FOUND_COMS:
			if str(found) in item:
				print('[!] {}'.format(item))
				foundalert.append('[!] {}'.format(item))

	# Display Single Line Commands
	for item in run_conf2:
		for disp in DISPLAY_COMS:
			if str(disp) in item:
				print('[=] {}'.format(item))
				dsingle.append('[=] {}'.format(item))

	print('\n\n\n')
	for item in run_conf2:
		for disp in DIS_BLOCK_COMS:
			if disp in item or prev == disp:
				prev = disp
				if block:
					if item[:1] != '!':
						print('[**] {}'.format(item))
						dblock.append('[**] {}'.format(item))
					else:
						block = False
						prev = ''
				else:
					print('[**] {}'.format(item))
					dblock.append('[**] {}'.format(item))
					block = True


	# show missing config
	print('\n\n\n[+] [{}]\n'.format('Missing Commands'))
	for rep in newlist:
		print(rep)
	for ea in foundalert:
		print(ea)


		#start checks on interfaces
		# down                  down
	if 1 == 2:
		print('\n\n{}\n'.format(HEADDER.format('Interface Checks')))
		ip_int = getLog('{}'.format('sh ip int brief'))
		ip_int2 = ip_int.split('\r\n')
		for item in ip_int2:
			if 'down                  down' in item:
				print('[!] {} - Interface not shutdown!'.format(item.split()[0]))
				intface.append('[!] {} - Interface not shutdown!'.format(item.split()[0]))
		print('\n\n')

	#join main output .format('\n'.join(slcom), '\n'.join(newlist),  '\n'.join(dsingle), '\n'.join(dblock))

	
	saveLog('{}\n\n\n{}\n\n\n{}\n\n\n{}'.format('\n'.join(slcom), '\n'.join(newlist),  '\n'.join(dsingle), '\n'.join(dblock)), hostname, "Main Log - Output", clean)
	saveLog('[+] - {}\n[+] - Missing Commands\n{}\n\n[+] - Alert Commands\n{}'.format(clean, '\n'.join(newlist),  '\n'.join(foundalert)), hostname, "Missing Commands & Alert", clean)
	saveReportCSV('[+] - {}({})\n[+] - Missing Commands\n{}\n\n[+] - Alert Commands\n{}'.format(hostname, clean,'\n'.join(newlist),  '\n'.join(foundalert)), 'Main Report')
	saveLog(getLog("sh run"), hostname, "sh run", clean)
	saveLog(getLog("sh vstack config"), hostname, "sh vstack config", clean)
	
	#saveReport('[+] - {}({})\n[+] - Missing Commands\n{}\n\n[+] - Alert Commands\n{}'.format(hostname, clean,'\n'.join(newlist),  '\n'.join(foundalert)), 'Main Report')
	#saveLog('\n'.join(intface), hostname, "Down Interfaces", clean)
	#saveLog(getLog("sh ip int brief"), hostname, "sh ip int brief", clean)

	disconnect()

if __name__ == '__main__':
	main()
