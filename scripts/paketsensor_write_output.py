"""
Findet den angeschlossenen Gewichts-Sensor und wiederholt im Zweifelsfall die Suche bis
ein angeschlossenes Geraet richtig antwortet.
Gibt aktuellen Status in einer kleinen GUI wieder.

"""

from configparser import ConfigParser
import serial.tools.list_ports as port_list
import serial
import requests
import time
import sys
import json
import tkinter as tk
from requests.structures import CaseInsensitiveDict

"""
Änderungen

1. Fenster hinzufügen, das aktuellen Status für Nutzer anzeigt 
2. Nicht schließen, wenn kein Port gefunden wurde sondern Nachricht in Fenster und erneut suchen
3. Bei Verbindungsverlusst Meldung an Fenster evtl. auf oberste Ebene setzen
"""

print("loading")

#config setup
config = ConfigParser()
config.read(r'config.ini')


#API setup
base = config['preset']['base']
print("base: "+str(base))
print("basic get from: "+str(base)+ "Data")


baud_rate = config['preset']['baud_rate']
print("baud rate: "+str(baud_rate))
max_druck = float(config['preset']['max_druck'])
print("max druck: "+str(max_druck))
pass_phrase = config['preset']['pass_phrase']
print("pass phrase: "+str(pass_phrase))

show_funktion = config['debug']['show_funktion']
print("show funktion: "+str(show_funktion))
show_results = config['debug']['show_results']
print("show results: "+str(show_results))


def update_data(d):
    headers = {"Content-Type": "application/json"}
    data = {"datenpunkt":d}
    response = requests.post(base + "Data/Update", json=data, headers=headers)
    return response.json()


def get_data():
    response = requests.get(base + "Data")
    return response.json()


def write_output(d):        #funktioniert
    out = open('./output.txt','w')    #C:/Programme/Gewichtssensor/output.txt
    output = ''
    timestamp = time.asctime()
    output += timestamp + ' - ' + str(d)
    out.write(output)
    out.close()
    update_data(d)


#findet Com Port und gibt diesen zurück
#prüft zunächst in config.ini voreingestellten Port
#durchläuft dann die Liste an verbundenen Com Ports
def findCOMport():
    ports = list(port_list.comports())
    connected =False
    try:
        com_port = config['preset']['com_port']
        com_port = "COM"+str(com_port)
        print("\n\nvoreingestellter port: "+com_port)
        ser = serial.Serial(com_port, baudrate = baud_rate, timeout=1, write_timeout=0.5)
        print("waiting for device")
        time.sleep(1.2)
        print("port "+ com_port +" opened")
        ser.read()
        ser.read()
        ser.write(pass_phrase.encode())
        print("pass phrase sent")
        time.sleep(0.1)
        answer = ser.readline()
        print("port answer: "+str(answer))
        ser.close()
        print("port closed")
        if answer == b'connection established\r\n':
            print("verbunden mit voreingestelltem port")
            connected = True
        ser.close()
    except:
        print("voreingestellter port nicht erreichbar")

    if connected == False:
        for i in ports:
            com_port = str(i)
            print("\n\nversuche verbindung zu "+com_port+" herzustellen")
            port = com_port.split(' - ')
            com_port = port[0]
            
            
            try:                                
                ser = serial.Serial(com_port, baudrate = baud_rate, timeout=1, write_timeout=0.5)
                print("waiting for device")
                time.sleep(1.2)
                print("port "+ com_port +" opened")
                ser.read()
                ser.read()
                ser.write(pass_phrase.encode())
                print("pass phrase sent")
                time.sleep(0.1)
                answer = ser.readline()
                print("port answer: "+str(answer))
                ser.close()
                print("port closed")
                if answer == b'connection established\r\n':
                    print("answer correct")
                    connected = True
                    break
                
            except:
                print("NO")
                #out = open('C:/Programme/Gewichtssensor/output.txt','w')
                out = open('./output.txt','w')  #C:/Programme/Gewichtssensor/output.txt
                output = '...there was no device found to connect to\nYou will have to set the port manually in the "config.ini" file and restart'
                out.write(output)
                out.close()

    if connected == False:
        print("Es konnte kein nutzbarer Com Port gefunden werden!")
        print("Bitte stellen sie sicher, dass das gewünschte Gerät erkannt wird")
        write_output(-99999.9)
        sys.exit()
    return(com_port)



pass_phrase = "request-connect"
com_port = "-1"

com_port = findCOMport()

print("using com port: "+str(com_port)+"\n\n")


#Serial setup

ser = serial.Serial(com_port, baudrate = baud_rate, timeout=1, write_timeout=0.5)
print("waiting for device")
time.sleep(1.2)
print("port "+ com_port +" opened")
ser.read()
ser.read()
ser.write(pass_phrase.encode())
print("pass phrase sent")
time.sleep(0.1)
answer = ser.readline()
print("port answer: "+str(answer))
time.sleep(0.1)
kalibrierwertArduino = (ser.readline())
print("port answer: "+str(kalibrierwertArduino))


#Variablen deklaration
disp_weight = 0.0
pressure = 0.0
anzahl_paletten = 0
kalibrierwert = float(kalibrierwertArduino)
numPoints = 50
dataList = [0]*numPoints

print("done loading")



#Funktions deklaration

def getDatapoints():        #funktioniert
    if show_funktion == 'on':
        print("getDatapoints")
        
    for i in range(0, numPoints):
        dataList[i] = readData()

    if show_results == 'on':
        print(dataList)

    return(dataList)


def readData():     #funktioniert
    if show_funktion == 'on':
        print("readData")

    try:
        #read values
        arduinoString = str(ser.readline())
        
        #turn data into usable value
        arduinoData = arduinoString[2:-5]
        arduinoData = float(arduinoData)

        if show_results == 'on':
            print(arduinoData)

        return(arduinoData) #Microamper
    except:
        if show_results == 'on':
            print("recieved" + arduinoString[2:-5])
            print("read data failed")
        return(1)


def calc_average(num):      #funktioniert
    if show_funktion == 'on':
        print("calc_average")

    avg = sum(num)/len(num)
    avg *= 0.000001

    if show_results == 'on':
        print(avg)

    return(avg) #Amper


def calc_pressure(amps):        #funktioniert
    if show_funktion == 'on':
        print("calc_pressure")

    pressure = ((amps-0.004)*max_druck)/(0.02-0.004)
    pressure -= kalibrierwert

    if show_results == 'on':
        print(pressure)

    return(pressure) #Bar


def calcWeight(d):      #funktiert scheinbar
    if show_funktion == 'on':
        print("calcWeight")

    a_d = calc_average(d)
    p = calc_pressure(a_d)
    weight = (p)/(0.0184)

    if show_results == 'on':
        print("a_d")
        print(a_d)
        print("p")
        print(p)
        print("weight")
        print(weight)

    return(weight) #Kilogramm


###############################################################################################
###############################################################################################


#MAIN
if __name__ == "__main__":
    if com_port != "-1":
        try:
            disp_weight = round(calcWeight(getDatapoints()), 1)
            print("disp_weight")
            print(disp_weight)
            write_output(disp_weight)
        except:
            print("Link lost")
            write_output(-99999.9)
            sys.exit()
    else:
        print("Es konnte kein nutzbarer Com Port gefunden werden!")
        print("Bitte stellen sie sicher, dass das gewünschte Gerät erkannt wird")
        write_output(-99999.9)
        sys.exit()