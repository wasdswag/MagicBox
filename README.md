# K O R O B O K  1.4 / ex. MagicBox

update list:
- added a console launcher menu
- now the game is run only if the "cartridge" (NFC card) is inside and returns to the main launcher if you pull it out.
- added recorder mode so you can update NFC card without manual code/text file editing. all the records are stored in catalogue.tsv file (keyboard is required)
- recorder has 5 modes available:
  1) retropie rom: to launch games from emulationstation: it uses ranger console file-manager to navigate and select game files and generate required retropie runcommand.sh script
  2) webpage: to launch any website in chromium kiosk mode. requires qjoypad to use a gamepad instead of a mouse
  3) localhost webpage: this was added to run Unity WebGL builds (or any local web apps) from the Raspberry PI. requires an NGNIX server and automatically updates the server configuration to host individual local web pages. Also runs in kiosk mode
  4) custom command: any custom command you want
  5) erase mode: erase existing card command

every recorder mode has an image-adding option to display it on an e-paper screen after the launch:
you can select an image locally or download it by using this lib https://pypi.org/project/duckduckgo-search/ as a dependency
the duckduckgo library was modified to store downloaded images in a temp folder.
image selection uses FIM console image viewer, navigate [N] and [P] buttons, enter to select image [Q] to complete
after images were selected in order to show them on the e-paper display it needs to be dithered and resized. Thanks to this lib: https://github.com/miaourapide/image-dithering 

To write/override the last inserted nfc card by using a recorder you need to hold [R] key. It will  

My retro-game console rig based on Retropie / RPi 4 and NFC module for a cartridges imitation with used Moscow metro passcards

Full list of components:
- Raspberry Pi 4 / 4gb
- PN532 NFC scanner hat: https://www.waveshare.com/wiki/PN532_NFC_HAT 
- E-Paper 7-colors 4 inch display to show games cover art https://www.waveshare.com/wiki/4.01inch_e-Paper_Module_(F)
- USP hat (battery power supply) https://www.waveshare.com/wiki/UPS_HAT_(B)
- Lego for DIY enclosure  
- Expired / used subway passes cards as a cartridges


Thanks to @imdaftmike https://github.com/imdaftmike/NESPi for inspiration!
#
![alt text](https://raw.githubusercontent.com/wasdswag/MagicBox/main/MAGICBOX_ALL.jpg?raw=true)
