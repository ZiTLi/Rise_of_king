import time
from Actions.action import Action
from window_handler import WindowHandler
import pyautogui

class ManualClickAction(Action):
    def __init__(self,x=50,y=50, delay=0, remember_position=True, retard=0.0):
        self.window_handler = WindowHandler()
        self.delay = delay
        self.window_title = 'BlueStacks App Player 3'
        self.x = x
        self.y = y
        self.remember_position = remember_position
        self.retard = retard



    def execute(self):
        time.sleep(self.delay)
        time.sleep(0.1)
        prev_active_window = pyautogui.getActiveWindow()
        prev_mouse_x, prev_mouse_y = pyautogui.position()
        click_x = int(self.window_handler.get_window(self.window_title).left + self.window_handler.get_window(self.window_title).width * self.x / 100)
        click_y = int(self.window_handler.get_window(self.window_title).top + self.window_handler.get_window(self.window_title).height * self.y / 100)
        pyautogui.click(click_x, click_y)
        prev_active_window.activate()
        if self.remember_position:
            pyautogui.moveTo(prev_mouse_x, prev_mouse_y)
        return True
