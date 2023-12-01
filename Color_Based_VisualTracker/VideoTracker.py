import cv2
import numpy as np
import matplotlib.pyplot as plt
import csv

class VideoTracker:
    def __init__(self, video_path, lower_hsv, upper_hsv, pixel_to_cm_ratio):
        self.video_path = video_path
        self.lower_hsv = lower_hsv
        self.upper_hsv = upper_hsv
        self.pixel_to_cm_ratio = pixel_to_cm_ratio

    def track_object(self):
        cap = cv2.VideoCapture(self.video_path)
        origin_position = None
        displacements = []
        times = []
        frame_number = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, self.lower_hsv, self.upper_hsv)
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            if contours:
                largest_contour = max(contours, key=cv2.contourArea)
                M = cv2.moments(largest_contour)
                if M['m00'] != 0:
                    cx = int(M['m10'] / M['m00'])
                    cy = int(M['m01'] / M['m00'])
                    current_position = (cx, cy)

                    if frame_number == 0:
                        origin_position = current_position

                    displacement_pixels = np.sqrt((current_position[0] - origin_position[0])**2 + (current_position[1] - origin_position[1])**2)
                    displacement_cm = displacement_pixels / self./Users/jiahaozh/Downloads/Test.MOVpixel_to_cm_ratio
                    displacements.append(displacement_cm)
                    time_sec = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0  # Convert ms to s
                    times.append(time_sec)

            frame_number += 1

        cap.release()
        return times, displacements

    def save_to_csv(self, times, displacements, filename="displacement_data.csv"):
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Time (s)", "Displacement (cm)"])
            for time, displacement in zip(times, displacements):
                writer.writerow([time, displacement])
        print(f"Data saved to {filename}")

    def plot_data(self, times, displacements):   
        plt.plot(times, displacements)
        plt.xlabel('Time (s)')
        plt.ylabel('Displacement (cm)')
        plt.title('Displacement vs Time')
        plt.show()

if __name__ == "__main__":
    video_path = input("Enter video path for Video Tracker: ")

    # Type in the lower and upper HSV values as H, S, V
    lower_hsv = input("Enter lower HSV values as H, S, V (eg. 0, 0, 0): ").split(',')
    upper_hsv = input("Enter upper HSV values as H, S, V (eg. 179, 255, 255): ").split(',')
    lower_hsv = np.array([int(val) for val in lower_hsv])
    upper_hsv = np.array([int(val) for val in upper_hsv])

    # Type in the pixel-to-cm ratio
    pixel_to_cm_ratio = float(input("Enter pixel/cm ratio: "))

    video_tracker = VideoTracker(video_path, lower_hsv, upper_hsv, pixel_to_cm_ratio)
    times, displacements = video_tracker.track_object()
    print("Data ready to be saved to CSV file and plotted.")
    video_tracker.plot_data(times, displacements)
    filename = input("Enter filename for the CSV file: ")
    video_tracker.save_to_csv(times, displacements, filename)