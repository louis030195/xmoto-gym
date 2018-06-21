from draw_ground import draw_ground
import numpy as np
import cv2
import os

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
"""
"""
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
"""

def roi(img, vertices):
    #blank mask:
    mask = np.zeros_like(img)
    # fill the mask
    cv2.fillPoly(mask, vertices, 255)
    # now only show the area that is the mask
    masked = cv2.bitwise_and(img, mask)
    return masked



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
        l1, l2, m1, m2 = draw_ground(original_image,lines) # Return lanes and their slopes
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

    return processed_img,original_image, m1, m2


def capturedata():
    screen = np.array(pyautogui.screenshot(region=(80,120,720,480)))
    new_screen,original_image, m1, m2 = process_img(screen)
    return new_screen,original_image, m1, m2
    #cv2.imshow('window', new_screen)
    #cv2.imshow('window2',cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB))
