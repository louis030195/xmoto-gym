import pyautogui
import time

"""
i = 0
while True:
    time.sleep(0.1) # Delay 1 second.
    pyautogui.screenshot('images/screenshot' + str(i) + '.png')
    print("Screenshot n " + str(i))
    i += 1
    if i == 10000: #10 000 screenshots, enough ?
        break
"""
"""
width, height = pyautogui.size()
print(width,height)
i, j = 0
while i < width:
    while j < height:
        print("Pixel : " + str(i) + "x" + str(j))
        j += 1
    i += 1
#pyautogui.pixelMatchesColor(100, 200, (140, 125, 134), tolerance=10)
"""

import numpy as np
#from grabscreen import grab_screen
import cv2
import time
#from getkeys import key_check
import os
from testkeypress import GetAsyncKeyState

import time

keyList = ["\b"]
for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ 123456789,.'£$/\\":
    keyList.append(char)

def key_check():
    keys = []
    for key in keyList:
        if GetAsyncKeyState(ord(key)):
            keys.append(key)
    return keys

w = [1,0,0,0,0,0,0,0,0]
s = [0,1,0,0,0,0,0,0,0]
a = [0,0,1,0,0,0,0,0,0]
d = [0,0,0,1,0,0,0,0,0]
wa = [0,0,0,0,1,0,0,0,0]
wd = [0,0,0,0,0,1,0,0,0]
sa = [0,0,0,0,0,0,1,0,0]
sd = [0,0,0,0,0,0,0,1,0]
nk = [0,0,0,0,0,0,0,0,1]

starting_value = 1

while True:
    file_name = 'training_data-{}.npy'.format(starting_value)

    if os.path.isfile(file_name):
        print('File exists, moving along',starting_value)
        starting_value += 1
    else:
        print('File does not exist, starting fresh!',starting_value)

        break


def roi(img, vertices):
    #blank mask:
    mask = np.zeros_like(img)
    # fill the mask
    cv2.fillPoly(mask, vertices, 255)
    # now only show the area that is the mask
    masked = cv2.bitwise_and(img, mask)
    return masked

def draw_lines(img,lines):
    for line in lines:
        coords = line[0]
        cv2.line(img, (coords[0], coords[1]), (coords[2], coords[3]), [255,255,255], 3)

def process_img(original_image):
    processed_img = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    processed_img = cv2.Canny(processed_img, threshold1=200, threshold2=300)

    vertices = np.array([[10,450],[10,250],[300,250],[480,250],[720,250],[720,450],
                         ], np.int32)
    processed_img = roi(processed_img, [vertices])


    # more info: http://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_houghlines/py_houghlines.html
    #                          edges       rho   theta   thresh         # min length, max gap:
    #lines = cv2.HoughLinesP(processed_img, 1, np.pi/180, 180,      20,         15)
    #if lines.any() != None:
    #    draw_lines(processed_img,lines)
    return processed_img

def keys_to_output(keys):
    '''
    Convert keys to a ...multi-hot... array
     0  1  2  3  4   5   6   7    8
    [W, S, A, D, WA, WD, SA, SD, NOKEY] boolean values.
    '''
    output = [0,0,0,0,0,0,0,0,0]

    if 'W' in keys and 'A' in keys:
        output = wa
    elif 'W' in keys and 'D' in keys:
        output = wd
    elif 'S' in keys and 'A' in keys:
        output = sa
    elif 'S' in keys and 'D' in keys:
        output = sd
    elif 'W' in keys:
        output = w
    elif 'S' in keys:
        output = s
    elif 'A' in keys:
        output = a
    elif 'D' in keys:
        output = d
    else:
        output = nk
    return output


def main(file_name, starting_value):
    file_name = file_name
    starting_value = starting_value
    training_data = []
    for i in list(range(4))[::-1]:
        print(i+1)
        time.sleep(1)

    last_time = time.time()
    paused = False
    print('STARTING!!!')
    while(True):

        if not paused:
            #screen = grab_screen(region=(0,40,1920,1120))
            screen = np.array(pyautogui.screenshot(region=(80,120,720,480)))
            # origin 90;120 no need useless texts
            new_screen = process_img(screen)
            last_time = time.time()
            # resize to something a bit more acceptable for a CNN
            #screen = cv2.resize(screen, (360,240))
            # run a color convert:
            #screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)

            #keys = key_check()
            #output = keys_to_output(keys)
            #training_data.append([screen,output])

            #print('loop took {} seconds'.format(time.time()-last_time))
            last_time = time.time()
            cv2.imshow('window',cv2.resize(new_screen,(640,360)))
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break

            if len(training_data) % 100 == 0:
                print(len(training_data))

                if len(training_data) == 500:
                    np.save(file_name,training_data)
                    print('SAVED')
                    training_data = []
                    starting_value += 1
                    file_name = '~/Desktop/test/-{}.npy'.format(starting_value)

"""
        keys = key_check()
        if 'T' in keys:
            if paused:
                paused = False
                print('unpaused!')
                time.sleep(1)
            else:
                print('Pausing!')
                paused = True
                time.sleep(1)
"""

main(file_name, starting_value)
