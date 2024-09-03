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


# from math_exp import get_angle, get_distance
# import gesture


# To Find the Angle between the three coordinates
def get_angle(a, b, c):
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(np.degrees(radians))
    return angle

# To Find the Distance between the two coordinates
def get_distance(x, y):
    if len(x) < 2:
        return False
    (x1, y1, z1), (x2, y2, z2) = x, y
    L = np.hypot(x2 - x1, y2 - y1)
    return np.interp(L, [0, 1], [0, 1000])


# Get the size of the primary monitor.
screen_width, screen_height = pyautogui.size()

# Detecting Coordinates of the  Index finger tip point
def coordinate_recognition(landmarks):
    if len(landmarks) < 7:
        return None

    # Extract X, Y, Z coordinates of the index finger tip and base (landmarks 8 and 5).
    x_tip, y_tip, z_tip = landmarks[8][0], landmarks[8][1], landmarks[8][2]
    text = "Index Finger Tip --->>> X : " + str(round(x_tip, 4)) + ", Y : " +str(round(y_tip, 4))+  ", Z :" +str(round(z_tip, 4))
    # print(text)
    return text


# Find the coordinates of the  Index finger tip
def to_find_index_finger_tip(landmarks):
    if len(landmarks) >= 8:
        return landmarks[8]
    return None, None, None


# Condition for Cursor Moments
def to_move_cursor(finger_tip, distance, landmarks):
    if finger_tip is not None:
        x = int(finger_tip[0] * screen_width)
        y = int(finger_tip[1] * 1.1 * screen_height)
        if x and y and distance > 70:
            return x, y, distance > 70, get_angle(landmarks[5], landmarks[6], landmarks[8]) > 100
        else:
            return x, y, False, False


# Condition for Left Click
def to_left_click(landmarks, thumb_dis):
    return (get_angle(landmarks[5], landmarks[6], landmarks[8]) < 70 and 
            get_angle(landmarks[9], landmarks[10], landmarks[12]) > 150 and
            get_angle(landmarks[13], landmarks[14], landmarks[16]) < 70 and 
            get_angle(landmarks[17], landmarks[18], landmarks[20]) < 70 and
             thumb_dis < 70)
    

# Condition for Right Click
def to_right_click(landmarks, thumb_dis):
    return (get_angle(landmarks[5], landmarks[6], landmarks[8]) > 150 and 
            get_angle(landmarks[9], landmarks[10], landmarks[12]) < 70  and
            get_angle(landmarks[13], landmarks[14], landmarks[16]) < 70 and 
            get_angle(landmarks[17], landmarks[18], landmarks[20]) < 70 and
             thumb_dis < 70)


# Condition for Double Click
def to_double_click(landmarks, thumb_dis):
    return (get_angle(landmarks[5], landmarks[6], landmarks[8]) < 90  and 
            get_angle(landmarks[9], landmarks[10], landmarks[12]) < 90 and
            get_angle(landmarks[13], landmarks[14], landmarks[16]) > 70 and 
            get_angle(landmarks[17], landmarks[18], landmarks[20]) > 70 and
             thumb_dis < 70)
            
# Condition for Display/Hide the Desktop
def to_display_hide_desktop(landmarks, thumb_dis):
    return (get_angle(landmarks[5], landmarks[6], landmarks[8])<60 and 
            get_angle(landmarks[9], landmarks[10], landmarks[12] ) < 60 and
             thumb_dis < 50)

# Condition for Drag and Drop
def drag_and_drop_condition(landmarks):
    if len(landmarks) ==21:
        return (get_angle(landmarks[5], landmarks[6], landmarks[8]) > 150 and 
                get_angle(landmarks[9], landmarks[10], landmarks[12]) < 80 and 
                get_angle(landmarks[13], landmarks[14], landmarks[16]) < 80 and 
                get_angle(landmarks[17], landmarks[18], landmarks[20]) > 150 )
    
# Condition for Cursor inbetween the  Drag and Drop 
def to_move_cursor1(finger_tip, distance):
    if finger_tip is not None:
        x = int(finger_tip[0] * screen_width)
        y = int(finger_tip[1] * 1.1 * screen_height)
        if x and y and distance < 90:
            return x, y, distance < 90
        else:
            return x, y, False
  


def to_task_swicher(landmarks, thumb_dis):
    index = get_distance(landmarks[5], landmarks[8])
    middle = get_distance(landmarks[9], landmarks[12])
    ring = get_distance(landmarks[13], landmarks[16])
    pinky = get_distance(landmarks[17], landmarks[20])
    return (index < 60 and
            middle < 60 and 
            ring < 60 and 
            pinky < 60 and 
            thumb_dis > 90)
      
# Drag and Drop

def drag_and_drop(landmarks, image):
    if drag_and_drop_condition(landmarks):
        cv2.putText(image, "Drag And Drop", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Double-click to initiate drag
        pyautogui.mouseDown(button='left')
        pyautogui.mouseDown(button='left')
        
        thumb_fig_dist = get_distance(landmarks[4], landmarks[5])
        cursor = to_move_cursor1(to_find_index_finger_tip(landmarks), thumb_fig_dist)

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

    cursor =to_move_cursor(to_find_index_finger_tip(landmark_lst), thumb_fig_dist, landmark_lst)

    # Coordinates
    if coordinate_recognition(landmark_lst):
        cv2.putText(image, coordinate_recognition(landmark_lst), (50, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 0), 2)

    # Drag and Drop
    if drag_and_drop_condition(landmark_lst):
        drag_and_drop(landmark_lst, image)


    #Cursor
    elif cursor[2] and cursor[3]:
        x = cursor[0]
        y = cursor[1]
        pyautogui.moveTo(x, y)
        cv2.putText(image, "Cursor", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    
    # Left Click
    elif to_left_click(landmark_lst, thumb_fig_dist):
        
        mouse.press(Button.left)
        mouse.release(Button.left)
        cv2.putText(image, "Left Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Right Click
    elif to_right_click(landmark_lst, thumb_fig_dist):
                   
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
    elif to_task_swicher(landmark_lst, thumb_fig_dist):
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
