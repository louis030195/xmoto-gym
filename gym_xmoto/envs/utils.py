import numpy as np
import cv2
#import pyautogui
import time
import mss
import mss.tools
import subprocess

def get_window_infos(name):
    output = subprocess.check_output(["xwininfo", "-name", name], universal_newlines=True)

    properties = {}
    for line in output.split("\n"):
        if ":" in line:
            parts = line.split(":",1)
            properties[parts[0].strip()] = parts[1].strip()

    x = int(properties['Absolute upper-left X'])
    y = int(properties['Absolute upper-left Y'])
    w = int(properties['Width'])
    h = int(properties['Height'])

    return x, y, w, h

def capture_screen(debug=False):
    """
    Capture screen
    Returns
    -------
    resized screen, original size screen

    """
    x, y, w, h = get_window_infos("0.5.11")

    with mss.mss() as sct:
        region = {'top': y,
         'left': x,
         'width': w,
         'height': h}
        screen = np.array(sct.grab(region))
    if debug:
        cv2.imshow('window', screen)


    return cv2.resize(screen, dsize=(150, 200)), screen

def test_capture_screen():
    print("Starting capturing data in 3 secs ...")
    time.sleep(3)
    while True:
        capture_screen(debug=True)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
