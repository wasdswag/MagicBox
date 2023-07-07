import os
import time
from termcolor import colored
from simple_term_menu import TerminalMenu
import catalogue
import DuckDuckGoImages as ddg
import stringtools



def CompleteRecord():
	
	#os.system('clear')
	print('\n new card was successfully recorded! would you like to reboot to apply changes?\n')
	options = ["yes, reboot now", "no"]
	menu = TerminalMenu(options)
	choosenOption = menu.show()
	if  choosenOption == 0:
		os.system("sudo reboot")
	elif choosenOption == 1:
		print("return to korobok")
	else:
		print("no options picked, return to korobok")

	return 'recorded!'		
	

def ConvertImagesToEPaper(savedir, from_internet = False):

	os.system('clear')
	picturesArray = []
	with open('/home/pi/MagicBox/pic/selection.txt', 'r') as r:
		pictures = r.readlines()
		index = 0
		for picture in pictures:
			if picture.startswith('/home/pi/MagicBox/pic/temp/'):
				picture = picture.strip()

				print (f'\napplying dithering to: {picture} {savedir} {index} ... please wait')
				os.system(f'python3 /home/pi/MagicBox/run/image-dithering/dithering.py {picture} {savedir} {index}')
				picturesArray.append(f'{index}.gif')
				index = index + 1
	
	if from_internet:		
		os.system('rm -r /home/pi/MagicBox/pic/temp/*')	

	return picturesArray		


def PickupImages(savedir):

	pictures = []
	os.system('clear')

	print('\nwould you like to add some pictures to display on e-paper screen as a cover?')
	print('you can upload your own in', colored('/home/pi/MagicBox/pic', 'cyan'), 'directory or scrap them from ', colored('web\n', 'green'))

	options = ['choose from local storage', 'download from google', 'no']
	menu = TerminalMenu(options)
	choosenOption = menu.show()
	
	try:	
		if choosenOption == 0:
			print('\n\nuse [N] and [P] button to select [Enter to mark image] and [Q] to finish')
			time.sleep(2)
			os.system('fim /home/pi/MagicBox/pic  * > /home/pi/MagicBox/pic/selection.txt')
			pictures = ConvertImagesToEPaper(savedir, False)

		elif choosenOption == 1:
			print('\ntype a search query:')
			query = input("search: ")
			os.system(f'ddgs images -k "{query}" -m 40 -s off -d')
			os.system('clear')
			print('\n\nuse [N] and [P] button to select [Enter to mark image] and [Q] to finish')
			time.sleep(2)
			os.system('fim /home/pi/MagicBox/pic/temp/  * > /home/pi/MagicBox/pic/selection.txt')
			pictures = ConvertImagesToEPaper(savedir, True)

		elif choosenOption == 2:
			print("cancel")

		else:
			print("cancel")		


	except Exception as e:
		print(e)

	return pictures				

#PickupImages('testtest')


def MakePicturesDirectory(dir):
	os.system(f'mkdir /home/pi/MagicBox/pic/{dir}')
	os.system(f'sudo chmod 777 /home/pi/MagicBox/pic/{dir}')



def WebJoystickOptions():

	print(colored("\n\nDo you want to enable qjoypad setting to use joystick/gamepad as a mouse?", "cyan"))
	print("Default mouse-gamepad is set to 'dexp' (aka 'shanwan android gamepad').\nIf you want to use different one or remap exisiting controller please boot to desktop (startx), run QJOYPAD app and apply new scheme there\n\n")
	useJoystickAsMouse = ''

	options = ["yes, use default", "use different", "no"]
	menu = TerminalMenu(options)
	choosenOption = menu.show()
	if choosenOption == 0:
		useJoystickAsMouse = '& qjoypad "dexp"'
	elif choosenOption == 1:
		useJoystickAsMouse = input('enter map settings in format "& qjoypad <name>"')
	elif choosenOption == 3:
		useJoystickAsMouse = ""
	else: 
		useJoystickAsMouse = '& qjoypad "dexp"'

	return useJoystickAsMouse

		

def RecordRetroPieRom(key):

	try:
		print("What's the game title?")
		title = input('type the name here: ')
		time.sleep(0.2)
		os.system("ranger /home/pi/RetroPie/roms/ --choosefile /home/pi/MagicBox/run/currentpath ")
		time.sleep(0.1)

		with open('/home/pi/MagicBox/run/currentpath') as p:
			path = stringtools.formattobashready(p.read())
			
		system = path.split('/')
		system = system[5]

		shname = stringtools.RemoveSpaces(title)
		MakePicturesDirectory(shname)

		pictures = PickupImages(shname)


		with open(f'/home/pi/MagicBox/run/cards/{shname}.sh', 'w') as o:
			o.write(f'/opt/retropie/supplementary/runcommand/runcommand.sh 0 _SYS_ {system} {path}')

		time.sleep(0.1)
		os.system(f'sudo chmod 777 /home/pi/MagicBox/run/cards/{shname}.sh')
		catalogue.Write(key, f'/home/pi/MagicBox/run/cards/{shname}.sh', title, pictures)

		return CompleteRecord()

	except Exception as e:
		print(e)
		return 'error!'	




