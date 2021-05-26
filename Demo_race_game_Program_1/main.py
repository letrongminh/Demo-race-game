#!/usr/bin/python
import numpy as np
import cv2
import os
from pynput.keyboard import Key, Controller
from helper.color_detection import MultiBackProjectionColorDetector
from helper.mask_analysis import BinaryMaskAnalyser

keyboard = Controller()
# Enable or disable the keyboard simulation (enabled when press 'a')
ENABLE_CAPTURE = False

# use relative path to resources
file_path = os.path.dirname(__file__)
gallery_path = os.path.join(file_path, "gallery")
hand_path = os.path.join(gallery_path, "hand_templates")

# Declare a list and load the templates. If you are using more templates
# then you have to load them here.
template_list = list()
template_list.append(cv2.imread(f"{hand_path}/final_1.png"))
template_list.append(cv2.imread(f"{hand_path}/final_2.png"))
template_list.append(cv2.imread(f"{hand_path}/final_3.png"))
template_list.append(cv2.imread(f"{hand_path}/final_4.png"))

# Open a webcam streaming
video_capture = cv2.VideoCapture(0)
# Reduce the size of the frame to 320x240
video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
# Get the webcam resolution
cam_w = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
cam_h = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
# Declare an offset that is used to define the distance
# from the webcam center of the two red lines
offset = 50

# Declaring the binary mask analyser object
my_mask_analyser = BinaryMaskAnalyser()

# Defining the color detector object
my_back_detector = MultiBackProjectionColorDetector()
my_back_detector.setTemplateList(template_list)  # Set the template

print("Press 'a' to start the hand tracking. Press 'q' to exit.")

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()
    if frame is None:
        break  # check for empty frames

    # Return the binary mask from the back projection algorithm
    frame_mask = my_back_detector.returnMask(
        frame, morph_opening=True, blur=True, kernel_size=5, iterations=2
    )
    if (
            my_mask_analyser.returnNumberOfContours(frame_mask) > 0
            and ENABLE_CAPTURE is True
    ):
        x_center, y_center = my_mask_analyser.returnMaxAreaCenter(frame_mask)
        x_rect, y_rect, w_rect, h_rect = my_mask_analyser.returnMaxAreaRectangle(
            frame_mask
        )
        area = w_rect * h_rect
        cv2.circle(frame, (x_center, y_center), 3, [0, 255, 0], 5)

        # Check the position of the target and press the keys
        if x_center > int(cam_w / 2) + offset and area > 5000:
            keyboard.press(Key.left)
            print("KEY_LEFT")
        elif x_center < int(cam_w / 2) - offset and area > 5000:
            keyboard.press(Key.right)
            print("KEY_RIGHT")
        else:
            print(area)
            print("WAITING")
            keyboard.release(Key.left)
            keyboard.release(Key.right)

    # red line horizontal
    cv2.line(frame, (int(cam_w / 2) - offset, 0), (int(cam_w / 2) - offset, cam_h), [0, 0, 255], 2, )
    cv2.line(frame, (int(cam_w / 2) + offset, 0), (int(cam_w / 2) + offset, cam_h), [0, 0, 255], 2, )

    # Showing the frame and waiting for the exit command
    frame = cv2.flip(frame, 1)
    frame_mask = cv2.flip(frame_mask, 1)
    # cv2.imshow("frame - training", frame)  # show on window
    # cv2.imshow("Mask", frame_mask)  # show on window

    both = np.concatenate((frame, frame_mask), axis=0)
    cv2.imshow('Frame', both)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break  # Exit when Q is pressed
    if cv2.waitKey(33) == ord("a"):
        if ENABLE_CAPTURE is True:
            print("Disabling capture...")
            ENABLE_CAPTURE = False
        else:
            print("Enabling capture...")
            ENABLE_CAPTURE = True
            # exec(open('Race Game.py').read())

# Close the keyboard object

# Release the camera
video_capture.release()
print("Bye")
