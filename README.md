# Xmoto AI

OpenAi Gym with Xmoto !

(Will clean code soon)


# Actions
 - W = ADVANCE
 - A = LIFT FRONT WHEEL
 - S = BRAKE
 - D = LIFT BACK WHEEL
 - SPACE = change direction
 - NA = no action

  # Observations
  - Screen pixels (720x480x3)



  # Installation

  Install [Xmoto](https://xmoto.tuxfamily.org/)

  ```
  git clone https://github.com/louis030195/xmoto-gym.git
  cd xmoto-gym
  pip install -e .
  pip install -e batch-ppo-master
  sudo apt-get install faketime
  ```

  # Usage

  With DQN

  ```
  python dqn.py
  ```

  With PPO (doesn't work atm)

  ```
  python3 -m batch-ppo-master.agents.scripts.train --config=xmoto --noenv_processes
  ```

	## Docker

	```
	docker build .
	docker run -p 5900:5900 <image hash>
	vncviewer localhost:5900
	```

	Second one : 
	```
	docker run -p 5901:5900 <image hash>
	vncviewer localhost:5901
	```

