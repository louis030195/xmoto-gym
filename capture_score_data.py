import gym
import gym_xmoto
from gym_xmoto.envs.utils import capture_screen
import cv2
import time




def capture_score_data(different_level=50, same_score=10):
    """
    This method is used to capture data about different score images (top left corner)
    """
    env = gym.make("Xmoto-v0")
    env.render()
    
    for i in range(0, different_level): # Capture multiple scores images (wrench, apple ...) 
        for j in range(0, same_score): # Capture multiple images of the same score because it's often moving
            (resized_screen, original_screen) = capture_screen((125, 235, 24, 24))
            #print(original_screen[0])
            time.sleep(2)
            cv2.imwrite('score_data/score' + str(i) + '_' + str(j) + '.png', original_screen)
        env.next_level()



if __name__ == "__main__":
    capture_score_data()