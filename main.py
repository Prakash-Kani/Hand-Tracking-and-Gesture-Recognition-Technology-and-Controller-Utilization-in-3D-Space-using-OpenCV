# import required packages

import cv2
import mediapipe as mp
import numpy as np
import cv2
import pyautogui
from pynput.mouse import Button, Controller

from math_exp import get_angle, get_distance
import gesture as ges


mouse = Controller()

# Initialize MediaPipe Hands.
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Initialize the VideoCapture object to get video from the webcam.
camera = cv2.VideoCapture(0)

# Get the size of the primary monitor.
screen_width, screen_height = pyautogui.size()

def gesture_recognition(image, landmark_lst,  ):

    thump_fig_dist = get_distance(landmark_lst[4], landmark_lst[5])

    cursor =ges.to_move_cursor(ges.to_find_index_finger_tip(landmark_lst), thump_fig_dist)

    #Cursor
    if cursor[2]:
        x = cursor[0]
        y = cursor[1]
        pyautogui.moveTo(x, y, duration =0.2)
        cv2.putText(image, "Cursor", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    
    # Left Click
    elif ges.to_left_click(landmark_lst, thump_fig_dist):
        
        mouse.press(Button.left)
        mouse.release(Button.left)
        cv2.putText(image, "Left Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)






def main():
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

                    
                    
                    gesture_recognition(image, landmark_lst )

                # Display the image.
                cv2.imshow('Hand Tracking and Gesture Recognition', image)
                if cv2.waitKey(5) & 0xFF == 27:
                    break  

    except Exception as e:
        print('Exception :', e )

    finally:
        camera.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
