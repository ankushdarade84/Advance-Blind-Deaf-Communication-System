import numpy as np
import pandas as pd
import serial
import time
import os
import sys

import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library

pyVER=sys.version
os.system('python -m serial.tools.list_ports')
d=pyVER
e=0
while(e!=-1):
    e=d.find('/dev/rfcomm0')

ser= serial.Serial('/dev/rfcomm0')
GPIO.setmode(GPIO.BOARD)
p=[]
n=''
b=[]
def receive():  
    f=ser.readline()
    f=f.decode('utf-8')
    n=f
#     os.system("espeak '"+str(n)+"' ")
    os.system("espeak  '"+f+"' -vaf+m3 ")
    print(n)
    n=''
while(1):
    for  i in range(0,1):
        receive()
#     time.sleep(0.50)
    
    
    
    
    
    
    
    
    
    
#     r=1
#     e=1
#     if(r==1):
#         f=ser.read()
#         print(f)
#         f=f.decode('utf-8')
#         p.append(f)
#         t="".join(p)
#         print(t)
#         if(f=='\r'):
#             
#             b=t
#             e=0
#             ser.flush()
#             t=""
#             f=""
# 
#             os.system("espeak -p 95 '"+str(b)+"' -vaf+f3")
#             print(str(b))
#             ser.flush()
#             b=""
#             #b=['']
#             t=""
#             f=""
#             print(str(b))
# #             print(str(b))
# #             os.system("espeak -p 95 '"+b+"' -vaf+f3")
#             r=0
#             #os.system("espeak -p 95 '"+str(t)+"' -vaf+f3 ")
# #     if(e!=0):
# #         os.system("espeak -p 95 '"+str(b)+"' -vaf+f3")
# #         print(str(b))
# #         ser.flush()
# #         b=""
# #         #b=['']
# #         t=""
# #         f=""
# #         print(str(b))
    
    

               

                
    