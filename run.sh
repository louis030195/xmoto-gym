Xvfb :99 -screen 0 1024x768x24 +extension GLX +render -noreset &
x11vnc -forever -display :99 &
DISPLAY=:99 /usr/games/xmoto -l tut1 #python xmoto-gym/example.py
