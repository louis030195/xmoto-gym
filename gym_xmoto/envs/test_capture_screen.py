from utils import test_capture_screen
import subprocess
subprocess.Popen(["xmoto", "-l", "tut1"])
test_capture_screen((125, 235, 24, 24))
