# Displacement_Time Drawer for Videos
 ***Color-based object tracker for drawing Object_Displacement vs Time Figure using captured videos.***

## Building Enviroment
Python = 3.9.18\
OpenCV = 4.8.1\
Numpy = 1.26.0\
matplotlib = 3.8.1\
csv = 1.0

## User Guide
Run the _main.py_ to play with your video.

1. Type in video directory:
    > Enter the video path: 

2. Find the HSV values range for the tracked object (Can be skipped if already known):
    > Type 'skip' to skip or press Enter to access HSV picker: 

    Use Trackbars to get the Lower HSV and Upper HSV when use the HSVPicker.
    > 'space' to pause/unpause, 'q' to quit

    Or

    Type in the known HSV values when 'skip':
    > Enter Lower HSV values as H,S,V (e.g. 0,0,0): 
    > Enter Upper HSV values as H,S,V (e.g. 179,255,255): 

3. Find the pixel_to_cm ratio for the video (Can be skipped if already known):
    > Type 'skip' to skip or press Enter to access Pixel-to-cm Ratio picker: 

    Ues mouse input to draw a 10cm line on the first frame of the video when use the PixelToCmRatio.
    > Draw a line of known length (10 cm) on the image. Press 'e' to erase and redraw the line. Press 'c' to confirm.

    Or

    Type in the known pixel_to_cm value when 'skip':
    > Enter the Pixel-to-cm Ratio (e.g. 75.4): 

4. Get the Displacement vs Time plot and the .csv file.
    > Data ready to be saved to CSV file and plotted.

    Name the .csv file:
    > Enter the filename for the CSV (Default: 'displacement_data.csv'): 
