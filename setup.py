#!/usr/bin/env python
import pathlib
from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()


setup(name='gym_xmoto',
      version='0.0.5',
      description='OpenAi\'s gym environment for Xmoto game - reinforcement learning research',
      url='https://github.com/louis030195/xmoto-gym',
      author='Louis Beaumont',
      author_email='louis.beaumont@gmail.com',
      install_requires=requirements,
      include_package_data=True,
      )
