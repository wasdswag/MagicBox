
def Read():

        with open('/home/pi/MagicBox/run/catalogue.tsv', 'r') as r:
                table = r.readlines()

                for line in table:
                        linevalues = line.split('\t')
                        if len(linevalues) > 2:
                                key = linevalues[0]
                                command = linevalues[1]
                                name = linevalues[2]
                                images = linevalues[3].split('\n')
                                pictures = images[0].split(',')
                                                                
                                data = (command, name, pictures)
                                cards.update({key:data})
        #print(cards)                
        return cards

def Erase(key =""):

        print ("update tsv!")
        with open('/home/pi/MagicBox/run/catalogue.tsv', 'r+') as w:

                lines = w.readlines()
                for l in lines:
                        if len(l) < 3:
                                lines.remove(l)


                for line in lines:
                        values = line.split('\t')
                        if key == values[0]:
                                lines.remove(line)
                                
                              
                w.seek(0)
                w.truncate()
                for line in lines:
                        w.writelines(line)


                w.close()


def IsExist(key=""):

        with open('/home/pi/MagicBox/run/catalogue.tsv', 'r') as r:
                lines = r.readlines()
                
                for line in lines:
                        values = line.split('\t')
                        if key == values[0]:
                                return True

                r.close()
                 
        return False





def Write(key="", command="", name="untitled", pictures=["mario.bmp"]):

        print ("update tsv!")
        with open('/home/pi/MagicBox/run/catalogue.tsv', 'r+') as w:

                lines = w.readlines()
                for l in lines:
                        if len(l) < 3:
                                lines.remove(l)


                replaceIndex = -404
                for index, line in enumerate(lines):
                        values = line.split('\t')
                        if key == values[0]:
                                replaceIndex = index
                                print(f'replace: {lines[replaceIndex]}')

                              
                w.seek(0)
                w.truncate()
                for n, line in enumerate(lines):
                        if n != replaceIndex: w.writelines(line)

                pics = ""        
                for x in pictures:
                        pics = pics+x
                        if(x != pictures[len(pictures)-1]): pics = pics + ','

                
                newrecord = f'\n{key}\t{command}\t{name}\t{pics}'               
                w.writelines(newrecord)
                w.close()


        data = (command, name, pictures)
        cards.update({key:data})



cards = { 'key' : ('command', 'name', ['pic']) }
cards = Read()


