import cv2
import numpy as np

def nothing(x):
    pass

def create_trackbars(window_name):
    cv2.createTrackbar('H_low', window_name, 0, 179, nothing)
    cv2.createTrackbar('S_low', window_name, 0, 255, nothing)
    cv2.createTrackbar('V_low', window_name, 0, 255, nothing)
    cv2.createTrackbar('H_high', window_name, 179, 179, nothing)
    cv2.createTrackbar('S_high', window_name, 255, 255, nothing)
    cv2.createTrackbar('V_high', window_name, 255, 255, nothing)

def HSV_picker(video_path):
    cap = cv2.VideoCapture(video_path)
    cv2.namedWindow('Trackbars')
    create_trackbars('Trackbars')

    pause = False

    while True:
        if not pause:
            ret, frame = cap.read()
            if not ret:
                break

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        h_low, s_low, v_low, h_high, s_high, v_high = [cv2.getTrackbarPos(pos, 'Trackbars') for pos in
                                                       ['H_low', 'S_low', 'V_low', 'H_high', 'S_high', 'V_high']]

        lower_color = np.array([h_low, s_low, v_low])
        upper_color = np.array([h_high, s_high, v_high])

        mask = cv2.inRange(hsv, lower_color, upper_color)
        cv2.imshow('Frame', frame)
        cv2.imshow('Mask', mask)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        if key == ord(' '):  # Space to toggle pause
            pause = not pause

    cap.release()
    cv2.destroyAllWindows()

    return lower_color, upper_color

if __name__ == "__main__":
    # Example usage when run as a script
    video_path = '/Users/jiahaozh/Downloads/IMG_7142.MOV'
    lower_color, upper_color = HSV_picker(video_path)
    print(f"Lower HSV: {lower_color}, Upper HSV: {upper_color}")
