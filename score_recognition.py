
from image_preprocessor import preprocess_image
import os
import cv2
import numpy as np
"""
digits = list()
for digit_file_name in os.listdir('digits'):

    image = cv2.imread('digits/' + digit_file_name, cv2.IMREAD_COLOR)
    digit_image = preprocess_image(image)
    digits.append((digit_file_name[:-4], digit_image[0]))
    """

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
            #print(score_digit.shape, digit_image.shape)
            # TODO: cv2.resize = lose accuracy ???
            #if score_digit.shape[0] <= digit_image.shape[0] or score_digit.shape[1] <= digit_image.shape[1]:
             #   score_digit = cv2.resize(score_digit, dsize=digit_image.shape).T
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