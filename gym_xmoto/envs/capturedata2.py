import numpy as np
import cv2
import os
from numpy import ones,vstack
from numpy.linalg import lstsq
import numpy as np
import pyautogui
import time
from math import sqrt

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
                m, b = lstsq(A, y_coords, rcond = None)[0]

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

        return [l1_x1, l1_y1, l1_x2, l1_y2], [l2_x1, l2_y1, l2_x2, l2_y2], ground1_id, ground2_id
    except Exception as e:
        print(str(e))

def process_img(original_image):
    processed_img = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    processed_img = cv2.Canny(processed_img, threshold1=200, threshold2=300)

    vertices = np.array([[10,450],[10,250],[300,250],[480,250],[720,250],[720,450],
                         ], np.int32)
    processed_img = cv2.GaussianBlur(processed_img,(5,5),0)
    #processed_img = roi(processed_img, [vertices])
    return processed_img, original_image

    # more info: http://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_houghlines/py_houghlines.html
    #                          edges       rho   theta   thresh         # min length, max gap:
    #lines = cv2.HoughLinesP(processed_img,1,np.pi/180, 80,20,15)
    #draw_lines(processed_img,lines)
    """
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
"""

def capturedata(zone):
    """
    Capture screen data
    Returns
    -------
    new_screen, original_screen, m1, m2
        zz
        zz
        zz
        zz

    """
    screen = np.array(pyautogui.screenshot(region=zone))
    screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
    #new_screen,original_image = process_img(screen)
    found1, found2 = False, False
    appleX, appleY = 0, 0
    bikeX, bikeY = 0, 0
    dist = 0



    for y in range(119):
        for x in range(99):
            [r, g, b] = screen[x, y]
            if (r == 0 and g == 0 and b == 255) and not found1:
                appleX, appleY = x, y
                found1 = True
            if (r == 104 and g == 238 and b == 255) and not found2:
                bikeX, bikeY = x, y
                found2 = True
            if found1 and found2:
                break
    try:#sometimes math error ??
        dist = sqrt((appleX - bikeX)^2 + (appleY - bikeY)^2)
    except ValueError:
        print ("Oops!  That was no valid number.  Try again...")
# NEED TO FIX THAT DETECT HIS OWN POSITION
    print("distance to apple :" + str(dist))

    return dist, screen


def testdata():
    print("Starting capturing data in 5 secs ...")
    time.sleep(5)

    last_time = time.time()
    while True:
        #s1, s2 = capturedata((200,200,200,200))
        s3, s4 = capturedata((80,550,120,100)) # Map size
        s4 = cv2.cvtColor(s4, cv2.COLOR_BGR2RGB)
        print('Frame took {} seconds'.format(time.time()-last_time))
        last_time = time.time()
        #cv2.imshow('window', s1)

        cv2.imshow('window3', s4)

        #print("distance to apple :" + str(dist))

        """
        for index, color in enumerate(s4):
            print(color)

        for index, color in enumerate(s4[3]):
            if ((color == [255,0,0]).any() and not found1):
                print(index)
                apple = index
                found1 = True
            if ((color == [255,238,104]).any() and not found2):
                print(index)
                found2 = True
                bike = index
            if found1 and found2:
                break

        print("distance to apple :" + str(apple - bike))
"""
        #cv2.circle(s4,(50,50),50,(255,0,0),-1)
        #cv2.imshow('window2',cv2.cvtColor(s2, cv2.COLOR_BGR2RGB))

        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
