#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name='gym_xmoto',
      version='0.0.9',
      description='OpenAi\'s gym environment for Xmoto game - reinforcement learning research',
      url='https://github.com/louis030195/xmoto-gym',
      author='Louis Beaumont',
      author_email='louis.beaumont@gmail.com',
      packages=find_packages(),
      install_requires=['numpy',
			'pandas',
			'opencv-python',
			'pyautogui',
			'gym',
			'python3_xlib',
			'matplotlib',
			'seaborn',
			'mss',
			'imutils'],
      include_package_data=True,
      )
