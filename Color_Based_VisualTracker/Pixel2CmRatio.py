import cv2
import numpy as np

class PixelToCmRatio:
    def __init__(self, video_path):
        self.video_path = video_path
        self.drawing = False
        self.line_drawn = False
        self.ix, self.iy = -1, -1
        self.ex, self.ey = -1, -1
        self.frame_copy = None

    def draw_line(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            if not self.drawing:
                self.drawing = True
                self.ix, self.iy = x, y
            else:
                self.drawing = False
                self.line_drawn = True
                self.ex, self.ey = x, y
                cv2.line(self.frame, (self.ix, self.iy), (self.ex, self.ey), (0, 255, 0), 2)

        elif event == cv2.EVENT_MOUSEMOVE:
            if self.drawing:
                temp_frame = self.frame_copy.copy()
                cv2.line(temp_frame, (self.ix, self.iy), (x, y), (0, 255, 0), 2)
                cv2.imshow('image', temp_frame)

    def get_ratio(self):
        cap = cv2.VideoCapture(self.video_path)
        ret, self.frame = cap.read()

        if not ret:
            print("Failed to capture video")
            cap.release()
            return None

        self.frame_copy = self.frame.copy()
        cv2.namedWindow('image')
        cv2.setMouseCallback('image', self.draw_line)

        while True:
            cv2.imshow('image', self.frame)

            k = cv2.waitKey(1) & 0xFF
            if k == ord('e'):  # 'e' to erase and redraw the line
                self.frame = self.frame_copy.copy()
                self.line_drawn = False
            elif k == ord('c') and self.line_drawn:  # 'c' to confirm and exit
                break

        cap.release()
        cv2.destroyAllWindows()

        if not self.line_drawn:
            return None

        # Calculate the pixels/cm ratio
        pixels_length = np.sqrt((self.ix - self.ex)**2 + (self.iy - self.ey)**2)
        return pixels_length / 10.0  # Assuming 10.0 cm as the known length

if __name__ == "__main__":
    print("Draw a line of known length (10 cm) on the image. Press 'e' to erase and redraw the line. Press 'c' to confirm.")
    video_path = input("Enter video path for Pixel-to-Cm Ratio calculation: ")
    pixel_to_cm_ratio = PixelToCmRatio(video_path)
    ratio = pixel_to_cm_ratio.get_ratio()
    if ratio is not None:
        print(f"Pixel-to-cm ratio: {ratio} pixels/cm")
