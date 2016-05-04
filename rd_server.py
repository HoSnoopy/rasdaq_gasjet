import time;
import datetime;
import RPi.GPIO as GPIO
import math
import sys
import argparse
import zmq
import os


GPIO.setmode(GPIO.BCM)  # GPIO-Pin Bezeichnungen verwenden
GPIO.setwarnings(False) # Warnungen deaktivieren

def readAnalogData(adcChannel, SCLKPin, MOSIPin, MISOPin, CSPin, delay):
    """ Funktionsdefinition """
    # Negative Flanke des CS-Signals generieren
    GPIO.output(CSPin,   GPIO.HIGH)
    GPIO.output(CSPin,   GPIO.LOW)
    GPIO.output(SCLKPin, GPIO.LOW)   
    sendCMD = adcChannel
    sendCMD |= 0b00011000 # Entspricht 0x18 (1: Startbit, 1: Single/ended)
    # Senden der Bitkombination (Es finden nur 5 Bits Beruecksichtigung)
    for i in range(5):
        if(sendCMD & 0x10): # Bit an Position 4 pruefen.
            GPIO.output(MOSIPin, GPIO.HIGH)
        else:
            GPIO.output(MOSIPin, GPIO.LOW)
        # Negative Flanke des Clock-Signals generieren
        GPIO.output(SCLKPin, GPIO.HIGH)
        GPIO.output(SCLKPin, GPIO.LOW)
        sendCMD <<= 1 # Bitfolge eine Position nach links schieben
    # Empfangen der Daten des AD-Wandlers
    adcValue = 0 # Reset des gelesenen Wertes
    for i in range(13):
        # Negative Flanke des Clock-Signals generieren
        GPIO.output(SCLKPin, GPIO.HIGH)
        GPIO.output(SCLKPin, GPIO.LOW)
        adcValue <<= 1 # Bitfolge 1 Position nach links schieben
        if(GPIO.input(MISOPin)):
            adcValue |=0x01
    time.sleep(delay) # Kurze Pause
    return adcValue

def setupGPIO(SCLKPin, MOSIPin, MISOPin, CSPin):
    """ GPIO-Pin Setup """
    GPIO.setup(SCLKPin, GPIO.OUT)
    GPIO.setup(MOSIPin, GPIO.OUT)
    GPIO.setup(MISOPin, GPIO.IN)
    GPIO.setup(CSPin,   GPIO.OUT)

def eformat(f, prec, exp_digits):
    s = "%.*e"%(prec, f)
    mantissa, exp = s.split('e')
    # add 1 to digits as 1 is taken by sign +/-
    return "%se%+0*d"%(mantissa, exp_digits+1, int(exp))

# Variablendefinition
#ADCChannel = 0   # AD-Kanal
#ADCChannel = int(sys.argv[1])   # AD-Kanal
SCLK       = 18  # Serial-Clock
MOSI       = 24  # Master-Out-Slave-In
MISO       = 23  # Master-In-Slave-Out
CS         = 25  # Chip-Select
PAUSE      = 0.08 # Anzeigepause

#Quadratradius Gasjet in qm
radius=2.5e-5
# Temperatursensonr auf Kanal1 
#TC	   = 2.000 # max 20K bei 10V
#TC	   = 10.00 # max 100K bei 10V
#TC	   = 15.00 # max 150K bei 10V
TC	   = 30.0 # max 300K bei 10V
# Drucksensor auf Kanal 2
PE 	   = 3.500 # max. 35Bar bei 10V
# Heliumbetrieb
#m = 4.002602/6.02214129e26
#X = 1.63
#Korr = 5.7
#Saug = 1320

# Wasserstoffbetrieb
m = 2.016/6.02214129e26
X = 1.4
Korr = 2.4 
Saug = 1100

# Argonbetrieb
#m = 39.948/6.02214129e26
#Korr = 0.8 
#Saug = 1000

# Kryptonbetrieb
#m = 83.798/6.02214129e26
#Korr = 0.5
#Saug = 850

# Xenonbetrieb
#m = 131.293/6.02214129e26
#Korr = 0.4
#Saug = 850

# Stickstoffbetrieb
#m = 28.0134/6.02214129e26
#Korr = 1
#Saug = 1320

