#!/usr/bin/env python
from setuptools import setup
with open('requirements.txt') as f:
    requirements = f.read().splitlines()


setup(name='gym_xmoto',
      version='0.0.1',
      install_requires=requirements,
      )
