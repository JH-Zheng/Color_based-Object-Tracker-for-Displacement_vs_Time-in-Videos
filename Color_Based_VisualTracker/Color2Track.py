import cv2
import numpy as np

class HSVPicker:
    def __init__(self, video_path):
        self.video_path = video_path

    def nothing(self, x):
        pass

    def create_trackbars(self, window_name):
        cv2.createTrackbar('H_low', window_name, 0, 179, self.nothing)
        cv2.createTrackbar('S_low', window_name, 0, 255, self.nothing)
        cv2.createTrackbar('V_low', window_name, 0, 255, self.nothing)
        cv2.createTrackbar('H_high', window_name, 179, 179, self.nothing)
        cv2.createTrackbar('S_high', window_name, 255, 255, self.nothing)
        cv2.createTrackbar('V_high', window_name, 255, 255, self.nothing)

    def pick_hsv(self):
        cap = cv2.VideoCapture(self.video_path)
        cv2.namedWindow('Trackbars')
        self.create_trackbars('Trackbars')
        pause = False

        while True:
            if not pause:
                ret, frame = cap.read()
                if not ret:
                    break

            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            h_low, s_low, v_low, h_high, s_high, v_high = [cv2.getTrackbarPos(pos, 'Trackbars') for pos in
                                                           ['H_low', 'S_low', 'V_low', 'H_high', 'S_high', 'V_high']]

            lower_hsv = np.array([h_low, s_low, v_low])
            upper_hsv = np.array([h_high, s_high, v_high])

            mask = cv2.inRange(hsv, lower_hsv, upper_hsv)
            cv2.imshow('Frame', frame)
            cv2.imshow('Mask', mask)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            if key == ord(' '):  # Space to toggle pause
                pause = not pause

        cap.release()
        cv2.destroyAllWindows()

        return lower_hsv, upper_hsv

if __name__ == "__main__":
    print("'space' to pause/unpause, 'q' to quit")
    video_path = input("Enter video path for HSV Picker: ")
    hsv_picker = HSVPicker(video_path)
    lower_hsv, upper_hsv = hsv_picker.pick_hsv()
    print(f"Lower HSV: {lower_hsv}, Upper HSV: {upper_hsv}")