import gym
import gym_xmoto
from gym_xmoto.envs.utils import capture_screen
import cv2
import time
import mss
import numpy as np
import os
import pathlib
from score_recognition import recognize_score_with_filename


def capture_score_data(different_level=50000, same_score=4):
    """
    This method is used to capture data about different score images (top left corner)
    """
    HERE = pathlib.Path(__file__).parent
    env = gym.make("Xmoto-v0")
    env.render()
    
    for i in range(0, different_level): # Capture multiple scores images (wrench, apple ...) 
        for j in range(0, same_score): # Capture multiple images of the same score because it's often moving
            (resized_screen, original_screen) = capture_screen()
            img = original_screen[0:0+30,100:100+30]
            cv2.imwrite(os.path.join(HERE / 'score_data/score', str(i) + '_' + str(j) + '.png'), img)
            time.sleep(1)
        env.next_level()


if __name__ == "__main__":
    HERE = pathlib.Path(__file__).parent

    for score_file_name in sorted(os.listdir('score_data')):
        score = recognize_score_with_filename(os.path.join(HERE / 'score_data/', score_file_name))
        print(score_file_name + " score: " + score)

    #capture_score_data()
    
