import time
import threading
from action_sets import ActionSets
from signal_emitter import SignalEmitter
import keyboard
import pygetwindow as gw
from PyQt5.QtCore import pyqtSignal
import importlib

class OSROKBOT:
    def __init__(self, window_title, delay=1):
        
        self.window_title = window_title
        self.delay = delay
        self.stop_event = threading.Event()
        self.signal_emitter = SignalEmitter()
        self.is_running = False
        self.all_threads_joined = True  # New flag
        self.UI = None # New attribute

    def run(self, state_machines):
        self.stop_event.clear()
        self.all_threads_joined = False

        def run_single_machine(machine):
            while not self.stop_event.is_set():
                if self.UI and self.UI.stop_flag:  # Проверка флага stop_flag
                    self.stop()
                    return
                if machine.execute():
                    time.sleep(self.delay)

        threads = [threading.Thread(target=run_single_machine, args=(machine,)) for machine in state_machines]

        for t in threads:
            t.start()

        for t in threads:
            t.join()

        self.all_threads_joined = True
        self.is_running = False

    def start(self, steps):
        if self.is_running or not self.all_threads_joined:
            return

        self.is_running = True
        threading.Thread(target=self.run, args=(steps,)).start()

    def stop(self):
        self.stop_event.set()
        self.is_running = False
        if self.UI: # сброс флага stop_flag
            self.UI.stop_flag = False


