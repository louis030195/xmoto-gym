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

  ```
  pip install -e .
  pip install -e batch-ppo-master
  ```

  # Usage

  open Xmoto set config at 800x600
  Move Xmoto exactly at top left corner

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

	Second one : 
	```
	docker run -p 5901:5900 <image hash>
	vncviewer localhost:5901
	```

