##################################################
###################  MODULES  ####################
##################################################

import cv2
import math
import time
import random
from buildhat import Motor
import mediapipe as mp


##################################################
###################  FUNCTIONS  ##################
##################################################

def hand_status(random_choice,pinky_motor,middle_motor,index_motor,thumb_motor):
    #rock
    if random_choice == 0:
        thumb_motor.run_to_position(170)
        pinky_motor.run_to_position(90)
        index_motor.run_to_position(-80)
        middle_motor.run_to_position(90)
        return "rock"
    #paper
    elif random_choice == 1:
        pinky_motor.run_to_position(0)
        index_motor.run_to_position(0)
        middle_motor.run_to_position(0)
        thumb_motor.run_to_position(0)
        return "paper"
    #sissor
    elif random_choice == 2:
        pinky_motor.run_to_position(90)
        index_motor.run_to_position(0)
        middle_motor.run_to_position(80)
        thumb_motor.run_to_position(0)
        return "scissors"
def reset(pinky_motor,middle_motor,index_motor,thumb_motor):
    pinky_motor.run_to_position(0)
    index_motor.run_to_position(0)
    middle_motor.run_to_position(0)
    thumb_motor.run_to_position(0)
    print("Reset")
def getHandMove(hand_landmarks):
    landmarks = hand_landmarks.landmark 
    if all([landmarks[i].y < landmarks[i+3].y for i in range(9,20,4)]):
        return "rock" 
    elif landmarks[13].y < landmarks[16].y and landmarks[17].y < landmarks[20].y:
        return "scissors"
    else:
        return "paper"

    
    
    
##################################################
################  INITIALIZATION  ################
##################################################
thumb_motor = Motor('D')
index_motor = Motor('C')
middle_motor = Motor('B') #--> caution: middle move together with ring
pinky_motor = Motor('A') 

clock = 0
text = ""
humain = None
robot = None
succes = True
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)
prev_frame_time = 0
new_frame_time = 0

with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
  while cap.isOpened():
    ret, image = cap.read()
    if not ret:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue   

    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)

    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.resize(image, (640, 480))
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                image,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())
    
    # Flip the image horizontally for a selfie-view display.
    image = cv2.flip(image, 1)
    new_frame_time = time.time() 
    fps = int(1/(new_frame_time-prev_frame_time))
    prev_frame_time = new_frame_time
    if 0 <= clock < 20:
        success = True
        text2 = "Ready ?"
        random_choice = random.randint(0,2)
    elif clock < 30:
        text2 = "3..."
    elif clock < 50:
        text2 = "2..."
    elif clock < 70:
        text2 = "1..."
    elif clock == 90:
        text2 = "GO !"
        hls = results.multi_hand_landmarks
        if hls and len(hls) == 1:
            humain = getHandMove(hls[0])
            robot = hand_status(random_choice,pinky_motor,middle_motor,index_motor,thumb_motor)
        else:
            sucess = False
    elif clock < 120:
        if success and robot !=0 :
            text = f"Humain Player {humain} vs robot {robot} "
            if humain == robot:
                text = f"{text}: Game is tied."
                text2 = "Nice try again"
            elif humain == "paper" and robot == "rock":
                text = f"{text}: Humain wins."
                text2 = "Yes ! Glory to humain"
            elif humain == "rock" and robot == "scissors":
                text = f"{text}: Humain wins."
                text2 = "Yes ! Glory to humain"
            elif humain == None or robot == None:
                text = "No player or didn't play properly"
                text2 = "Restart!"
            else:
                text = f"{text}:  Robot wins"
                text2 = "Fuck !"
        else:
            text = "No player or didn't play properly"
            text2 = "Restart !"
    cv2.putText(image,f"{fps}", (200,10),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),1,cv2.LINE_AA)
    cv2.putText(image,f"{text2}", (10,30),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),1,cv2.LINE_AA)
    cv2.putText(image,text, (150,60),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),2,cv2.LINE_AA)
    clock = (clock + 1) % 120
    text = ""
    cv2.imshow('MediaPipe Hands', image) 
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()