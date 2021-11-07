
sh = '/home/pi/MagicBox/run/cards/'
    
# GAME CARDS
lsdDreamEmulator = 	(sh + 'lsd.sh &', 'LSD Dream Emulator', ['lsd_1.gif', 'lsd_2.gif','lsd_2.gif','lsd_3.gif','lsd_4.gif','lsd_5.gif','lsd_6.gif','lsd_7.gif','lsd_8.gif','lsd_9.gif', 'lsd_10.gif','lsd_11.gif','lsd_12.gif','lsd_13.gif','lsd_14.gif','lsd_15.gif','lsd_16.gif',])
crazyTaxi = 		(sh + 'crazyTaxi.sh &', 'Crazy Taxi', ['crazy_taxi.gif'])
tekken3 =			(sh + 'tekken3.sh &', 'Tekken3', ['tekken_3.gif'])
mario_paint =		(sh + 'marioPaint.sh &', 'Mario Paint', ['mario_paint.gif'])
MetalGearSolid =	(sh + 'metalGearSolid.sh &', 'Metal Gear Solid', ['metalGearSolid_1.gif', 'metalGearSolid_2.gif'])
sonic =				(sh + 'sonic.sh &', 'Sonic Adventure', ['sonic2.gif'])
lifespan =			(sh + 'lifespan.sh &', 'LIFESPAN by John ONeill 83', ['lifespan.gif'])
shenmue =			(sh + 'shenmue.sh &', 'SHENMUE', ['shenmue.gif'])


# SYSTEM CARDS
reboot = 			('sudo reboot', 'zero', 'mario.bmp');
halt = 				('sudo shutdown -h now', 'halt', 'mario.bmp');


cards = 	{   b'4\xc1\xf7\xa9W\x8b\xa7' 		: 	lsdDreamEmulator,  
				b'49\x83i2o\x86' 				: 	crazyTaxi, 
				b'4\xe9\x079;k\xa6' 			: 	tekken3, 
				b'4\x9e\x8e\x99\xafC\xc6' 		: 	mario_paint,  
                b'49\x83\xa1$\xf4\x86' 			: 	MetalGearSolid, 
                b'\x04Q,\x8a\xdeT\x80' 			: 	sonic,  
                b'4;a\xb9\x90\xdc\x96' 			: 	lifespan, 
                b'49\x83iW\x86\x86' 			: 	shenmue,
                b'4\xc5\xdd\x99\xa4\x97\xa6' 	:	reboot, 
                b'4\xd1\x93\xc9b)\xa6' 			: 	halt  	}



resetToDefaultKey = b'49\x83\xa1#"\x86'
