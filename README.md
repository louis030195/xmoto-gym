# Xmoto AI

OpenAi Gym with Xmoto !

https://github.com/openai/gym


# Version 0
[Video](https://www.youtube.com/watch?v=ks1ci2bMIiY&feature=youtu.be)


# Actions
 - W = ADVANCE
 - A = LIFT FRONT WHEEL
 - S = BRAKE
 - D = LIFT BACK WHEEL
 - SPACE = change direction
 - ENTER = reset

  # Observations
  - Screen pixels (720x480x3) 

  # Rewards
  - Positive advancing
  - Negative every frame to speed up
  - Positive when winning
  - Negative when losing



  # Installation
  
  ```
  sudo apt-get install scrot 
  virtualenv env --python=python3
  . env/bin/activate
  pip install -e .
  ```

  # Usage

  python -m dqn2

  ```

  import gym
  import gym_xmoto

  env = gym.make('Xmoto-v0')

  ```