host = "192.168.10.2"
port = 10000


datei = open("/opt/data/gasjet_current.dat","w")
datei.close

context = zmq.Context()
sock = context.socket(zmq.PUB)
sock.bind("tcp://{}:{}".format(host, port))

setupGPIO(SCLK, MOSI, MISO, CS) # GPIO-Pin Setup

while True:
#    print  \
  for ADCChannel in range(0,8):
   if ADCChannel==0: 
        datei = open("/opt/data/gasjet_current.dat","a")
        s=0
        ts=time.time()
        tm=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H:%M:%S')
#        tm=datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S')
        print (tm + "  ", end="")
        datei.write(tm, ) 
        datei.write("  ",)
   d= readAnalogData(ADCChannel, SCLK, MOSI, MISO, CS, PAUSE)
   u= ((d*10.000)/4096) 
   if ADCChannel==0: 
        topic = '10004'
        p=u*TC
        temp=p
        if temp<3: temp=300 # Temperatursensor aus
        p=round(temp,2)
        vgas=math.sqrt(((2*X*1.38e-23*temp)/((X-1)*m)))
        messagedata = tm + ' ' + str(temp)
        sock.send_string("{} {}".format(topic, messagedata))
        topic = '10002'
        datvgas = open("/opt/data/vgas.dat","w")
        datvgas.write(str(round(vgas, 2)))
        datvgas.close
        dattemp = open("/opt/data/temp.dat","w")
        dattemp.write(str(p))
        dattemp.close
        messagedata = tm + ' ' + str(p)
        sock.send_string("{} {}".format(topic, messagedata))
   elif ADCChannel==1:
        topic = '10011'
        p=u*PE
        edruck=p
        p=round(p,2)
        messagedata = tm + ' ' + str(p)
        sock.send_string("{} {}".format(topic, messagedata))
   elif ADCChannel==3:
        topic = '10013'
        p= 10**(u-12)
        messagedata = tm + ' ' + str(p)
        sock.send_string("{} {}".format(topic, messagedata))
   elif ADCChannel==4:
        topic = '10014'
        p= 10**(u-12)
        messagedata = tm + ' ' + str(p)
       	sock.send_string("{} {}".format(topic, messagedata))
   elif ADCChannel==5:
        topic = '10015'
        p= 10**(u-12)
        messagedata = tm + ' ' + str(p)
        sock.send_string("{} {}".format(topic, messagedata))
   elif ADCChannel==6:
        topic = '10016'
        p= 10**((u-7.75)/0.75)
        messagedata = tm + ' ' + str(p)
        sock.send_string("{} {}".format(topic, messagedata))
   else: 
        p= 10**((u-7.75)/0.75)
   if ADCChannel > 3: 
        s=s+p
   if ADCChannel > 1: 
        p= eformat(p, 2, 2)   
        if ADCChannel==2:
                topic = '10012'
                date1 = open("/opt/data/e1.dat","w")
                date1.write(str(p))
                date1.close
                messagedata = tm + ' ' + str(p)
                sock.send_string("{} {}".format(topic, messagedata))
   print (str(p) + "  ",end="",flush=True)
   datei.write(str(p), )
   datei.write("  ",) 
   if ADCChannel==7: 
        topic = '10017'
        messagedata = tm + ' ' + p
        sock.send_string("{} {}".format(topic, messagedata))
        topic = '10005'
#        dichte=(Korr*s*Saug*4e-5)/(3.141*1.38e-23*radius*vgas*temp)
        dichte=(1e-5*4*Korr*s*Saug)/(3.141*1.38e-23*0.005*temp*vgas)
        datei.write(str(eformat(dichte, 2,2))+"\n")	
        datei.close
        datei = open("/opt/data/dichte.dat","w")
        datei.write(str(eformat(dichte, 2, 2)))
        datei.close
        dichte =  eformat(dichte, 2, 2) 
        print (dichte)
        messagedata = tm + ' ' + dichte 
        sock.send_string("{} {}".format(topic, messagedata))
        topic = '10001'
        s = str(s)
        messagedata = tm + ' ' + str(s) + ',' + str(temp) + ',' + str(edruck)
        sock.send_string("{} {}".format(topic, messagedata))
#        print ('\n')
