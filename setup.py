#!/usr/bin/env python
import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / 'README.md').read_text()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()


setup(name='gym_xmoto',
      version='0.0.1',
      description='OpenAi\'s gym environment for Xmoto game - reinforcement learning research',
      url='https://github.com/louis030195/xmoto-gym',
      author='Louis Beaumont',
      author_email='louis.beaumont@gmail.com',
      install_requires=requirements,
      )
