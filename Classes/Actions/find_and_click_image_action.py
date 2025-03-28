import pyautogui
import random
import time
import numpy as np
from pynput.mouse import Controller, Button
from termcolor import colored
import cv2
from Actions.action import Action
from image_finder import ImageFinder
from window_handler import WindowHandler


mouse = Controller()

def bezier_curve(points, num_points=20):
    """Генерирует точки кривой Безье."""
    n = len(points) - 1
    curve_points = []
    for t in [i / (num_points - 1) for i in range(num_points)]:
        x = 0
        y = 0
        for i, p in enumerate(points):
            b = binomial_coefficient(n, i) * (1 - t) ** (n - i) * t ** i
            x += p[0] * b
            y += p[1] * b
        curve_points.append((x, y))
    return curve_points

def binomial_coefficient(n, k):
    """Вычисляет биномиальный коэффициент."""
    if k < 0 or k > n:
        return 0
    if k == 0 or k == n:
        return 1
    if k > n // 2:
        k = n - k
    res = 1
    for i in range(k):
        res = res * (n - i) // (i + 1)
    return res

def move_mouse_pynput(start_x, start_y, end_x, end_y, duration):
    """Перемещает мышь с помощью pynput."""
    control_points = [
        (start_x, start_y),
        (start_x + random.randint(-100, 100), start_y + random.randint(-50, 50)),
        (end_x + random.randint(-100, 100), end_y + random.randint(-50, 50)),
        (end_x, end_y),
    ]
    curve_points = bezier_curve(control_points, num_points=100)
    start_time = time.time()
    for point in curve_points:
        current_time = time.time() - start_time
        if current_time > duration:
            break
        x, y = point
        mouse.position = (int(x), int(y))
        time.sleep(duration / len(curve_points))
    return end_x, end_y

class FindAndClickImageActionMouse(Action):
    def __init__(self, image: str, offset_x=0, offset_y=0, delay=0.2, retard=0, max_matches=0, move_mouse=True):
        self.delay = delay
        self.image_finder = ImageFinder()
        self.image = image
        self.max_matches = max_matches
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.window_handler = WindowHandler()
        self.window_title = 'BlueStacks App Player 3'
        self.move_mouse = move_mouse
        self.retard = retard

    def execute(self):
        try:
            print(colored(f"Finding image: {self.image}", "yellow"))
            screenshot, win = self.window_handler.screenshot_window(self.window_title)
            best_scale, best_loc, num_matches, best_max_val, target_image, screenshot_cv = self.image_finder._match_image(self.image, screenshot)
            if best_max_val >= self.image_finder.threshold:
                rects = np.array([(pt[0], pt[1], pt[0] + target_image.shape[1] * best_scale[0], pt[1] + target_image.shape[0] * best_scale[1]) for pt in best_loc])
                pick = ImageFinder.non_max_suppression_fast(rects, 0.3)
                for (startX, startY, endX, endY) in pick:
                    cv2.rectangle(screenshot_cv, (int(startX), int(startY)), (int(endX), int(endY)), (255,0,255), 2)
                    center_x = int(startX + (endX - startX) // 2 + win.left)
                    center_y = int(startY + (endY - startY) // 2 + win.top)
                    start_x, start_y = pyautogui.position()
                    if self.move_mouse:
                        end_x, end_y = move_mouse_pynput(start_x, start_y, center_x + self.offset_x, center_y + self.offset_y, duration=self.delay) 
                        #end_x, end_y = move_mouse_pynput(start_x, start_y, center_x + self.offset_x, center_y + self.offset_y, duration=self.delay) # Используем self.delay
                    else:
                        pyautogui.moveTo(center_x + self.offset_x, center_y + self.offset_y)
                        end_x, end_y = center_x + self.offset_x, center_y + self.offset_y
                    time.sleep(0.3)
                    offset_click_x = random.randint(-5, 5)
                    offset_click_y = random.randint(-5, 5)
                    mouse.click(Button.left)
                    print(colored(f"found {self.image} {len(pick)}x at {best_max_val}%", "green"))
                    if len(pick) >= self.max_matches and self.max_matches != 0:
                        return False
                    if len(pick) < self.max_matches and self.max_matches != 0:
                        return True
                    return True
            else:
                print(colored(f"Image {self.image} not found.", "red"))
                return False
        except Exception as e:
            print(colored(f"Error clicking image {self.image}: {e}", "red"))
            return False
        
class FindAndClickImageAction(Action):
    def __init__(self, image: str,offset_x= 0, offset_y= 0, delay=0.2, retard=0, max_matches=0 ):
        
        self.delay = delay
        self.image_finder = ImageFinder()
        self.image = image
        self.max_matches = max_matches
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.window_handler = WindowHandler()
        self.window_title = 'BlueStacks App Player 3'
        self.retard = retard

    def execute(self):
        screenshot, win = self.window_handler.screenshot_window(self.window_title)
        break_action_group = self.image_finder.find_and_click_image(self.image, screenshot, win, self.offset_x, self.offset_y, self.max_matches)
        return break_action_group