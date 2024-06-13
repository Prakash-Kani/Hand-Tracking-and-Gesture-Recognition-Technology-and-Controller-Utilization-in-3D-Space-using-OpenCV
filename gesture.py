
import pyautogui

# Get the size of the primary monitor.
screen_width, screen_height = pyautogui.size()


# Find the coordinates of the  Index finger tip
def to_find_index_finger_tip(landmarks):
    if len(landmarks)>=8:
        return landmarks[8]
    return None, None, None


# Condition for Cursor Moments
def to_move_cursor(finger_tip, distance):
    if finger_tip is not None:
        x = int(finger_tip[0] * screen_width)
        y = int(finger_tip[1] * 1.1 * screen_height)
        if x and y and distance >70:
            return x, y, distance >70
        else:
            return x, y, False

            