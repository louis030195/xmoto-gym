import numpy as np
import cv2
import os
from numpy import ones,vstack
from numpy.linalg import lstsq
import numpy as np
import pyautogui
import time
import mss
import mss.tools
import math
from math import sqrt


def capturedata(zone, debug=False): #Param to get only screen
    """
    Capture screen data
    Returns
    -------
    new_screen, original_screen

    """
    with mss.mss() as sct:
        # Grab the data
        region = {'top': zone[0], 'left': zone[1], 'width': zone[2], 'height': zone[3]}
        screen = np.array(sct.grab(region))
    if debug:
        cv2.imshow('window', screen)

    return cv2.resize(screen, dsize=(int(zone[2] / 4), int(zone[3] / 4))), screen


def testdata():
    print("Starting capturing data in 3 secs ...")
    time.sleep(3)
    while True:
        capturedata((80, 90, 720, 480), debug=True)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
