import numpy as np
import cv2
import pyautogui
import time
import mss
import mss.tools


def capture_screen(zone, debug=False):
    """
    Capture screen
    Returns
    -------
    resized screen, original size screen

    """
    with mss.mss() as sct:
        region = {'top': zone[0], 'left': zone[1], 'width': zone[2], 'height': zone[3]}
        screen = sct.grab(region)
    if debug:
        cv2.imshow('window', screen)

    return cv2.resize(np.array(screen), dsize=(int(zone[2] / 4), int(zone[3] / 4))), screen

def test_capture_screen(zone):
    print("Starting capturing data in 3 secs ...")
    time.sleep(3)
    while True:
        capture_screen(zone, debug=True)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
