# import required packages

import cv2
import mediapipe as mp
import numpy as np
import cv2
import pyautogui

# Initialize MediaPipe Hands.
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Initialize the VideoCapture object to get video from the webcam.
camera = cv2.VideoCapture(0)

# Get the size of the primary monitor.
screen_width, screen_height = pyautogui.size()


try:
        
    while camera.isOpened():
        success, image = camera.read()
        if not success:
            break
        elif success:

            image = cv2.flip(image, 1)

            # Convert the BGR image to RGB.
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Process the image and find hands.
            result = hands.process(image)

            # Convert the image back to BGR.
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            landmark_lst=[]

            if result.multi_hand_landmarks:

                mp.solutions.drawing_utils.draw_landmarks(image, result.multi_hand_landmarks[0], mp_hands.HAND_CONNECTIONS)
                

                for landmarks in result.multi_hand_landmarks[0].landmark:
                    landmark_lst.append((landmarks.x, landmarks.y, landmarks.z))

                # Display the image.
                cv2.imshow('Hand Tracking and Gesture Recognition', image)
            if cv2.waitKey(5) & 0xFF == 27:
                break  

except Exception as e:
    print('Exception :', e )

finally:
    camera.release()
    cv2.destroyAllWindows()

