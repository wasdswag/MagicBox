import os
import sys
import time



libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
if os.path.exists(libdir): sys.path.append(libdir)
if os.path.exists(picdir): sys.path.append(picdir)


import logging
from waveshare_epd import epd4in01f
from PIL import Image,ImageDraw,ImageFont

rp_dir = '/home/pi/sketchbook/RandomPersonRetropie/RANDOM_DUDE.gif'
import battery




class EPaper:

    font24 = 0
    font18 = 0
    font30 = 0

    def Init():

        logging.basicConfig(level=logging.DEBUG)

        try:
            #logging.info("init screen")
            epd = epd4in01f.EPD()

            epd.init()
            epd.Clear()
            return epd


        except IOError as e:
            #logging.info(e)
            epd4in01f.epdconfig.module_exit()
            time.sleep(2)
            #EPaper.Init()
            exit()

        except KeyboardInterrupt:    
            #logging.info("ctrl + c:")
            epd4in01f.epdconfig.module_exit()
            exit()


    def Update(card_image = 'default'):

        try:

            stateInfo = battery.getInfo() 

            epd.Clear()
            font30 = ImageFont.truetype(picdir + '/Helvetica.ttc', 40)
            Himage = 'img'
            hasGameCard = card_image != 'default'
             
            if hasGameCard == True:
                Himage = Image.open(picdir + '/' + card_image)
            else: 
                Himage = Image.open(rp_dir)
                Himage = Himage.resize((epd.height, epd.width))
        
             
            draw = ImageDraw.Draw(Himage)
            draw.text((22, 580), stateInfo, font = font30, fill = 255)
            angle = 180

            if hasGameCard == True: angle = 0  
            img = Himage.rotate(angle)
            epd.display(epd.getbuffer(img))
                

        except IOError as e:
            #logging.info(e)
            epd4in01f.epdconfig.module_exit()
            time.sleep(2)
            EPaper.Init()
            exit()

        except KeyboardInterrupt:    
            #logging.info("ctrl + c:")
            epd4in01f.epdconfig.module_exit()
            exit()


epd = EPaper.Init()



