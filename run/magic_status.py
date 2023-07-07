import os
import time
import random
from termcolor import colored
import battery
import keyboard

import threading
from simple_term_menu import TerminalMenu

import recorder



#"Delta Corps Priest 1"
favfonts = [
"THIS", "Flower Power", "Jacky", "Crazy"
]


def FakeDownloadStatus(status =''):

	char =''
	dStatusline = '\t0%\tLOADING...   '
	line =''
	linesCount = 0;

	time.sleep(3)
	while(linesCount < 100):

		for x in range(16):
			if (random.random() < 0.5): char = "\\" 
			else: char = '/'
			line += char;
		
		perc = linesCount+1	
		dStatusline = f'\t{perc}%\tLOADING...   '
		#print(f'{dStatusline}{line}')
		os.system(f'toilet -f "Banner"  --termwidth {dStatusline}{line}')
		time.sleep(0.0166)	

		line = ''
		linesCount +=1

	linesCount = 0;
	os.system('clear')



def DrawStatus(isApp=False, status="ready to play", cardname=""):

	font = random.choice(favfonts)
	rnd = random.random()

	os.system('clear')

	print('\n\n\n\n\n\n\n\n')
	os.system(f'toilet -f "JS Stick Letters" --gay --termwidth {status}')

	


	print('\n\n\n\nkorobok: ver 1.4 | premium 4k 60fps experience')
	print('hello@wasdswag.com | https://github.com/wasdswag/MagicBox')
	cpuInfo = battery.getInfo();

	print("wasdswag 2023 ", colored(cpuInfo, "green"))
	print('_____________________________________________________')



	if(isApp == True): 
		FakeDownloadStatus(status)
		UpdateStatus.isRunningApp = True;

	if(cardname != "" and isApp == False):
		tabs = "\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t"	
		print(f'\n\nHOLD', 
			 colored('[R]', 'magenta'), f'key to write/overwrite \nlast inserted card is:', colored(f'{cardname}', 'cyan'), 
			 f'\nkeyboard is required!' )




def UpdateStatus():

	previousStatus = ''
	status = ''
	style = ''
	loopCounts = 0

	readyStatus = ["please, insert a cartridge!", "your ticket please", "ready to play!", "wait a second..."] 
	emptyStatus = "empty card: "
	isApplication = False;

	timer = 0;
	UpdateStatus.isRunningApp = False;
	UpdateStatus.isRecording = False;
	UpdateStatus.Title = '' 
	UpdateStatus.TimeOut = 120


	try:

		with open('/home/pi/MagicBox/run/status.txt', 'w') as w:
			w.write("wait a second...")
		DrawStatus(False, "K O R O B O K")
		time.sleep(4)
	


		while True:

			with open('/home/pi/MagicBox/run/status.txt') as s:
				status = s.read()
				if (status in readyStatus or status == emptyStatus): 
					isApplication = False
					UpdateStatus.isRunningApp = False;	

				else: isApplication = True

				if(status == emptyStatus): UpdateStatus.Title = "clear card"
				if(isApplication): UpdateStatus.Title = status


			if(UpdateStatus.isRecording == False and (previousStatus != status or timer >= UpdateStatus.TimeOut)) :

				DrawStatus(isApplication, status, UpdateStatus.Title)
				timer = 0


			time.sleep(1)
			previousStatus = status
			timer = timer + 1
			

	except Exception as e:
		print(e)
	except KeyboardInterrupt:    
		logging.info("ctrl + c:")
		exit()



update = threading.Thread(target=UpdateStatus)
update.start()
time.sleep(10)
DrawStatus(False, "ready to play")



def ExitWith(status):
	UpdateStatus.isRecording = False
	DrawStatus(False, status)


if __name__=='__main__':

	path = ''
	system = ''
	recordMenu = False

	try:
		while True:
			if(UpdateStatus.isRunningApp): continue 
			if(keyboard.is_pressed('r')):
				while(keyboard.is_pressed('r')):
					time.sleep(0.2)
					UpdateStatus.isRecording = True
					print(colored("//  record mode", "light_red"), " please release",  colored(" [R] ", "yellow"), "button")

				os.system('clear')
				os.system(f'toilet -f "Banner"  --termwidth create new record on {UpdateStatus.Title}') 
				print("\n what kind of record do you want?\n\n")
				options = ["retropie rom", "localhost webpage", "webpage", "custom command", "erase card", "cancel"]
				menu = TerminalMenu(options)
				choosenOption = menu.show()

				cardKey = ""
				with open('/home/pi/MagicBox/run/key.txt') as k:
					cardKey = k.read()

				status = ''	

				# RECORD FROM RETROPIE ROMS FOLDER 
				if choosenOption == 0:
					status = recorder.RecordRetroPieRom(cardKey)
					
				# RECORD YOUR OWN LOCALHOST WEB PAGES (eg UNITY WEBGL games etc) will open in kiosk mode	
				elif choosenOption == 1:
					status = recorder.RecordLocalHostWebPage(cardKey)

				# RECORD ANY WEBPAGE / kiosk mode 	
				elif choosenOption == 2:
					status = recorder.RecordWebPage(cardKey)

				# RECORD CUSTOM COMMAND	
				elif choosenOption == 3:
					status = recorder.RecordCustomCommand(cardKey)

				# ERASE CARD	
				elif choosenOption == 4:
					status = recorder.EraseCard(cardKey, UpdateStatus.Title)

				# EXIT		
				elif choosenOption == 5:
					print('exit')
					status = 'canceled'

				else:
					print('no option picked')
					status = canceled


				ExitWith(status)		

			time.sleep(3)		
							


	except Exception as e:
		print(e)

	except KeyboardInterrupt:
		logging.info("ctrl + c:")
		exit()

