# Xmoto AI

![](https://img.shields.io/pypi/v/gym_xmoto.svg?style=flat)

OpenAi Gym with Xmoto !


# Actions
 - W = ADVANCE
 - A = LIFT FRONT WHEEL
 - S = BRAKE
 - D = LIFT BACK WHEEL
 - SPACE = change direction
 - NA = no action

  # Observations
  - Screen pixels (200, 150, 3)



# Installation

```
pip install gym_xmoto
sudo apt-get install faketime
sudo apt-get install xmoto
```

# Usage

Example

```
python example.py
```


## Docker
(Currently doesn't work Seg fault at example in run)
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
- [ ] More observations from Xmoto API
- [ ] Better score detection performance
- [ ] Synchronisation algorithm - faketime
- [ ] Distributed training
- [x] Reward on hit apple (decrease score)

