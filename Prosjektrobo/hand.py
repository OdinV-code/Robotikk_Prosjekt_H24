from djitellopy import Tello
import cv2
import pygame
import time
import mediapipe as mp

# Initialize the Tello drone
drone = Tello()
drone.connect()
print("Battery:", drone.get_battery(), "%")

# Start video stream
drone.streamon()

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hand = mp_hands.hands()

while True:
    img = drone.get_frame_read().frame
    img =cv2.resize(img,(380,240))
    succes, frame = img.read() 
    if succes:
        hand.process(frame)
        RGB_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hand = mp_hands.hands(RGB_frame)
        cv2.imshow("Live Feed", frame)

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                print (hand_landmarks)
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        cv2.imshow("Live tracking")
        if cv2.waitKey(1)==ord('q'):
            break