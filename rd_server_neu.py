#!/usr/bin/python

#Einfaches Pythonscript zum Auslesen von 2 MCP3208-ADC-Wandlern (insgesamt 16 Kanaele) per SPI-Interface (NICHT GPIO!)
#Ich habe als Referenzspannung 3,3V, die per Spannungsteiler von max. 10V heruntergebrochen werden. 

import spidev
import time
import datetime
import math

spi = spidev.SpiDev()

#Frequenz des SPI-Busses. Maximal 5000000, geht man drueber, kommen unsinnige Werte heraus.

datei = '/opt/data/wwk.dat'
herz = 10
warte = 0.9
zeile=[]


dat = open(datei, 'w')
dat.close

#umrechnen der werte in ein schoeneres Format und in einen String
def eformat(f, prec, exp_digits):
    s = "%.*e"%(prec, f)
    mantissa, exp = s.split('e')
    # add 1 to digits as 1 is taken by sign +/-
    return "%se%+0*d"%(mantissa, exp_digits+1, int(exp))

#umrechnen der Spannung in einen Druckwert
def ionivac(wert):
    u = float(wert)
    p = 10**(u-12)
    p = eformat(p, 2, 2)
    return (p)

#umrechnen der Spannung in einen Druckwert
def widerange(wert): 
    u = float(wert)
    p = 10**((u-7.75)/(0.75))
    p = eformat(p, 2, 2)
    return (p)


while True:

  for s in range (2):
     spi.open(0,s)  # oeffnen des einen oder anderen MCP3208 
     spi.max_speed_hz=(herz)
     for c in range (8):
       #Bestimmung des Kommandos zum Empfangen der einzelnen Kanaele. Siehe dazu auch https://github.com/xaratustrah/rasdaq
       if c < 4:
          com1 = 0x06
          com2 = c * 0x40
       else: 
          com1 = 0x07
          com2 = (c-4) * 0x40
    
       antwort = spi.xfer([com1, com2, 0])


       val = ((antwort[1] << 8) + antwort[2])  # Interpretieren der Antwort
       val = int(val)
       u = val * 0.002441406                  
       zeile.append(str(u))
     spi.close() 
# herausschreiben und Umrechnung der Spannungswerte am Ende der 16 eingelesenen Kanaele
     if s == 1:
        ts = time.time()
        ausgang = (str(datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H:%M:%S')) + ' ')  # Zeitskala
        ausgang = (ausgang + (ionivac(zeile[1])) + ' ')
        ausgang = (ausgang + (ionivac(zeile[2])) + ' ')
        ausgang = (ausgang + (ionivac(zeile[3])) + ' ')
        ausgang = (ausgang + (ionivac(zeile[4])) + ' ')
        ausgang = (ausgang + (ionivac(zeile[5])) + ' ')
        ausgang = (ausgang + (ionivac(zeile[6])) + ' ')
        ausgang = (ausgang + (ionivac(zeile[7])) + ' ')
        ausgang = (ausgang + (ionivac(zeile[8])) + ' ')
        ausgang = (ausgang + (ionivac(zeile[9])) + ' ')
        ausgang = (ausgang + (ionivac(zeile[10])) + ' ')
        ausgang = (ausgang + (ionivac(zeile[11])) + ' ')
        ausgang = (ausgang + (ionivac(zeile[12])) + ' ')
        ausgang = (ausgang + (ionivac(zeile[13])) + ' ')
        ausgang = (ausgang + (ionivac(zeile[14])) + ' ')
        ausgang = (ausgang + (ionivac(zeile[15])) + '\n ')
        print (ausgang)
        dat = open(datei, 'a')
        dat.write(str(ausgang))
        dat.close
        time.sleep(warte)
