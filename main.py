# import required packages

import time
import cv2
import mediapipe as mp
import numpy as np
import cv2
import pyautogui
from pynput.keyboard import Key, Controller
keyboard = Controller()

from pynput.mouse import Button, Controller
mouse = Controller()


from math_exp import get_angle, get_distance
import gesture

      
# Drag and Drop

def drag_and_drop(landmarks, image):
    if gesture.drag_and_drop_condition(landmarks):
        cv2.putText(image, "Drag And Drop", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Double-click to initiate drag
        pyautogui.mouseDown(button='left')
        pyautogui.mouseDown(button='left')
        
        thumb_fig_dist = get_distance(landmarks[4], landmarks[5])
        cursor = gesture.to_move_cursor1(gesture.to_find_index_finger_tip(landmarks), thumb_fig_dist)

        if cursor[2]:  # Cursor movement is allowed
            
            x, y = cursor[0], cursor[1]
            pyautogui.moveTo(x, y, duration=0.1)
            
            # time.sleep(10)
            cv2.putText(image, "Cursor For Drag and Drop", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            if thumb_fig_dist > 70:
                # Release the left mouse button to drop the file
                pyautogui.mouseUp(button='left')
                cv2.putText(image, "Dropped", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)




# Initialize MediaPipe Hands.
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Initialize the VideoCapture object to get video from the webcam.
camera = cv2.VideoCapture(0)

# Get the size of the primary monitor.
screen_width, screen_height = pyautogui.size()

def gesture_recognition(image, landmark_lst,  ):

    thumb_fig_dist = get_distance(landmark_lst[4], landmark_lst[5])

    cursor =gesture.to_move_cursor(gesture.to_find_index_finger_tip(landmark_lst), thumb_fig_dist, landmark_lst)

    # Coordinates
    if gesture.coordinate_recognition(landmark_lst):
        cv2.putText(image, gesture.coordinate_recognition(landmark_lst), (50, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 0), 2)

    # Drag and Drop
    if gesture.drag_and_drop_condition(landmark_lst):
        drag_and_drop(landmark_lst, image)


    #Cursor
    elif cursor[2] and cursor[3]:
        x = cursor[0]
        y = cursor[1]
        pyautogui.moveTo(x, y, duration =0.2)
        cv2.putText(image, "Cursor", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    
    # Left Click
    elif gesture.to_left_click(landmark_lst, thumb_fig_dist):
        
        mouse.press(Button.left)
        mouse.release(Button.left)
        cv2.putText(image, "Left Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Right Click
    elif gesture.to_right_click(landmark_lst, thumb_fig_dist):
                   
        mouse.press(Button.right)
        mouse.release(Button.right)
        cv2.putText(image, "Right Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Double Click
    # elif gesture.to_double_click(landmark_lst, thumb_fig_dist):

    #     pyautogui.doubleClick()
    #     cv2.putText(image, "Double Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)


    

    # # Display/Hide the Desktop
    # elif gesture.to_display_hide_desktop(landmark_lst, thumb_fig_dist):
    #     keyboard1 = keyboard.Controller()
    #     SUPER_KEY = keyboard.Key.cmd

    #     keyboard1.press(SUPER_KEY)
    #     keyboard1.press('d')
    #     keyboard1.release('d')
    #     keyboard1.release(SUPER_KEY)
    #     cv2.putText(image, "Display/Hide the Desktop", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Task Swicher
    elif gesture.to_task_swicher(landmark_lst, thumb_fig_dist):
        cv2.putText(image, "Task Swicher", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        # from pynput.keyboard import Key, Controller

        # keyboard = Controller()

        # Press the Alt  and  Tap key
        keyboard.press(Key.alt)
        keyboard.press(Key.tab)

        # Release the Alt  and  Tap key
        keyboard.release(Key.alt)
        keyboard.release(Key.tab)
        time.sleep(1)







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
