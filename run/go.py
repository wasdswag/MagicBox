#!/usr/bin/python
# -*- coding:utf-8 -*-
import time
import threading
import os
import RPi.GPIO as GPIO
from pn532 import *

# a path to my processing sketch which generate random graphic for screen in standby mode
# comment line 160 to prevent errors :)
# runSketch = '/home/pi/bin/random_person.sh'

import subprocess
from subprocess import PIPE, Popen

import catalogue
import battery
import screen

import random


procnames = [      "retroarch", "ags", "uae4all2", "uae4arm", "capricerpi", "linapple", "hatari", "stella",
                   "atari800", "xroar", "vice", "daphne", "reicast", "redream", "pifba", "osmose", "gpsp", "jzintv",
                   "basiliskll", "mame", "advmame", "dgen", "openmsx", "mupen64plus", "gngeo", "dosbox", "ppsspp",
                   "simcoupe", "scummvm", "snes9x", "pisnes", "frotz", "fbzx", "fuse", "gemrb", "cgenesis", "zdoom",
                   "eduke32", "lincity", "love", "alephone", "micropolis", "openbor", "openttd", "opentyrian",
                   "cannonball", "tyrquake", "ioquake3", "residualvm", "xrick", "sdlpop", "uqm", "stratagus",
                   "wolf4sdl", "solarus", "psx", "emulationstation", "emulationstatio"      ]



def process_is_running(name):
    for line in os.popen("ps ax | grep " + name + " | grep -v grep"):
        if len(line) > 5: return True


def kill_process(name):
    for line in os.popen("ps ax | grep " + name + " | grep -v grep"):
        fields = line.split()
        pid = fields[0]
        os.system("kill -15 " + pid)



def Monitor():
    
    Monitor.is_gameImage = False
    try:
        while True:
            state = battery.getInfo()
            if NFCRead.card and Monitor.is_gameImage == False: 
                screen.EPaper.Update(NFCRead.cardImage)
                Monitor.is_gameImage = True

            
            if Monitor.is_gameImage == True and process_is_running('emulationstation'):
                print('EMPTY')
                NFCRead.card = False
                NFCRead.cardTitle = ''
                Monitor.is_gameImage = False

            time.sleep(10);



    except Exception as e:
        print(e)
    except KeyboardInterrupt:    
        logging.info("ctrl + c:")
        exit()
    



def NFCRead():

    NFCRead.card = False
    NFCRead.cardTitle = ''
    NFCRead.cardImage = ''

    try:
        #pn532 = PN532_SPI(debug=False, reset=20, cs=4)
        pn532 = PN532_I2C(debug=False, reset=20, req=16)
        #pn532 = PN532_UART(debug=False, reset=20)

        ic, ver, rev, support = pn532.get_firmware_version()
        print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))

        # Configure PN532 to communicate with MiFare cards
        pn532.SAM_configuration()


        print('Waiting for RFID/NFC card...')
        while True:
            # Check if a card is available to read
            uid = pn532.read_passive_target(timeout=0.5)
            print('.', end="")
            # Try again if no card is available.
            if uid is None:
                continue

            if uid in catalogue.cards:
                print(catalogue.cards[uid][1])
                NFCRead.card = True
                if NFCRead.cardTitle != catalogue.cards[uid][1]:
                   NFCRead.cardTitle = catalogue.cards[uid][1]                   
                   NFCRead.cardImage = random.choice(catalogue.cards[uid][2]) 
                   print(catalogue.cards[uid][0])
                   Monitor.is_gameImage = False

                   
                   for p in procnames: kill_process(p)

                   while  process_is_running("emulationstation") or process_is_running("emulationstatio"):
                        
                        kill_process("emulationstation")
                        kill_process("emulationstatio")
                        print('NOW LOADING: ' + catalogue.cards[uid][1])
                        time.sleep(2)
                        
                        
                   subprocess.call(catalogue.cards[uid][0], shell=True)


            else:
                print(uid)
                if uid == catalogue.resetToDefaultKey:
                    NFCRead.card = False
                    NFCRead.cardImage = ''


    except Exception as e:
        print(e)
    except KeyboardInterrupt:    
        logging.info("ctrl + c:")
        exit()
    
    finally:
        GPIO.cleanup()



nfc = threading.Thread(target=NFCRead)
monitor = threading.Thread(target=Monitor)

nfc.start()
monitor.start()




if __name__=='__main__':
    
    while True:
        
        if NFCRead.card == False: 
             screen.EPaper.Update()
             time.sleep(180)
             #os.system(runSketch)
        else:
             time.sleep(10)    
        

