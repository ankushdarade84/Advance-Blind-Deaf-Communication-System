#! /usr/bin/python
# import the necessary packages
import sys #import system function
import os
import cv2
import imutils
from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import numpy as np #import numpy library
import pandas as pd # imprt pandas for arry opeation
import pickle
import time #import time fpr delay
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import requests
import serial #import serial port

pyVER=sys.version
os.system('python3 -m serial.tools.list_ports')
d=pyVER
e=0
c=0
r=1
while(e!=-1):
    e=d.find('/dev/rfcomm0')
    c=d.find('/dev/ttyAMA0')

ser= serial.Serial('/dev/rfcomm0')
serr= serial.Serial('/dev/ttyAMA0')
#os.system('sudo python /home/pi/Desktop/combine_project/bt_connect.py')
def receive():
    fi=serr.readline()
    fi=fi.decode('utf-8')
    
    os.system("espeak '"+str(fi)+"' ")
#     os.system("espeak -p 95 '"+f+"' -vaf+f3 ")
    print(fi)

GPIO.setmode(GPIO.BOARD)

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

#Initialize 'currentname' to trigger only when a new person is identified.
currentname = "unknown"
#Determine faces from encodings.pickle file model created from train_model.py
encodingsP = "encodings.pickle"
#use this xml file
cascade = "haarcascade_frontalface_default.xml"
# load the known faces and embeddings along with OpenCV's Haar
# cascade for face detection
print("[INFO] loading encodings + face detector...")
data = pickle.loads(open(encodingsP, "rb").read())
detector = cv2.CascadeClassifier(cascade)
# initialize the video stream and allow the camera sensor to warm up
# Set the ser to the followng
# src = 0 : for the build in single web cam, could be your laptop webcam
# src = 2 : I had to set it to 2 inorder to use the USB webcam attached to my laptop
#vs = VideoStream(src=2,framerate=10).start()
#vs = VideoStream(usePiCamera=True).start()
#time.sleep(2.0)
# initialize the video stream and allow the camera sensor to warm up
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
# vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)
# start the FPS counter
fps = FPS().start()

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
         }# This input is when we give 0 pulse for bit all bit is 1 

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
key_list = list(dict1.keys())
val_list = list(dict1.values()) 
print(key_list)
sppp=''
names=''
# loop over frames from the video file stream
while True:
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
    
    # grab the frame from the threaded video stream and resize it
    # to 500px (to speedup processing)
    frame = vs.read()
    frame = imutils.resize(frame, width=500)
    # Detect the fce boxes
    boxes = face_recognition.face_locations(frame)
    
    # convert the input frame from (1) BGR to grayscale (for face
    # detection) and (2) from BGR to RGB (for face recognition)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # detect faces in the grayscale frame
    rects = detector.detectMultiScale(gray, scaleFactor=1.1, 
        minNeighbors=5, minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE)

    # OpenCV returns bounding box coordinates in (x, y, w, h) order
    # but we need them in (top, right, bottom, left) order, so we
    # need to do a bit of reordering
    boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]

    # compute the facial embeddings for each face bounding box
    encodings = face_recognition.face_encodings(frame, boxes)
    names = []

    # loop over the facial embeddings
    for encoding in encodings:
        # attempt to match each face in the input image to our known
        # encodings
        matches = face_recognition.compare_faces(data["encodings"],
            encoding)
        name = "Unknown" #if face is not recognized, then print Unknown

        # check to see if we have found a match
        if True in matches:
            # find the indexes of all matched faces then initialize a
            # dictionary to count the total number of times each face
            # was matched
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}

            # loop over the matched indexes and maintain a count for
            # each recognized face face
            for i in matchedIdxs:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1

            # determine the recognized face with the largest number
            # of votes (note: in the event of an unlikely tie Python
            # will select first entry in the dictionary)
            name = max(counts, key=counts.get)

            #If someone in your dataset is identified, print their name on the screen
            if currentname != name:
                currentname = name
                print(currentname)
                
        # update the list of names
        names.append(name)
        print(names)
  

    # loop over the recognized faces
    for ((top, right, bottom, left), name) in zip(boxes, names):
        # draw the predicted face name on the image - color is in BGR
        cv2.rectangle(frame, (left, top), (right, bottom),
            (0, 255, 225), 2)
        y = top - 15 if top - 15 > 15 else top + 15
        cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
            .8, (0, 255, 255), 2)

    # display the image to our screen
    cv2.imshow("Facial Recognition is Running", frame)
    key = cv2.waitKey(1) & 0xFF

    # quit when 'q' key is pressed
    if key == ord("q"):
        break

    # update the FPS counter
    fps.update()
    if(hex_bit=='0x3e'):
        os.system("espeak -ven+m5  '"+str(names)+"' -vaf+f3 ")
        print (names)
        
        
#     #code for read data serially
#     if(hex_bit=='0x3f'):
#         for  i in range(0,1):
#             receive()

        
    if(hex_bit!='0x3f'):
        try:
            position = key_list.index(hex_bit)
            print(val_list[position])
            os.system("espeak '"+(val_list[position])+"' ")
            q=q+str(val_list[position])
        except:     
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
                print("last char deleted string is ="+q)
                print(q)
                #delete
            if(hex_bit=='0x3d'):
                q=q+'\n\r'
                s=bytes(q,encoding='utf-8')
                ser.write(s)
                print("Send to mobile device")
                q=''
                #send



#         f=f.decode('utf-8')
#         n=f
#         os.system("espeak '"+str(f)+"' ")
# #     os.system("espeak -p 95 '"+f+"' -vaf+f3 ")
#         print(n)
#         f=""
#         time.sleep(1)


            

        
    
# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()

