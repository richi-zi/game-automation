import pyautogui
import time

time.sleep(2)

try:
    pos = pyautogui.locateOnScreen(
        "pic/start.png",confidence=0.8
    )
except pyautogui.ImageNotFoundException:
    pos = None

print("get:",pos)