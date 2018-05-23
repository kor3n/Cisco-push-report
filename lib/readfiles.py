from lib.connections import *
from options.settings import *

def globalcoms(command):
	if command == '__GLOBAL__':
		pass
	elif command == '__ENDGLOBAL__':
		pass
	else:
		GLOBAL_COMMANDS.append(command)

def readconf():
	with open(FILE_NAME, 'r') as pushsettings:
		push = pushsettings.readlines()
		gbl = False
		for row in push:
			clean = row.strip('\n')
			tab_count = len(clean) - len(clean.lstrip())
			if clean == '__GLOBAL__':
				gbl = True
			if clean == '__ENDGLOBAL__':
				gbl = False
			if gbl == True:
				globalcoms(clean.lstrip())


			if tab_count == 0 and clean != '__ENDGLOBAL__' and gbl == False:
				disconnect()
				print('Main device: {}'.format(clean)) # perform connection
				connect(clean, USERNAME, PASSWORD, ENABLE_CONSOLE)
			if gbl == False:
				if tab_count == 1:
					if '__GCOM' in clean.lstrip():
						gnum = clean.lstrip().split()
						for num in gnum:
							if num == '__GCOM':
								pass
							else:
								exeCommand('{}'.format(GLOBAL_COMMANDS[int(num) - 1]))
						# exeCommand(str(GLOBAL_COMMANDS[int(gnum[1]) - 1])).decode()
					else:
						exeCommand('{}'.format(clean.lstrip()))
	disconnect()
