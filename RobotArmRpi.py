##################################################
###################  MODULES  ####################
##################################################

import cv2
import math
import random
from buildhat import Motor
import mediapipe as freedomtech


##################################################
###################  FUNCTIONS  ##################
##################################################

def hand_status(random_choice,pinky_motor,middle_motor,index_motor,thumb_motor):
    status="" 
    #rock
    if random_choice == 0:
        pinky_motor.run_to_position(90)
        index_motor.run_to_position(-80)
        middle_motor.run_to_position(90)
        thumb_motor.run_to_position(90)
        status = "rock"
    #paper
    elif random_choice == 1:
        pinky_motor.run_to_position(0)
        index_motor.run_to_position(0)
        middle_motor.run_to_position(0)
        thumb_motor.run_to_position(0)
        status = "paper"
    #sissor
    elif random_choice == 2:
        pinky_motor.run_to_position(90)
        index_motor.run_to_position(0)
        middle_motor.run_to_position(80)
        thumb_motor.run_to_position(0)
        status = "sissor"
    return status

def findpostion(frame1):
    list=[]
    results = mod.process(cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB))
    if results.multi_hand_landmarks != None:
       for handLandmarks in results.multi_hand_landmarks:
           drawingModule.draw_landmarks(frame1, handLandmarks, handsModule.HAND_CONNECTIONS)
           list=[]
           for id, pt in enumerate (handLandmarks.landmark):
                x = int(pt.x * w)
                y = int(pt.y * h)
                list.append([id,x,y])

    return list            

def findnameoflandmark(frame1):
     list=[]
     results = mod.process(cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB))
     if results.multi_hand_landmarks != None:
        for handLandmarks in results.multi_hand_landmarks:


            for point in handsModule.HandLandmark:
                 list.append(str(point).replace ("< ","").replace("HandLandmark.", "").replace("_"," ").replace("[]",""))
     return list
    
    
    
##################################################
################  INITIALIZATION  ################
##################################################

drawingModule = freedomtech.solutions.drawing_utils
handsModule = freedomtech.solutions.hands

mod=handsModule.Hands()

h=480
w=640 

cap = cv2.VideoCapture(0)
tip=[8,12,16,20,4]
tipname=[8,12,16,20,4]
fingers=[]
old_fingers = []
finger=[]
thumb = 1
old_thumb = 1

thumb_motor = Motor('D')
index_motor = Motor('C')
middle_motor = Motor('B') #--> caution: middle move together with ring
pinky_motor = Motor('A') 

##################################################
################      ACTIONS     ################ 
##################################################

random_choice = 0 #random.randint(0,2)
status = hand_status(random_choice,pinky_motor,middle_motor,index_motor,thumb_motor)
      
#Create an infinite loop which will produce the live feed to our desktop and that will search for hands
# while True:
     
#     ret, frame = cap.read() 
    
#     #Unedit the below line if your live feed is produced upsidedown
#     #flipped = cv2.flip(frame, flipCode = -1)
    
#     #Determines the frame size, 640 x 480 offers a nice balance between speed and accurate identification
#     frame1 = cv2.resize(frame, (320, 240))

# #Below is used to determine location of the joints of the fingers 
#     a=findpostion(frame1)
#     b=findnameoflandmark(frame1)
    
#     #random_choice = random.randint(0,2)
#     #status = hand_status(random_choice,pinky_motor,middle_motor,index_motor,thumb_motor)
    

#     #Below shows the current frame to the desktop 
#     cv2.imshow("Frame", frame1);
#     key = cv2.waitKey(1) & 0xFF
    
#     #Below states that if the |q| is press on the keyboard it will stop the system
#     if key == ord("q"):
#         break
