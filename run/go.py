#!/usr/bin/python
# -*- coding:utf-8 -*-
import time
import threading
import os
import RPi.GPIO as GPIO
from pn532 import *

# directories
random_person = '/home/pi/bin/random_person.sh'

import subprocess
from subprocess import PIPE, Popen

import catalogue
import battery
import screen

import random
import stringtools



procnames = [      "retroarch", "ags", "uae4all2", "uae4arm", "capricerpi", "linapple", "hatari", "stella",
                   "atari800", "xroar", "vice", "daphne", "reicast", "redream", "pifba", "osmose", "gpsp", "jzintv",
                   "basiliskll", "mame", "advmame", "dgen", "openmsx", "mupen64plus", "gngeo", "dosbox", "ppsspp",
                   "simcoupe", "scummvm", "snes9x", "pisnes", "frotz", "fbzx", "fuse", "gemrb", "cgenesis", "zdoom",
                   "eduke32", "lincity", "love", "alephone", "micropolis", "openbor", "openttd", "opentyrian",
                   "cannonball", "tyrquake", "ioquake3", "residualvm", "xrick", "sdlpop", "uqm", "stratagus",
                   "wolf4sdl", "solarus", "psx", "emulationstation", "emulationstatio", "xinit", "lxde", "LXDE", "chromium-browser", 
                   "chromium", "chromium-browser-v7", "atari2600", "atari5200", "atari7800", "atarijaguar", 
                   # "atarilynx", "atarist", "c64", "channelf", "coleco", "crvision", "dreamcast", "fba", "fds", "gamegear", 
                   # "gb", "gba", "gbc", "gc", "genesis", "home", "j2me", "kodi", "macintosh", "mame-libretro", 
                   # "mame-mame4all", "mastersystem", "megadrive", "moto", "movies", "n64", "nds", "neogeo", "nes", "ngp", 
                   # "ngpc", "oric", "pc88", "pc98", "pcengine", "pcfx", "pico8", "pokemini", "psp",
                   # "residualvm", "saturn", "scummvm", "sega32x", "segacd", "sg-1000", "snes", "steam", "ti99", "tic80", "trs-80", 
                   # "tvshows", "vectrex", "x1", "x68000", "zx81", "zxspectrum"

                     ]


status = ''
lastStatus = ''


def process_is_running(name):
    for line in os.popen("ps ax | grep " + name + " | grep -v grep"):
        if len(line) > 5: return True


def kill_process(name):
    for line in os.popen("ps ax | grep " + name + " | grep -v grep"):
        fields = line.split()
        pid = fields[0]
        os.system("sudo kill -15 " + pid)


def Monitor():
    
    Monitor.record = None
    Monitor.state = ''
    Monitor.isUpdating = False

    previous_state = ''
    timer = 180
    timeout = 180


    while True:

        if Monitor.isUpdating == False:

            is_standby = timer > timeout and Monitor.record is None

            if Monitor.state != previous_state or is_standby:

                Monitor.isUpdating = True
                previous_state = Monitor.state
                UpdatePaperScreen(Monitor.record);
                timer = 0
                
            timer = timer + 2
            time.sleep(2) 

    

def UpdateStatus(message="", key="no", card=None):

    global lastStatus
    if(message != lastStatus):
        print("new status!")
        with open('/home/pi/MagicBox/run/status.txt', 'w') as s:
            s.write(message)
            lastStatus = message;
        if(key != "no"):
            with open('/home/pi/MagicBox/run/key.txt', 'w') as k:
                k.write(key)

        Monitor.record = card
        Monitor.state = message        



def UpdatePaperScreen(record=None):

    if record is not None:
        if len(record[2]) > 0:
            paper_image = stringtools.RemoveSpaces(record[1]) + "/" + random.choice(record[2])
            screen.EPaper.Update(paper_image)
        else:
            os.system(random_person) 
            screen.EPaper.Update()

    else:
        os.system(random_person)
        screen.EPaper.Update()

    Monitor.isUpdating = False    
            


def NFCRead():

    application_is_running = False
    current_record = None
    app =''
    readyStatus = ["please, insert a cartridge!", "your ticket please", "ready to play!"]   

    try:

        #scanner setup:
        pn532 = PN532_I2C(debug=False, reset=20, req=16)
        ic, ver, rev, support = pn532.get_firmware_version()
        print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))
        pn532.SAM_configuration()
        print('Waiting for RFID/NFC card...')
        isCleared = False;

        while True:

            uid = pn532.read_passive_target(timeout=1)

            # DETECT NO CARD
            if uid is None and current_record is not None:

                    current_record = None
                    os.system('killall chromium-browser-v7')
                
                    if application_is_running: 
                        application_is_running = False
                        app.kill()

                    for p in procnames: kill_process(p)

                    UpdateStatus(random.choice(readyStatus), "no") 
                    continue



            uid = f'{uid}' # parse byte to string to avoid incorrect encoding / decodinig issues 

            # DETECT RECORDED CARD
            if uid in catalogue.cards:

                if current_record != catalogue.cards[uid]:
                   current_record = catalogue.cards[uid]

                   for p in procnames: kill_process(p)

                   while  process_is_running("emulationstation"):
                        kill_process("emulationstation")
                        time.sleep(1)

                   app = subprocess.Popen(catalogue.cards[uid][0], stdout=subprocess.PIPE, shell=True)
                   application_is_running = True

                   UpdateStatus(catalogue.cards[uid][1], uid, catalogue.cards[uid])


            # DETECT EMPTY CARD:       
            elif uid != 'None':

                print(uid)
                current_record = 'empty'
                application_is_running = False
                UpdateStatus("empty card: ", uid)


        time.sleep(1)    


    except Exception as e:
        print(e)
        os.system('/opt/retropie/configs/all/autostart.sh')
    except KeyboardInterrupt:    
        logging.info("ctrl + c:")
        exit()
    

monitor = threading.Thread(target=Monitor)
monitor.start()


if __name__=='__main__':

    print('start')
    NFCRead()
   