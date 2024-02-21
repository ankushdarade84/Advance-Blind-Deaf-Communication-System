import numpy as np
import pandas as pd
import serial
import time
import os
import sys

import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library

pyVER=sys.version
os.system('python3 -m serial.tools.list_ports')
d=pyVER
e=0
r=1
while(e!=-1):
    e=d.find('/dev/rfcomm0')

ser= serial.Serial('/dev/rfcomm0')
GPIO.setmode(GPIO.BOARD)
# GPIO.setwarnings(False)
def receive():  
    f=ser.readline()
    f=f.decode('utf-8')
    n=f
    os.system("espeak '"+str(f)+"' ")
#     os.system("espeak -p 95 '"+f+"' -vaf+f3 ")
    print(n)

B1 = 7
B2 = 11
B3 = 13
B4 = 15
B5 = 19
B6 = 21

GPIO.setup(B1, GPIO.IN)
GPIO.setup(B2, GPIO.IN)
GPIO.setup(B3, GPIO.IN)
GPIO.setup(B4, GPIO.IN)
GPIO.setup(B5, GPIO.IN)
GPIO.setup(B6, GPIO.IN)



dict1 = {'0x1f':'A',
         '0xf':'B',
         '0x1b':'C',
         '0x19':'D',
         '0x1d':'E', 
         '0xb':'F',
         '0x9':'G',
         '0xd':'H',
         '0x2b':'I',
         '0x29':'J',
         '0x17':'K',
         '0x7':'L',
         '0x13':'M',
         '0x11':'N',
         '0x15':'O',
         '0x3':'P',
         '0x1':'Q',
         '0x5':'R',
         '0x23':'S',
         '0x21':'T',
         '0x16':'U',
         '0x6':'V',
         '0x28':'W',
         '0x12':'X',
         '0x10':'Y',
         '0x14':'Z'
         }# This input is when we give 0 pulse for bit

dict2 = {'0x20':'A',
         '0x30':'B',
         '0x24':'C',
         '0x26':'D',
         '0x22':'E', 
         '0x34':'F',
         '0x36':'G',
         '0x32':'H',
         '0x14':'I',
         '0x16':'J',
         '0x28':'K',
         '0x38':'L',
         '0x2c':'M',
         '0x2e':'N',
         '0x2a':'O',
         '0x3c':'P',
         '0x3e':'Q',
         '0x3a':'R',
         '0x1c':'S',
         '0x1e':'T',
         '0x29':'U',
         '0x39':'V',
         '0x17':'W',
         '0x2d':'X',
         '0x2f':'Y',
         '0x2b':'Z'
         }# This input is when we give 1 pulse for bit
q=''
n=''
p=[]
t=[]
g=''
key_list = list(dict1.keys())
val_list = list(dict1.values()) 
print(key_list)
while(1):
  
    r=0
    bb1=GPIO.input(B1)
    bb2=GPIO.input(B2)
    bb3=GPIO.input(B3)
    bb4=GPIO.input(B4)
    bb5=GPIO.input(B5)
    bb6=GPIO.input(B6)
    combine_bit=str(bb1)+str(bb2)+str(bb3)+str(bb4)+str(bb5)+str(bb6)
    print(combine_bit)
    Binary_bit=int(combine_bit,2)
    hex_bit=hex(Binary_bit)
    print(hex_bit)
    if(hex_bit!='0x3f'):
        try:
            position = key_list.index(hex_bit)
            print(val_list[position])
            os.system("espeak '"+(val_list[position])+"' ")
            q=q+str(val_list[position])
        except:pass

        if(hex_bit=='0x2f'):
            q+=" "
            print("space_added")
            #add space
        if(hex_bit=='0x3b'):
            os.system("espeak -p 95 '"+q+"' -vaf+f3")
            print(q)
            #read
        if(hex_bit=='0x37'):
            j=len(q)
            try:q=q[:(j-1)]
            except:pass
            print("last char deleted")
            print(q)
            #delete
        if(hex_bit=='0x3d'):
            if(len(q)>0):
                q=q+'\n\r'
                s=bytes(q,encoding='utf-8')
                ser.write(s)
                print("Send to mobile device")
                q=g
            #send
        if(hex_bit=='0x3e'):
            os.system("espeak -p 95 '"+str(n)+"' -vaf+f3 ")
            print(n)
            n=''
    time.sleep(0.50)
    
    
 

