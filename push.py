import argparse, getpass
from lib.readfiles import *
from options.settings import *

# TO DO:
#	ADD Error checking for listing a __GCOM but no __GLOBAL__ defined
#	ADD Some form of inteligence to ask if command is in running conf
#		then compair existing command in config to sending command

def parseArgs():
	# Parse arguments and display help
	parser = argparse.ArgumentParser(description='{}'.format(APP_NAME))
	parser.add_argument('-c', help='Config file location', default='')
	parser.add_argument('-u', help='Username', default='')
	parser.add_argument('-p', help='Password - Use with caution, you type this in plain text!', default='')
	parser.add_argument('-e', help='Enable console usage: 1 = enabled, 0 = disabled', default=0)
	args = parser.parse_args()
	return args

def main():
	print('\n{}\n'.format(HEADDER.format(APP_NAME)))
	args = parseArgs()
	if args.c != '':
		FILE_NAME = args.c
	if args.e != 0:
		ENABLE_CONSOLE = args.e
	if args.u == '':
		USERNAME = input('[+] Username: ')
	else:
		USERNAME = args.u
	if args.p == '':
		PASSWORD = getpass.getpass(prompt='[+] Password: ')
		print('')
	else:
		PASSWORD = args.p
	readconf()
	print('\n{}\n\n'.format(HEADDER.format('Done :)')))


if __name__ == '__main__':
	main()
