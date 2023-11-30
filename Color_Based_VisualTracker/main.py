import cv2
import numpy as np
import matplotlib.pyplot as plt
import csv

def track_object(video_path, lower_hsv, upper_hsv, pixel_to_cm_ratio):
    cap = cv2.VideoCapture(video_path)
    origin_position = None
    displacements = []
    times = []

    frame_number = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_hsv, upper_hsv)
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
                displacement_cm = displacement_pixels / pixel_to_cm_ratio
                displacements.append(displacement_cm)
                time_sec = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0  # Convert ms to s
                times.append(time_sec)

        frame_number += 1

    cap.release()
    return times, displacements

def save_to_csv(times, displacements, filename="displacement_data.csv"):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Time (ms)", "Displacement (cm)"])
        for time, displacement in zip(times, displacements):
            writer.writerow([time, displacement])
    print(f"Data saved to {filename}")

def plot_data(times, displacements):
    plt.plot(times, displacements)
    plt.xlabel('Time (ms)')
    plt.ylabel('Displacement (cm)')
    plt.title('Displacement vs Time')
    plt.show()

if __name__ == "__main__":
    video_path = '/Users/jiahaozh/Downloads/IMG_7141.MOV'
    lower_hsv = np.array([0, 109, 99])  # Replace with HSV values [H_low, S_low, V_low]
    upper_hsv = np.array([30, 255, 255])  # Replace with HSV values [H_high, S_high, V_high]
    pixel_to_cm_ratio = 76 # pixel/cm

    times, displacements = track_object(video_path, lower_hsv, upper_hsv, pixel_to_cm_ratio)
    save_to_csv(times, displacements, filename="displacement_data.csv")
    plot_data(times, displacements)