def RecordLocalHostWebPage(key):

	try:
		port = 0
		title = ""

		#load last saved ngnix port
		with open('/home/pi/MagicBox/run/localhost_last_port_index', 'r') as r:
			port = int(r.read()) + 1
			print(f'\npage will record at port: {port}')
			title = input('enter the name please: ')

		#choose website directory: 		
		print("select your index.html location: ")
		time.sleep(0.5)
		os.system("ranger /home/pi/wasdswag-kiosk/ --choosefile /home/pi/MagicBox/run/currentpath ")

		# configure ngnix server on new port 
		os.system('clear')
		print('\n configuring server...')
		os.system(f'sudo ufw allow {port}')

		with open('/home/pi/MagicBox/run/currentpath') as p:
			path = stringtools.formattobashready(p.read())
			folder = path.split('/')
			folder = folder[4]
			time.sleep(1)

		servconfig = "server { \n  listen " + str(port) + ";\n  server_name _;\n  root /home/pi/wasdswag-kiosk/" + folder + "; \n  index index.html;\n }"	

		with open(f'/etc/nginx/sites-available/{folder}', 'w') as s:
			s.write(servconfig)

		os.system(f"sudo ln -s /etc/nginx/sites-available/{folder} /etc/nginx/sites-enabled/")
		time.sleep(0.2)
		os.system("sudo systemctl restart nginx")
		print("Done!")
		
		# update port index
		with open('/home/pi/MagicBox/run/localhost_last_port_index', 'w') as w:
			w.write(str(port))


		shname = stringtools.RemoveSpaces(title)
		MakePicturesDirectory(shname)

		joystickoptions = WebJoystickOptions()
		pictures = PickupImages(shname)

		shellscript = f'!/bin/bash\nxset -dpms s off s noblank\nmatchbox-window-manager -use_titlebar no {joystickoptions} & \n/usr/bin/chromium-browser --noerrors --disable-session-crashed-bubble --disable-infobars --kiosk http://localhost:{port}'

		with open(f'/home/pi/bin/{shname}.sh', 'w') as o:
			o.write(shellscript)

		time.sleep(0.1)
		os.system(f'sudo chmod 777 /home/pi/bin/{shname}.sh')
		catalogue.Write(key, f'xinit /home/pi/bin/{shname}.sh', title, pictures)
		
		return CompleteRecord()	


	except Exception as e:
		print(e)
		return 'error!'	



def RecordWebPage(key):

	try:
		title = input('enter the name please: ')
		url = input('enter website url in format http://example.com  ')

		shname = stringtools.RemoveSpaces(title)
		MakePicturesDirectory(shname)

		joystickoptions = WebJoystickOptions()
		pictures = PickupImages(shname)


		shellscript = f'!/bin/bash\nxset -dpms s off s noblank\nmatchbox-window-manager -use_titlebar no {joystickoptions} & \n/usr/bin/chromium-browser --noerrors --disable-session-crashed-bubble --disable-infobars --kiosk {url}'

		with open(f'/home/pi/bin/{shname}.sh', 'w') as o:
			o.write(shellscript)

		time.sleep(0.1)
		os.system(f'sudo chmod 777 /home/pi/bin/{shname}.sh')
		catalogue.Write(key, f'xinit /home/pi/bin/{shname}.sh', title, pictures)
		return CompleteRecord()	

	except Exception as e:
		print(e)
		return 'error!'	



def RecordCustomCommand(key):

	try:
		title = input('enter the name please: ')
		command = input('enter custom command here: ')

		shname = stringtools.RemoveSpaces(title)
		MakePicturesDirectory(shname)

		pictures = PickupImages(shname)

		with open(f'/home/pi/bin/{shname}.sh', 'w') as o:
			o.write(f'!/bin/bash\n{command}')

		time.sleep(0.1)
		os.system(f'sudo chmod 777 /home/pi/bin/{shname}.sh')
		catalogue.Write(key, f'/home/pi/bin/{shname}.sh', title, pictures)
		return CompleteRecord()	

	except Exception as e:
		print(e)
		return 'error!'	



def EraseCard(key, name):

	result = ''
	try:
		if catalogue.IsExist(key):

			print(f'\n You are going to remove card: {name} from catalogue. Are you sure?\n')
			options = ["yes", "no"]
			
			menu = TerminalMenu(options)
			choosenOption = menu.show()
			
			if choosenOption == 0:
				catalogue.Erase(key)
				result = CompleteRecord()

			elif choosenOption == 1:
				print('aborted')
				result = 'canceled'	
			else: 
				result = 'canceled'

		else:
			print("this card is already empty")
			result = 'already cleared'

		return result

	except Exception as e:
		print(e)
		return 'error!'

		