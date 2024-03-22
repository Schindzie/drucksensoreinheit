from configparser import ConfigParser
import serial
import time


print("loading")

#config setup
config = ConfigParser()
config.read(r'config.ini')

com_port = config['preset']['com_port']
print(com_port)
com_port = "COM"+str(com_port)
baud_rate = config['preset']['baud_rate']
print(baud_rate)
pass_phrase = config['preset']['pass_phrase']
max_druck = float(config['preset']['max_druck'])
print(max_druck)


show_funktion = config['debug']['show_funktion']
print(show_funktion)
show_results = config['debug']['show_results']
print(show_results)


#Serial setup
try:
    ser = serial.Serial(com_port, baudrate = baud_rate, timeout=0.5, write_timeout = 0.5)
    print("Serial connection established")
except:
    print("Establishing Serial connection failed!")
    while True:
        1+1
time.sleep(1.2)
ser.write(pass_phrase.encode())
ser.readline()
ser.readline()
numPoints = 50
dataList = [0]*numPoints


#Variablen deklaration
disp_weight = 0.0
pressure = 0.0
anzahl_paletten = 0
pr = [0,0,0,0,0]

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
        arduinoData = int(arduinoData)

        if show_results == 'on':
            print(arduinoData)

        return(arduinoData) #Microamper
    except:
        if show_results == 'on':
            print("Failed to read Data!")
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

    if show_results == 'on':
        print(pressure)

    return(pressure) #Bar

def write_tara(tval):
    if show_funktion == 'on':
        print("write_tara")
    
    ser.close()
    ser = serial.Serial(com_port, baudrate = baud_rate, timeout=0.5, write_timeout = 0.5)
    time.sleep(1.2)
    ser.write("kalibrieren".encode)
    time.sleep(1)
    ser.write(tval.encode)



#MAIN
if __name__ == "__main__":
    print( "\n \n \n")
    print("Ermittle Nullwert... \n")
    
    calc_pressure(calc_average(getDatapoints()))
    for i in range(0,5):
        pr[i] = calc_pressure(calc_average(getDatapoints()))
        print(pr[i])
    
    print("\n\nDer Mittelwert ist: \n")
    nullwert = sum(pr)/len(pr)
    print(nullwert)
    write_tara(nullwert)
    print()
    print("_______________________________________")
    print("Der Mittelwert wurde als Kalibrierwert eingetragen.")
    print("Das Programm kann jetzt geschlossen werden.")
    ser.close()
    while True:
        1+1