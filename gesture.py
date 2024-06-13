
import pyautogui
from math_exp import get_angle, get_distance

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
def to_move_cursor(finger_tip, distance):
    if finger_tip is not None:
        x = int(finger_tip[0] * screen_width)
        y = int(finger_tip[1] * 1.1 * screen_height)
        if x and y and distance > 70:
            return x, y, distance > 70
        else:
            return x, y, False


# Condition for Left Click
def to_left_click(landmarks, thump_dis):
    return (get_angle(landmarks[5], landmarks[6], landmarks[8]) < 70 and 
            get_angle(landmarks[9], landmarks[10], landmarks[12]) > 150 and
            get_angle(landmarks[13], landmarks[14], landmarks[16]) < 70 and 
            get_angle(landmarks[17], landmarks[18], landmarks[20]) < 70 and
             thump_dis < 70)
    

# Condition for Right Click
def to_right_click(landmarks, thump_dis):
    return (get_angle(landmarks[5], landmarks[6], landmarks[8]) > 150 and 
            get_angle(landmarks[9], landmarks[10], landmarks[12]) < 70  and
            get_angle(landmarks[13], landmarks[14], landmarks[16]) < 70 and 
            get_angle(landmarks[17], landmarks[18], landmarks[20]) < 70 and
             thump_dis < 70)


# Condition for Double Click
def to_double_click(landmarks, thump_dis):
    return (get_angle(landmarks[5], landmarks[6], landmarks[8]) < 90  and 
            get_angle(landmarks[9], landmarks[10], landmarks[12]) < 90 and
            get_angle(landmarks[13], landmarks[14], landmarks[16]) < 70 and 
            get_angle(landmarks[17], landmarks[18], landmarks[20]) < 70 and
             thump_dis < 70)
            
# Condition for Display/Hide the Desktop
def to_display_hide_desktop(landmarks, thump_dis):
    return (get_angle(landmarks[5], landmarks[6], landmarks[8])<60 and 
            get_angle(landmarks[9], landmarks[10], landmarks[12] ) < 60 and
             thump_dis < 50)

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
  