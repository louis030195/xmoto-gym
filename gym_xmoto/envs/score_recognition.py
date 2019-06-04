
from gym_xmoto.envs.image_preprocessor import preprocess_image
import os
import cv2
import numpy as np

def recognize_score_with_filename(image_filename):
    try:
        return recognize_score(cv2.imread(image_filename, cv2.IMREAD_COLOR))
    except:
        return ""

def recognize_score(image):
    score = ""
    score_digits = preprocess_image(image)

    for score_digit in score_digits:
        for (digit_file_name, digit_image) in digits:
            try:
                res = cv2.matchTemplate(score_digit, digit_image, cv2.TM_CCOEFF_NORMED)
                threshold = 0.8
                if len(np.where( res >= threshold)[0]) > 0:
                    score = score + digit_file_name
                    break
            except:
                pass
        #cv2.imshow("", score_digit)
        #cv2.waitKey(3000)
    return score

def recognize_score_ml(image):
    pass

def train_score():
    pass