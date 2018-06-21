#!/usr/bin/env python
# -*- coding: utf-8 -*-


# core modules
import logging.config
import math
import pkg_resources
import random
import pyautogui
# 3rd party modules
from gym import spaces
import gym
import numpy as np
import subprocess
from capturedata import capturedata



class XmotoEnv(gym.Env):

  def __init__(self):


    self.viewer = None

    # WASD SPACE ENTER
    self.action_space = spaces.Discrete(6)
    self.observation_space = Box(0, 255, [720, 480, 3]) # yolo ????

    for a in self.action_space:
      print("Action : " + str(a))



"""
    bashCommand = "./xmoto"

    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
"""

    #self.reset()


  def step(self, action):
    """
    The agent takes a step in the environment.
    Parameters
    ----------
    action : int
    Returns
    -------
    ob, reward, episode_over, info : tuple
        ob (object) :
            an environment-specific object representing your observation of
            the environment.
        reward (float) :
            amount of reward achieved by the previous action. The scale
            varies between environments, but the goal is always to increase
            your total reward.
        episode_over (bool) :
            whether it's time to reset the environment again. Most (but not
            all) tasks are divided up into well-defined episodes, and done
            being True indicates the episode has terminated. (For example,
            perhaps the pole tipped too far, or you lost your last life.)
        info (dict) :
             diagnostic information useful for debugging. It can sometimes
             be useful for learning (for example, it might contain the raw
             probabilities behind the environment's last state change).
             However, official evaluations of your agent are not allowed to
             use this for learning.
    """


    anyaction(action)
    reward = -0.01 # TODO : If dead mean reward ...

    episode_over = False
    # TODO : Detect when end screen appear and return as episode_over
    return self.obs, reward, episode_over, {}


  def reset(self):
    return anyaction('\n')



    # DRIVE -------------------------

    def accelerate():
        pyautogui.keyDown('W')

    def liftfront():
        pyautogui.keyDown('A')

    def liftback():
        pyautogui.keyDown('D')

    def brake():
        pyautogui.keyDown('S')

    def anyaction(key):
        pyautogui.keyUp(key)
        pyautogui.keyUp(key)

    #  -------------------------


  def get_keys_to_action(self):
    KEYWORD_TO_KEY = {
        'ADVANCE':      ord('w'),
        'BRAKE':    ord('s'),
        'LEFT':    ord('a'),
        'RIGHT':   ord('d'),
        'SPACE':    ord(' '),
        'RESET':   ord('\n'),

    }

    keys_to_action = {}

    for action_id, action_meaning in enumerate(self.get_action_meanings()):
        keys = []
        for keyword, key in KEYWORD_TO_KEY.items():
            if keyword in action_meaning:
                keys.append(key)
        keys = tuple(sorted(keys))

        assert keys not in keys_to_action
        keys_to_action[keys] = action_id

    return keys_to_action
