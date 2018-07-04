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

  # States
  - Dead = Detect when dead screen
  - Win = Detect win screen

  # Observations
  I use the minimap pixels, why not ?
  Atm only 1 observation : distance from bike to objective(apple)
  then :
  - Direction : the longest distance between bike and minimap edge is the direction.
  - How many objectives left (top left screen)

  # Rewards
  - Positive when bike is getting closer to objectives(apples)
  - Negative every frame to speed up
  - Positive when winning
  - Negative when losing
  TODO :
   - Positive when getting apple
   ...



  # After updating pip package
  python3 setup.py sdist bdist_wheel
  then pip install -e .

  # Usage

  ```

  import gym
  import gym_xmoto

  env = gym.make('Xmoto-v0')

  ```
