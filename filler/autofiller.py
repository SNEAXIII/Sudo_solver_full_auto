from time import sleep
import keyboard
import pyautogui

def clicked():
    global nb
    global side
    global enter
    keyboard.press_and_release(nb)
    keyboard.press_and_release(enter)
    keyboard.press_and_release(enter)

nb = {"1": "&", "2": "é", "3": "\"", "4": "'", "5": "(", "6": "-", "7": "è", "8": "_", "9": "ç"}[input("nb : ")]
enter = "enter"
keyboard.press_and_release("alt+tab")



for row in range(9):
    side = "right" if row % 2 == 0 else "left"
    for _ in range(9):
        clicked()
        keyboard.press_and_release(side)
        test = pyautogui.locateCenterOnScreen('replay.png')
        if test is not None:
            sleep(.5)
            pyautogui.click(test)
            sleep(1)
        sleep(.05)
    keyboard.press_and_release("down")
keyboard.press_and_release("left")
for _ in range(7):
    keyboard.press_and_release("up")
clicked()
keyboard.press_and_release("right")
clicked()
keyboard.press_and_release("up")
for _ in range(3):
    clicked()
    keyboard.press_and_release("left")
for _ in range(2):
    keyboard.press_and_release("left")
clicked()
