import cv2
import numpy as np

# Global variables
drawing = False  # True if mouse is pressed
ix, iy = -1, -1  # x and y coordinates for the start of the line
ex, ey = -1, -1  # x and y coordinates for the end of the line
line_drawn = False
frame_copy = None

# Mouse callback function
def draw_line(event, x, y, flags, param):
    global ix, iy, ex, ey, drawing, line_drawn, frame, frame_copy

    if event == cv2.EVENT_LBUTTONDOWN:
        if not drawing:
            drawing = True
            ix, iy = x, y
        else:
            drawing = False
            line_drawn = True
            ex, ey = x, y
            cv2.line(frame, (ix, iy), (ex, ey), (0, 255, 0), 2)

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            temp_frame = frame_copy.copy()
            cv2.line(temp_frame, (ix, iy), (x, y), (0, 255, 0), 2)
            cv2.imshow('image', temp_frame)

def get_pixel_to_cm_ratio(video_path):
    global frame, frame_copy, line_drawn, ix, iy, ex, ey
    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()

    if not ret:
        print("Failed to capture video")
        cap.release()
        return None

    frame_copy = frame.copy()
    cv2.namedWindow('image')
    cv2.setMouseCallback('image', draw_line)

    while True:
        cv2.imshow('image', frame)

        k = cv2.waitKey(1) & 0xFF
        if k == ord('e'):  # 'e' to erase and redraw the line
            frame = frame_copy.copy()
            line_drawn = False
        elif k == ord('c') and line_drawn:  # 'c' to confirm and exit
            break

    cap.release()
    cv2.destroyAllWindows()

    if not line_drawn:
        return None

    # Calculate the pixels/cm ratio
    pixels_length = np.sqrt((ix - ex)**2 + (iy - ey)**2)
    return pixels_length / 10.0  # 10.0 cm


if __name__ == "__main__":
    video_path = '/Users/jiahaozh/Downloads/IMG_7141.MOV'
    ratio = get_pixel_to_cm_ratio(video_path)
    if ratio is not None:
        print(f"Pixel-to-cm ratio: {ratio} pixels/cm")
