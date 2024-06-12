import numpy as np

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