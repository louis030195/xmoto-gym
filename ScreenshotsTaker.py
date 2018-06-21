import pyautogui
import time
from numpy import ones,vstack
from numpy.linalg import lstsq

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
"""
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
"""
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

def draw_ground(img, lines, color=[0, 255, 255], thickness=3):

    # if this fails, go with some default line
    try:

        # finds the maximum y value for a ground marker
        # (since we cannot assume the horizon will always be at the same point.)

        ys = []
        for i in lines:
            for ii in i:
                ys += [ii[1],ii[3]]
        min_y = min(ys)
        max_y = 500
        new_lines = []
        line_dict = {}

        for idx,i in enumerate(lines):
            for xyxy in i:
                # These four lines:
                # modified from http://stackoverflow.com/questions/21565994/method-to-return-the-equation-of-a-straight-line-given-two-points
                # Used to calculate the definition of a line, given two sets of coords.
                x_coords = (xyxy[0],xyxy[2])
                y_coords = (xyxy[1],xyxy[3])
                A = vstack([x_coords,ones(len(x_coords))]).T
                m, b = lstsq(A, y_coords)[0]

                # Calculating our new, and improved, xs
                x1 = (min_y-b) / m
                x2 = (max_y-b) / m

                line_dict[idx] = [m,b,[int(x1), min_y, int(x2), max_y]]
                new_lines.append([int(x1), min_y, int(x2), max_y])

        final_ground = {}

        for idx in line_dict:
            final_ground_copy = final_ground.copy()
            m = line_dict[idx][0]
            b = line_dict[idx][1]
            line = line_dict[idx][2]

            if len(final_ground) == 0:
                final_ground[m] = [ [m,b,line] ]

            else:
                found_copy = False

                for other_ms in final_ground_copy:

                    if not found_copy:
                        if abs(other_ms*1.2) > abs(m) > abs(other_ms*0.8):
                            if abs(final_ground_copy[other_ms][0][1]*1.2) > abs(b) > abs(final_ground_copy[other_ms][0][1]*0.8):
                                final_ground[other_ms].append([m,b,line])
                                found_copy = True
                                break
                        else:
                            final_ground[m] = [ [m,b,line] ]

        line_counter = {}

        for ground in final_ground:
            line_counter[ground] = len(final_ground[ground])

        top_ground = sorted(line_counter.items(), key=lambda item: item[1])[::-1][:2]

        ground1_id = top_ground[0][0]
        ground2_id = top_ground[1][0]

        def average_ground(ground_data):
            x1s = []
            y1s = []
            x2s = []
            y2s = []
            for data in ground_data:
                x1s.append(data[2][0])
                y1s.append(data[2][1])
                x2s.append(data[2][2])
                y2s.append(data[2][3])
            return int(np.mean(x1s)), int(np.mean(y1s)), int(np.mean(x2s)), int(np.mean(y2s))

        l1_x1, l1_y1, l1_x2, l1_y2 = average_ground(final_ground[ground1_id])
        l2_x1, l2_y1, l2_x2, l2_y2 = average_ground(final_ground[ground2_id])

        return [l1_x1, l1_y1, l1_x2, l1_y2], [l2_x1, l2_y1, l2_x2, l2_y2]
    except Exception as e:
        print(str(e))

def process_img(original_image):
    processed_img = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    processed_img = cv2.Canny(processed_img, threshold1=200, threshold2=300)

    vertices = np.array([[10,450],[10,250],[300,250],[480,250],[720,250],[720,450],
                         ], np.int32)
    processed_img = cv2.GaussianBlur(processed_img,(5,5),0)
    processed_img = roi(processed_img, [vertices])


    # more info: http://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_houghlines/py_houghlines.html
    #                          edges       rho   theta   thresh         # min length, max gap:
    lines = cv2.HoughLinesP(processed_img,1,np.pi/180, 80,20,15)
    #draw_lines(processed_img,lines)
    try:
        l1, l2 = draw_ground(original_image,lines)
        cv2.line(original_image, (l1[0], l1[1]), (l1[2], l1[3]), [0,255,0], 30)
        cv2.line(original_image, (l2[0], l2[1]), (l2[2], l2[3]), [0,255,0], 30)
    except Exception as e:
        print(str(e))
        pass
    try:
        for coords in lines:
            coords = coords[0]
            try:
                cv2.line(processed_img, (coords[0], coords[1]), (coords[2], coords[3]), [255,0,0], 3)


            except Exception as e:
                print(str(e))
    except Exception as e:
        pass

    return processed_img,original_image

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

            # resize to something a bit more acceptable for a CNN
            #screen = cv2.resize(screen, (360,240))
            # run a color convert:
            #screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)

            #keys = key_check()
            #output = keys_to_output(keys)
            #training_data.append([screen,output])

            #pyautogui.keyDown('w')
            #pyautogui.keyUp('w')


            print('Frame took {} seconds'.format(time.time()-last_time))
            last_time = time.time()
            new_screen,original_image = process_img(screen)
            cv2.imshow('window', new_screen)
            cv2.imshow('window2',cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB))

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
