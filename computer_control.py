import pyautogui
import time

print("Automation starting in 5 seconds...")
time.sleep(5)

pyautogui.moveTo(500,300)
pyautogui.click()

pyautogui.write("Hello Gowtham")

pyautogui.press("enter")