# Xmoto AI

OpenAi Gym with Xmoto !

[![xmoto-gym](https://img.youtube.com/vi/GL6iTVeh19I/0.jpg)](https://www.youtube.com/watch?v=GL6iTVeh19I)


# Actions
 - W = ADVANCE
 - A = LIFT FRONT WHEEL
 - S = BRAKE
 - D = LIFT BACK WHEEL
 - SPACE = change direction
 - NA = no action

  # Observations
  - Screen pixels (720,480,3) resized to (180,120,3)



  # Installation

  ```
  git clone https://github.com/louis030195/xmoto-gym.git
  cd xmoto-gym
  pip install -e .
  pip install -e batch-ppo-master
  sudo apt-get install faketime
  sudo apt-get install xmoto
  ```

  # Usage

  With DQN

  ```
  python dqn.py
  ```

  With PPO

  ```
  python3 -m batch-ppo-master.agents.scripts.train --config=xmoto --noenv_processes
  ```


  ## Docker
  ```
	docker build .
	docker run -p 5900:5900 <image hash>
	vncviewer localhost:5900
  ```

  **Second agent:**
  ```
	docker run -p 5901:5900 <image hash>
	vncviewer localhost:5901
  ```

  ...

  ## Roadmap

  - [ ] Distributed training
  - [ ] Multiple algorithms
  - [ ] Reward on hit apple (decrease score)
  - [ ] Try others algorithms

