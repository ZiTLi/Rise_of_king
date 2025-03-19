import sys
import importlib
from PyQt5 import QtWidgets, QtGui, QtCore
from action_sets import ActionSets
from OS_ROKBOT import OSROKBOT
import pygetwindow as gw
import time
from window_handler import WindowHandler
from global_vars import GLOBAL_VARS
import threading
import inspect  # Добавьте этот импорт


class UI(QtWidgets.QWidget):
    def __init__(self, window_title, delay=0):
        super().__init__()
        self.OS_ROKBOT = OSROKBOT(window_title, delay)
        self.OS_ROKBOT.signal_emitter.pause_toggled.connect(self.on_pause_toggled)
        self.action_sets = ActionSets(OS_ROKBOT=self.OS_ROKBOT)
        self.target_title = window_title
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_position)
        self.timer.start(10)
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
            color: white !important;
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

        self.status_label = QtWidgets.QLabel(' Ready!')
        self.status_label.setStyleSheet("color: #4a90e2; font-weight: bold; text-align: left !important;")
        self.status_label.setAlignment(QtCore.Qt.AlignLeft)
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setAlignment(QtCore.Qt.AlignLeft)
        self.play_button = QtWidgets.QPushButton()
        self.play_icon = QtGui.QIcon("Media/UI/play_icon.svg")
        self.play_button.setIcon(self.play_icon)
        self.play_button.setIconSize(QtCore.QSize(24, 24))
        self.play_button.clicked.connect(self.start_automation)
        button_layout.addWidget(self.play_button)
        self.stop_button = QtWidgets.QPushButton()
        self.stop_icon = QtGui.QIcon("Media/UI/stop_icon.svg")
        self.stop_button.setIcon(self.stop_icon)
        self.stop_button.setIconSize(QtCore.QSize(24, 24))
        self.stop_button.clicked.connect(self.stop_automation)
        button_layout.addWidget(self.stop_button)
        self.pause_button = QtWidgets.QPushButton()
        self.pause_icon = QtGui.QIcon("Media/UI/pause_icon.svg")
        self.unpause_icon = QtGui.QIcon("Media/UI/play_icon.svg")
        self.pause_button.setIcon(self.pause_icon)
        self.pause_button.setIconSize(QtCore.QSize(24, 24))
        self.pause_button.clicked.connect(self.toggle_pause)
        button_layout.addWidget(self.pause_button)
        self.action_set_combo_box = QtWidgets.QComboBox()
        self.action_set_combo_box.setStyleSheet("""
            color: #fff;
        """)
        self.action_set_names = [
            method_name
            for method_name, method in inspect.getmembers(self.action_sets, predicate=inspect.ismethod)
            if method.__self__ == self.action_sets
            and not method_name.startswith('_')  # Исключаем приватные методы
            and method_name not in ('__init__', 'create_machine', 'email_captcha')  # Исключаем __init__ и create_machine
        ]
        self.action_set_combo_box.addItems(self.action_set_names)
        self.check_captcha_checkbutton = QtWidgets.QCheckBox("captcha")
        self.check_captcha_checkbutton.setStyleSheet("""
            font-size: 11px;
            background-color: #3a3a3a;
            color: #fff;
            border: 2px solid #4a90e2;
            border-radius: 8px;
            padding: 2px;
        """)
        self.check_captcha_checkbutton.setChecked(True)
        debug_layout = QtWidgets.QVBoxLayout()
        debug_layout.setContentsMargins(0, 0, 0, 0)
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
        text_layout = QtWidgets.QVBoxLayout(self.current_state_label_BG)
        text_layout.setSpacing(2)
        text_layout.addWidget(self.current_state_label_title)
        text_layout.addWidget(self.current_state_label)
        text_layout.setContentsMargins(0, 0, 0, 0)
        self.mouse_press_position = None
        self.mouse_move_position = None
        self.is_dragging = False  # Добавлено
        self.is_moving = False  # Добавлено

        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(button_layout)
        layout.addWidget(self.action_set_combo_box)

        content_layout = QtWidgets.QVBoxLayout()
        content_layout.setSpacing(2)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.addWidget(self.check_captcha_checkbutton)
        content_layout.addLayout(debug_layout)
        layout.addLayout(content_layout)

        self.setLayout(layout)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowTitle('OSROKBOT')
        self.play_button.show()
        self.stop_button.hide()
        self.pause_button.hide()
        self.setFixedWidth(100)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowOpacity(0.75)
        self.show()
        WindowHandler().activate_window("OSROKBOT")
        GLOBAL_VARS.UI = self

        self.reload_button = QtWidgets.QPushButton("X")
        self.reload_button.clicked.connect(self.reload_bot)  # Подключаем обработчик
        button_layout.addWidget(self.reload_button)

    def reload_bot(self):
        """
        Перезагружает приложение бота.
        """
        try:
            # 1. Stop the bot
            self.stop_automation()

            # 2. Close the current UI
            self.close()

            # 3. Restart the application
            python = sys.executable
            import os
            os.execl(python, python, *sys.argv)

        except Exception as e:
            print(f"Error reloading bot: {e}")

    def currentState(self, state_text):
        self.current_state_label.setText(state_text)
        self.current_state_label.adjustSize()

    def update_position(self):
        if self.is_dragging or self.is_moving:  # Изменено
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

    def on_pause_toggled(self, is_paused):
        if is_paused:
            self.status_label.setText(' Paused')
            self.status_label.setStyleSheet("color: orange;")
            self.pause_button.setIcon(self.unpause_icon)
            self.stop_button.show()
            self.pause_button.show()
            self.play_button.hide()
        else:
            self.status_label.setText(' Running')
            self.status_label.setStyleSheet("color: green;")
            self.pause_button.setIcon(self.pause_icon)
            self.play_button.hide()
            self.pause_button.show()
            self.pause_button.show()

    def start_automation(self):
        if self.OS_ROKBOT.is_running or not self.OS_ROKBOT.all_threads_joined:
            self.current_state_label.setText('Finishing last job\nwait 2s')
            return
        else:
            if self.OS_ROKBOT.is_paused():
                self.toggle_pause()
            selected_index = self.action_set_combo_box.currentIndex()
            if selected_index != -1:
                action_group = getattr(self.action_sets, self.action_set_names[selected_index])()
                actions_groups = [action_group]
                if self.check_captcha_checkbutton.isChecked():
                    actions_groups.append(self.action_sets.email_captcha())
                self.OS_ROKBOT.start(actions_groups)
                self.status_label.setText(' Running')
                self.status_label.setStyleSheet("color: green;font-weight: bold;")
            self.play_button.hide()
            self.stop_button.show()
            self.pause_button.show()

    def stop_automation(self):
        self.OS_ROKBOT.stop()
        self.status_label.setText(' Ready')
        self.status_label.setStyleSheet("color: #4a90e2; font-weight: bold; text-align: left;")
        self.play_button.show()
        self.stop_button.hide()
        self.pause_button.hide()
        threading.Thread(target=self.call_current_state, args=("Ready",)).start()

    def toggle_pause(self):
        self.OS_ROKBOT.toggle_pause()
        if self.OS_ROKBOT.is_paused():
            threading.Thread(target=self.call_current_state, args=("Paused",)).start()

    def call_current_state(self, info):
        time.sleep(2)
        self.currentState(info)

    def closeEvent(self, event):
        self.stop_automation()
        event.accept()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.mouse_press_position = event.globalPos()
            self.mouse_move_position = event.globalPos()
            self.setWindowOpacity(0.5)
            self.is_dragging = True  # Добавлено

    def mouseMoveEvent(self, event):
        if self.is_dragging:  # Изменено
            delta = event.globalPos() - self.mouse_move_position
            self.move(self.pos() + delta)
            self.mouse_move_position = event.globalPos()
            self.is_moving = True  # Добавлено

    def mouseReleaseEvent(self, event):
        self.mouse_press_position = None
        self.mouse_move_position = None
        self.setWindowOpacity(0.75)
        self.is_dragging = False  # Добавлено
        self.is_moving = False  # Добавлено


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    gui = UI('BlueStacks App Player 3')
    sys.exit(app.exec_())