import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from action_sets import ActionSets
from OS_ROKBOT import OSROKBOT
import pygetwindow as gw
import time
from window_handler import WindowHandler
from global_vars import GLOBAL_VARS
import threading
import inspect 
from Actions.find_and_click_image_action import FindAndClickImageActionMouse
import time
import threading
from pynput import keyboard


class UI(QtWidgets.QWidget):
    def __init__(self, window_title, delay=0):
        super().__init__()
        
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setAlignment(QtCore.Qt.AlignLeft)
        self.OS_ROKBOT = OSROKBOT(window_title, delay)
        self.start_global_key_listener()
        self.action_sets = ActionSets(OS_ROKBOT=self.OS_ROKBOT)
        self.target_title = window_title
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_position)
        self.timer.start(10)
        # Colors and styles
        self.setStyleSheet("""
        QWidget {
            background-color: #2a2a2a;
        }
        QPushButton {
            background-color: #3a3a3a; 
            color: #f5f5f5;             
            border: 2px solid #4a90e2;  
            border-radius: 8px;
            padding: 5px;
            width: 34px;
            height: 22px;
        }
        QPushButton:hover {
            background-color: #4a4a4a;  
            border: 2px solid #357ab2;  
        }
        QLabel {
            font-size: 16px;
            color: #f5f5f5;
            background-color: transparent;
            text-align: left !important;                
            
            
        }
        QComboBox {
            
            border: 2px solid #4a90e2; 
            border-radius: 8px;
            
            padding: 3px;
            font-size: Auto;
            background-color: #3a3a3a !important;
            color: white !important; /* This sets the text color of non-selected items to white */
        }
        QComboBox::drop-down {
            background-color: #2a2a2a !important;
            border: 2px solid #4a90e2 !important;
            width: 10px;
            border-radius: 5px;
        }
        QComboBox::down-arrow {
            image: url(Media/UI/down_arrow.svg);
            padding-top: 2px;
            width: 10px;
            height: 10px;           
        }
                            

                        
        QCheckBox {
            font-size: 16px;
            color: #f5f5f5;
        }
        
    """)

        # Title Bar
        self.title_bar = QtWidgets.QWidget()
        self.title_bar.setStyleSheet("""
            background-color: #3a3a3a;
            border: none;
        """)
        title_bar_layout = QtWidgets.QHBoxLayout(self.title_bar)
        title_bar_layout.setContentsMargins(0, 0, 0, 0)
        title_bar_layout.setSpacing(0)

        # Title Label
        self.title_label = QtWidgets.QLabel('OSROKBOT')
        self.title_label.setStyleSheet("""
            color: #f5f5f5;
            font-size: 14px;
            font-weight: bold;
            padding-left: 10px;
        """)
        title_bar_layout.addWidget(self.title_label)
        title_bar_layout.addStretch()

        # Close Button
        self.close_button = QtWidgets.QPushButton('x')
        self.close_button.clicked.connect(self.close)
        self.close_button.setStyleSheet("""
            background-color: #3a3a3a;
            color: #f5f5f5;
            border: none;
            font-size: 24px;
            min-width: 5px !important;
            min-height: 5px !important;
            padding: 0px !important;                       
            margin: 0px !important;
        """)
        #make title_bar_layout height 30
        self.title_bar.setFixedHeight(30)
        title_bar_layout.addWidget(self.close_button)

        # Status label
        self.status_label = QtWidgets.QLabel(' Ready!')
        self.status_label.setStyleSheet("color: #4a90e2; font-weight: bold; text-align: left !important;")
        self.status_label.setAlignment(QtCore.Qt.AlignLeft)
        # Button Layout
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setAlignment(QtCore.Qt.AlignLeft)
        # Create the Play Button
        self.play_button = QtWidgets.QPushButton()
        self.play_icon = QtGui.QIcon("Media/UI/play_icon.svg")
        self.play_button.setIcon(self.play_icon)
        self.play_button.setIconSize(QtCore.QSize(24, 24))
        self.play_button.clicked.connect(self.start_automation)
        button_layout.addWidget(self.play_button)

        # Create the Stop Button
        self.stop_button = QtWidgets.QPushButton()
        self.stop_icon = QtGui.QIcon("Media/UI/stop_icon.svg")
        self.stop_button.setIcon(self.stop_icon)
        self.stop_button.setIconSize(QtCore.QSize(24, 24))
        self.stop_button.clicked.connect(self.stop_automation)
        button_layout.addWidget(self.stop_button)


        # Action sets dropdown
        self.action_set_combo_box = QtWidgets.QComboBox()
        self.action_set_combo_box.setStyleSheet("""
            color: #fff;
        """)
        
        self.action_set_names = [
            method_name
            for method_name, method in inspect.getmembers(self.action_sets, predicate=inspect.ismethod)
            if method.__self__ == self.action_sets
            and not method_name.startswith('_')  # Исключаем все методы которые начинаються с "_"
            and method_name not in ('__init__', 'create_machine', 'email_captcha', 'get_action_class')  # Исключаем по списку вручную __init__ и create_machine
        ]
        self.action_set_combo_box.addItems(self.action_set_names)

        # Checkbox for move_mouse
        self.move_mouse_pynput = QtWidgets.QCheckBox("move_mouse")
        self.move_mouse_pynput.setStyleSheet("""
            font-size: 11px;
            background-color: #3a3a3a;
            color: #fff;
            border: 2px solid #4a90e2;
            border-radius: 8px;
            padding: 2px;
        """)
        self.move_mouse_pynput.setChecked(True)

        # Content Layout
        debug_layout = QtWidgets.QVBoxLayout()
        debug_layout.setContentsMargins(0, 0, 0, 0)

        # Background label
        self.current_state_label_BG = QtWidgets.QLabel() 
        self.current_state_label_BG.setFixedWidth(97)
        self.current_state_label_BG.setFixedHeight(80)
        self.current_state_label_BG.setStyleSheet("""
            text-align: center;
            font-size: 10px;
            border: 2px solid #4a90e2; 
            border-radius: 8px;
            padding: 0px;
            background-color: #3a3a3a;
        """)
        self.current_state_label_BG.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)
        debug_layout.addWidget(self.current_state_label_BG)
        debug_layout.setSpacing(0)
        # Text label
        self.current_state_label_title = QtWidgets.QLabel('Debug')
        self.current_state_label_title.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)
        self.current_state_label_title.setStyleSheet("""
            text-align: center;
            font-size: 12px;
            font-weight: bold;
            border: 2px solid #4a90e2; 
            border-radius: 6px;
            margin: 0px !important;                                         
            padding: 0px !important;
            background-color: transparent;
        """)
        self.current_state_label = QtWidgets.QLabel("Ready!")
        self.current_state_label.setFixedWidth(97)
        self.current_state_label.setFixedHeight(70)
        self.current_state_label.setStyleSheet("""
            text-align: center;
            font-size: 10px;
            border: 0px solid #4a90e2; 
            margin: 0px !important;
            padding: 0px !important;
            border-radius: 2px;
            background-color: transparent;
        """)
        self.current_state_label.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)
        self.current_state_label.setContentsMargins(0, 0, 0, 0)
        

        # Create a layout for the text label and add it to the background label
        text_layout = QtWidgets.QVBoxLayout(self.current_state_label_BG)
        text_layout.setSpacing(2)

        text_layout.addWidget(self.current_state_label_title)
        text_layout.addWidget(self.current_state_label)
        text_layout.setContentsMargins(0, 0, 0, 0) 

        content_layout = QtWidgets.QVBoxLayout()
        content_layout.setSpacing(2)
        content_layout.setContentsMargins(0, 0, 0, 0)
        #content_layout.addWidget(self.status_label)
        button_layout.setSpacing(2)
        content_layout.addLayout(button_layout)
        content_layout.addWidget(self.action_set_combo_box)
        content_layout.addWidget(self.move_mouse_pynput)
        content_layout.addLayout(debug_layout) 

        # Main Layout
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(3, 0, 0, 0)
        layout.setSpacing(5)
        #layout.addWidget(self.title_bar)
        layout.addLayout(content_layout)

        # Set main layout
        self.setLayout(layout)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowTitle('OSROKBOT')

        self.play_button.show()
        self.stop_button.hide()
        #self.setFixedSize(100, 150)
        #fix horizontal size
        self.setFixedWidth(100)

        #transparent backgourd
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        

        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowOpacity(0.75)
        self.show()
        WindowHandler().activate_window("OSROKBOT")
        GLOBAL_VARS.UI = self

            # Новые флаги 
        self.is_dragging = False
        self.is_moving = False 
        self.stop_flag = False
        
        self.OS_ROKBOT.UI = self

        self.reload_button = QtWidgets.QPushButton("X")
        self.reload_button.clicked.connect(self.reload_bot)
        button_layout.addWidget(self.reload_button)

    def start_global_key_listener(self):
        """Запускает глобальный слушатель клавиш."""
        def on_press(key):
            try:
                # Проверяем, нажата ли клавиша F1
                if key == keyboard.Key.f1:
                    self.stop_automation()  # Вызываем функцию reload_bot
            except Exception as e:
                print(f"Error in global key listener: {e}")

        # Создаем и запускаем слушатель клавиш
        self.listener = keyboard.Listener(on_press=on_press)
        self.listener.start()

    def reload_bot(self):
        """
        Перезагружает приложение бота.
        """
        try:
            self.stop_automation()
            self.close()
            python = sys.executable
            import os
            os.execl(python, python, *sys.argv)

        except Exception as e:
            print(f"Error reloading bot: {e}")

    def currentState(self, state_text):
        self.current_state_label.setText(state_text)
        self.current_state_label.adjustSize() # Optional, to adjust the size of the label to fit the new text

    def update_position(self):
        if self.is_dragging or self.is_moving:
            return
        target_windows = gw.getWindowsWithTitle(self.target_title)
        active_window = gw.getActiveWindow()
        if target_windows and (
                target_windows[0].title == self.target_title or target_windows[0].title == "OSROKBOT"):
            target_window = target_windows[0]
            self.move(target_window.left - self.frameGeometry().width() - 10, target_window.top + 10)
            if active_window and (
                    active_window.title == self.target_title or active_window.title == "OSROKBOT" or active_window.title == "python3"):
                self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
            else:
                self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowStaysOnTopHint)
            if not self.isVisible():
                self.show()

    def start_automation(self):
        if self.OS_ROKBOT.is_running or not self.OS_ROKBOT.all_threads_joined:
            self.current_state_label.setText('Finishing last job\nwait 2s')
            return
    
        selected_index = self.action_set_combo_box.currentIndex()
        if selected_index == -1:
            self.current_state_label.setText('Select action')
            return
    
        selected_action_name = self.action_set_names[selected_index]
        move_mouse_checked = self.move_mouse_pynput.isChecked()
    
        if selected_action_name == "run_random":
            threading.Thread(target=self.action_sets.run_random).start()
            self.status_label.setText(' Run Random Scripts')
            self.status_label.setStyleSheet("color: green;font-weight: bold;")
            self.play_button.hide()
            self.stop_button.show()
        else:
            action_method = getattr(self.action_sets, selected_action_name)
    
            # Проверяем, принимает ли метод аргумент move_mouse_checked
            if "move_mouse_checked" in inspect.signature(action_method).parameters:
                action_group = action_method(move_mouse_checked)
            else:
                action_group = action_method()
    
            actions_groups = [action_group]
            self.OS_ROKBOT.start(actions_groups)
            self.status_label.setText(' Run')
            self.status_label.setStyleSheet("color: green;font-weight: bold;")
            self.play_button.hide()
            self.stop_button.show()

    def stop_automation(self):
        self.stop_flag = True
        self.OS_ROKBOT.stop()
        self.status_label.setText(' Ready')
        self.status_label.setStyleSheet("color: #4a90e2; font-weight: bold; text-align: left;")
        self.play_button.show()
        self.stop_button.hide()
        threading.Thread(target=self.call_current_state, args=("Ready",)).start()
        
        
    def call_current_state(self,info):
        time.sleep(2)
        self.currentState(info)

    def closeEvent(self, event):
        self.stop_automation()
        self.listener.stop()
        event.accept()
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    gui = UI('BlueStacks App Player 3')
    
    sys.exit(app.exec_())