import pyautogui
import time
import pickle

# Initialize empty list to store recorded actions
recorded_actions = []
KEY_PRESS = 'keypress'
KEY_RELEASE ='keyrelease'
CLICK = 'click'
DOUBLE_CLICK = 'double_click'
RELEASE ='release'
SCROLL = 'scroll'
DRAG = 'drag'

# Function to replay recorded actions
def actions_to_script(recorded_actions):
    script = list()
    # Save recorded actions to a Python script file
    script.append("import pyautogui\n")
    script.append("import time\n")
    script.append("\n")
    script.append("time.sleep(2)\n")  # Delay before replay starts, adjust as needed
    for action in recorded_actions:
        if action[0] == KEY_PRESS:
            script.append(f"pyautogui.press('{action[1]}', presses=1, interval=0.0)\n")
        elif action[0] == KEY_RELEASE:
            script.append(f"pyautogui.keyUp('{action[1]}')\n")
        elif action[0] == CLICK:
            script.append(f"pyautogui.click({action[1]}, {action[2]})\n")
        elif action[0] == 'double_click':
            script.append(f"pyautogui.doubleClick({action[1]}, {action[2]})\n")
        elif action[0] == RELEASE:
            script.append(f"pyautogui.mouseUp({action[1]}, {action[2]})\n")
        elif action[0] == SCROLL:
            script.append(f"pyautogui.scroll({action[1]}, {action[2]})\n")
        elif action[0] == DRAG:
            script.append(f"pyautogui.moveTo({action[1]}, {action[2]})\n")
            script.append(f"pyautogui.mouseDown()\n")
            script.append(f"pyautogui.moveRel({action[3]}, {action[4]})\n")
            script.append(f"pyautogui.mouseUp()\n")
    script.append("\n")
    return script