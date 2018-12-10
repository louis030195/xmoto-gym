import gym
import gym_xmoto
from gym_xmoto.envs.utils import capture_screen
import cv2
import time
import mss
import numpy as np

from score_classification import extract_digits

def capture_score_data(different_level=50, same_score=10):
    """
    This method is used to capture data about different score images (top left corner)
    """
    env = gym.make("Xmoto-v0")
    env.render()
    
    for i in range(0, different_level): # Capture multiple scores images (wrench, apple ...) 
        for j in range(0, same_score): # Capture multiple images of the same score because it's often moving
            (resized_screen, original_screen) = capture_screen((85, 195 , 30, 30))
            mss.tools.to_png(original_screen.rgb, original_screen.size, output='score_data/score' + str(i) + '_' + str(j) + '.png')
            time.sleep(2)
        env.next_level()


def color_detection():

    #env = gym.make("Xmoto-v0")
    #env.render()

    #time.sleep(2)

    (resized_screen, original_screen) = capture_screen((85, 195 , 30, 30))

    original_screen = np.array(original_screen)


    # Converts images from BGR to HSV 
    hsv = cv2.cvtColor(original_screen, cv2.COLOR_BGR2HSV) 
    lower_red = np.array([20,100,100]) 
    upper_red = np.array([30,255,255]) 

    # Here we are defining range of bluecolor in HSV 
    # This creates a mask of blue coloured  
    # objects found in the frame. 
    mask = cv2.inRange(hsv, lower_red, upper_red) 
    
    # The bitwise and of the frame and mask is done so  
    # that only the blue coloured objects are highlighted  
    # and stored in res 
    res = cv2.bitwise_and(original_screen, original_screen, mask= mask) 
    #cv2.imshow('frame',original_screen) 
    #cv2.imshow('mask',mask) 
    #cv2.imshow('res',res) 

    # This displays the frame, mask  
    # and res which we created in 3 separate windows. 
    #k = None
    #while k != 27:
    #    k = cv2.waitKey(5) & 0xFF
    
    # Destroys all of the HighGUI windows. 
    #cv2.destroyAllWindows()

    cv2.imwrite('score_data/7.png', mask)


if __name__ == "__main__":
    #capture_score_data()
    img = cv2.imread('score_data/score0_2.png',0)
    print(img.shape)#img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    print(len(extract_digits(img)))