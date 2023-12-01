import numpy as np
from Color2Track import HSVPicker
from Pixel2CmRatio import PixelToCmRatio
from VideoTracker import VideoTracker

def main():
    video_path = input("Enter the video path: ")

    # HSV range selection
    hsv_choice = input("Type 'skip' to skip or press Enter to access HSV picker: ")
    if hsv_choice.lower() != 'skip':
        print("'space' to pause/unpause, 'q' to quit")
        hsv_picker = HSVPicker(video_path)
        lower_hsv, upper_hsv = hsv_picker.pick_hsv()
    else:
        # Enter previously known HSV values
        lower_hsv_values = input("Enter Lower HSV values as H,S,V (e.g. 0,0,0): ").split(',')
        upper_hsv_values = input("Enter Upper HSV values as H,S,V (e.g. 179,255,255): ").split(',')
        lower_hsv = np.array([int(val) for val in lower_hsv_values])
        upper_hsv = np.array([int(val) for val in upper_hsv_values])
    
    if lower_hsv is not None and upper_hsv is not None:
        print(f"Lower HSV: {lower_hsv}, Upper HSV: {upper_hsv}")

    # Pixel-to-cm ratio selection
    ratio_choice = input("Type 'skip' to skip or press Enter to access Pixel-to-cm Ratio picker: ")
    if ratio_choice.lower() != 'skip':
        print("Draw a line of known length (10 cm) on the image. Press 'e' to erase and redraw the line. Press 'c' to confirm.")
        pixel_to_cm_ratio_picker = PixelToCmRatio(video_path)
        pixel_to_cm_ratio = pixel_to_cm_ratio_picker.get_ratio()
    else:
        # Enter previously known pixel-to-cm ratio
        pixel_to_cm_ratio = float(input("Enter the Pixel-to-cm Ratio (e.g. 75.4): "))

    if pixel_to_cm_ratio is not None:
        print(f"Pixel-to-cm ratio: {pixel_to_cm_ratio} pixels/cm")

    # Video tracking
    tracker = VideoTracker(video_path, /Users/jiahaozh/Downloads/Test.MOV, upper_hsv, pixel_to_cm_ratio)
    times, displacements = tracker.track_object()

    print("Data ready to be saved to CSV file and plotted.")
    tracker.plot_data(times, displacements)

    csv_filename = input("Enter the filename for the CSV (Default: 'displacement_data.csv'): ")
    if not csv_filename:
        csv_filename = "displacement_data.csv"
    tracker.save_to_csv(times, displacements, filename=csv_filename)

if __name__ == "__main__":
    main()
