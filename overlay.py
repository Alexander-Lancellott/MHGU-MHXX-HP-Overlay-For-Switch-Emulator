import os
import re
import sys
import time
import math
import cursor
import win32gui
from ahk import AHK, Position
from PySide6.QtCore import QTimer, Qt, QThread, Signal
from PySide6.QtGui import QColorConstants
from modules.mhgu_xx import get_data, get_base_address, Monsters
from modules.config import ConfigOverlay, ConfigLayout, ConfigColors
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QSizePolicy
from modules.utils import (
    TextColor,
    PassiveTimer,
    prevent_keyboard_exit_error,
    rgba_int,
    clear_screen,
    header,
    max_monsters,
    logger_init,
    log_timer,
    log_error,
)
from ahk_wmutil import wmutil_extension


class DataFetcher(QThread):
    data_fetched = Signal(list)

    def __init__(self, pid, base_address, show_small_monsters, running, max_workers):
        super().__init__()
        self.pid = pid
        self.running = running
        self.base_address = base_address
        self.show_small_monsters = show_small_monsters
        self.max_workers = max_workers

    def run(self):
        while True:
            data = get_data(self.pid, self.base_address, self.show_small_monsters, self.max_workers)
            self.data_fetched.emit(data)
            self.msleep(round(ConfigOverlay.hp_update_time * 1000))


class Overlay(QWidget):
    def __init__(self):
        super().__init__()
        self.current_time = 0
        self.last_execution = 0
        self.debounce_time = 0.5
        self.is_borderless = False
        self.running = False
        self.is_xx = False
        self.is_open_window = False
        self.process_handle = None
        self.base_address = None
        self.initial_window_state: Position = Position(0, 0, 800, 600)
        self.win_title = None
        self.process_name = None
        self.is_ryujinx = False
        self.pid = None
        self.timeout = (20 * 60) + 1  # 20 minutes
        self.counter = self.timeout
        self.timeout_start = time.time()
        self.max_workers = ConfigOverlay.max_workers
        self.emu_hide_ui = ConfigLayout.emu_hide_ui
        self.orientation = ConfigLayout.orientation
        self.x = ConfigLayout.x
        self.y = ConfigLayout.y
        self.show_initial_hp = ConfigOverlay.show_initial_hp
        self.show_hp_percentage = ConfigOverlay.show_hp_percentage
        self.show_small_monsters = ConfigOverlay.show_small_monsters,
        self.fix_offset = dict(x=ConfigLayout.fix_x, y=ConfigLayout.fix_y)
        self.hotkey = ConfigOverlay.hotkey
        self.data_fetcher = None
        self.hp_update_time = round(ConfigOverlay.hp_update_time * 1000)
        self.debugger = ConfigOverlay.debugger
        self.pt = PassiveTimer()
        self.initialize_ui()

    def initialize_ui(self):
        target_window_title = "MONSTER HUNTER (GENERATIONS ULTIMATE|XX Nintendo Switch Ver.)[\\w\\W\\s]+"
        not_responding_title = " \\([\\w\\s]+\\)$"
        yuzu_target_window_title = "(yuzu|suyu|sudachi)[\\w\\W\\s]+\\| (HEAD|dev|sudachi)-[\\w\\W\\s]+"
        ahk = AHK(version="v2", extensions=[wmutil_extension])

        if self.debugger:
            logger_init(".log")
            self.pt.start(5)

        self.setWindowTitle("Overlay")
        self.setWindowFlags(
            Qt.WindowType.Tool
            | Qt.WindowType.CustomizeWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.FramelessWindowHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.setStyleSheet(
            f"""
            font-family: {ConfigOverlay.font_family}; 
            font-weight: {ConfigOverlay.font_weight};
            font-size: {ConfigOverlay.font_size}px;
            border-radius: 5px;
            margin: 0 0 5px;
            """
        )

        color = rgba_int(
            getattr(QColorConstants.Svg, ConfigColors.text_color).rgb(),
            ConfigColors.text_transparency,
        )
        background_color = rgba_int(
            getattr(QColorConstants.Svg, ConfigColors.background_color).rgb(),
            ConfigColors.background_transparency,
        )

        labels = []
        for i in range(0, max_monsters):
            label = QLabel()
            label.setStyleSheet(
                f"""
                color: {color};
                background-color: {background_color};
                padding: 5px {15 if self.orientation == 'center' else 10}px;
                """
            )
            label.setSizePolicy(
                QSizePolicy.Policy.Expanding if ConfigLayout.align else QSizePolicy.Policy.Fixed,
                QSizePolicy.Policy.Fixed
            )
            if self.orientation == "right":
                label.setAlignment(Qt.AlignmentFlag.AlignRight)
            elif self.orientation == "left":
                label.setAlignment(Qt.AlignmentFlag.AlignLeft)
            else:
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            labels.append(label)

        label_layouts = []
        for i in range(0, max_monsters):
            label_layout = QVBoxLayout()
            label_layout.setContentsMargins(0, 0, 0, 0)
            if self.orientation == "right":
                label_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
            elif self.orientation == "left":
                label_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
            else:
                label_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label_layouts.append(label_layout)

        lm_layout = QVBoxLayout()
        lm_layout.setContentsMargins(0, 0, 0, 0)
        lm_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        sm_layout = QVBoxLayout()
        sm_layout.setContentsMargins(0, 0, 0, 0)
        sm_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        for index, label_layout in enumerate(label_layouts):
            if 2 > index:
                lm_layout.addLayout(label_layout)
            else:
                sm_layout.addLayout(label_layout)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addLayout(lm_layout)
        layout.addLayout(sm_layout)

        self.update_position(ahk, layout, target_window_title, not_responding_title, yuzu_target_window_title)

        timer1 = QTimer(self)
        timer1.timeout.connect(
            lambda: self.update_position(
                ahk, layout, target_window_title, not_responding_title, yuzu_target_window_title
            )
        )
        timer1.start(10)

        ahk.add_hotkey(
            f"{self.hotkey} Up",
            callback=lambda: self.toggle_borderless_screen(
                ahk, target_window_title, not_responding_title, yuzu_target_window_title
            ),
        )
        ahk.start_hotkeys()

        timer2 = QTimer(self)
        timer2.timeout.connect(lambda: self.wait_init_game(labels, label_layouts))
        timer2.start(1000)

    def start_data_fetcher(self, labels, label_layouts):
        self.data_fetcher = DataFetcher(
            self.pid, self.base_address, self.show_small_monsters, self.running, self.max_workers
        )
        self.data_fetcher.data_fetched.connect(
            lambda data: self.update_show(data, labels, label_layouts)
        )
        self.data_fetcher.start()

    def get_window(self, ahk, target_window_title, not_responding_title, yuzu_target_window_title):
        self.is_xx = False
        win = None
        win_not_responding = ahk.find_window(
            title=target_window_title + not_responding_title, title_match_mode="RegEx"
        )
        if not win_not_responding:
            win = ahk.find_window(title=target_window_title, title_match_mode="RegEx")
            if win:
                if re.search("XX", win.title):
                    self.is_xx = True
                win_not_responding2 = ahk.find_window(
                    title=yuzu_target_window_title + not_responding_title, title_match_mode="RegEx"
                )
                if not win_not_responding2:
                    win2 = ahk.find_window(title=yuzu_target_window_title, title_match_mode="RegEx")
                    if win2:
                        win = win2
        return win

    @staticmethod
    def get_window_position(hwnd):
        rect = win32gui.GetWindowRect(hwnd)
        x = rect[0]
        y = rect[1]
        width = rect[2] - rect[0]
        height = rect[3] - rect[1]
        return Position(x, y, width, height)

    def toggle_borderless_screen(self, ahk, target_window_title, not_responding_title, yuzu_target_window_title):
        try:
            win = self.get_window(ahk, target_window_title, not_responding_title, yuzu_target_window_title)
            monitor = win.get_monitor()
            target = self.get_window_position(win.id)
            win.set_style("^0xC00000")
            win.set_style("^0x40000")
            self.is_borderless = monitor.size[0] <= target.width and monitor.size[1] - 1 <= target.height
            if self.is_borderless:
                win.set_style("+0xC00000")
                win.set_style("+0x40000")
                win32gui.MoveWindow(
                    win.id,
                    self.initial_window_state.x,
                    self.initial_window_state.y,
                    self.initial_window_state.width,
                    self.initial_window_state.height,
                    True
                )
            else:
                self.initial_window_state = target
                win.set_style("-0xC00000")
                win.set_style("-0x40000")
                win32gui.MoveWindow(
                    win.id,
                    monitor.position[0],
                    monitor.position[1],
                    monitor.size[0],
                    monitor.size[1] + 1,
                    True
                )
        except Exception as error:
            if self.debugger:
                log_error(f'Toggle Borderless Error: {error}')
            pass

    def wait_init_game(self, labels, label_layouts):
        if not self.is_open_window:
            if self.running:
                clear_screen()
                header()
            if self.data_fetcher:
                self.data_fetcher.terminate()
            self.hide()
            self.running = False
            self.counter -= 1
            self.base_address = None
            m, s = divmod(self.counter, 60)
            if self.counter >= 0:
                red_text = TextColor.red("No game running.")
                yellow_text = TextColor.yellow(f"{m:02d}:{s:02d}")
                text = f"{red_text} Waiting {yellow_text}, then it will close."
                print(f"\r{text}", end="", flush=True)
            if time.time() > self.timeout_start + self.timeout:
                sys.exit()
        else:
            if not self.base_address:
                self.base_address = get_base_address(self.process_name)
                if self.base_address and self.base_address > 0:
                    self.start_data_fetcher(labels, label_layouts)
            if not self.running:
                clear_screen()
                header()
            self.running = True
            self.counter = self.timeout
            self.timeout_start = time.time()
            text = TextColor.green(f"{"MHXX" if self.is_xx else "MHGU"} running.")
            print(f"\r{text}", end="", flush=True)

    def update_show(self, data, labels, label_layouts):
        for index, label in enumerate(labels):
            if len(data) > index:
                label_layout = label_layouts[index]
                monster = data[index]
                large_monster_name = Monsters.large_monsters.get(monster[0])
                small_monster_name = Monsters.small_monsters.get(monster[0])
                hp = monster[1]
                initial_hp = monster[2]
                if initial_hp > 5:
                    if large_monster_name and hp < 45000:
                        text = f"{large_monster_name}:"
                        if self.show_hp_percentage:
                            text += f" {math.ceil((hp / initial_hp) * 100)}% |"
                        text += f" {hp}"
                        if self.show_initial_hp:
                            text += f" | {initial_hp}"
                        label.setText(text)
                        label_layout.addWidget(label)
                    if ConfigOverlay.show_small_monsters:
                        if small_monster_name and hp < 20000:
                            initial_hp = monster[2]
                            text = f"{small_monster_name}:"
                            if self.show_hp_percentage:
                                text += f" {math.ceil((hp / initial_hp) * 100)}% |"
                            text += f" {hp}"
                            if self.show_initial_hp:
                                text += f" | {initial_hp}"
                            label.setText(text)
                            label_layout.addWidget(label)
                else:
                    label.clear()
                    label.setParent(None)
            else:
                label.clear()
                label.setParent(None)
            self.show()

    def update_position(self, ahk, layout, target_window_title, not_responding_title, yuzu_target_window_title):
        try:
            win = self.get_window(ahk, target_window_title, not_responding_title, yuzu_target_window_title)
            target = self.get_window_position(win.id)
            monitor = win.get_monitor()
            scale_factor = monitor.scale_factor
            hide_ui = not re.search("(GENERATIONS ULTIMATE|XX)", win.title)
            self.process_name = win.process_name
            self.pid = win.pid
            self.is_ryujinx = self.process_name.lower() == "ryujinx.exe"
            self.resize(self.minimumSizeHint())
            self.is_borderless = monitor.size[0] <= target.width and monitor.size[1] - 1 <= target.height

            margin_top = 35 * scale_factor
            margin_bottom = 11 * scale_factor
            margin_left = 10 * scale_factor
            margin_right = 10 * scale_factor

            if self.is_borderless:
                margin_top = 4 * scale_factor
                margin_bottom = 6 * scale_factor
                margin_left = 4 * scale_factor
                margin_right = 4 * scale_factor

            if not self.emu_hide_ui and not hide_ui:
                if self.is_ryujinx:
                    margin_top = 69 * scale_factor
                    margin_bottom = 33 * scale_factor
                    if self.is_borderless:
                        margin_top = 38 * scale_factor
                        margin_bottom = 25 * scale_factor
                else:
                    margin_top = 55 * scale_factor
                    margin_bottom = 32 * scale_factor
                    if self.is_borderless:
                        margin_top = 25 * scale_factor
                        margin_bottom = 25 * scale_factor

            offset_x = (target.x + (target.width - self.geometry().width()) * self.x / 100) + self.fix_offset["x"]
            offset_y = (target.y + (target.height - self.geometry().height()) * self.y / 100) + self.fix_offset["y"]
            layout.setContentsMargins(margin_left, margin_top, margin_right, margin_bottom)
            if self.debugger:
                log_timer(self.pt, [
                    dict(type="info", msg=f'Window Title: {win.title}'),
                    dict(type="info", msg=f'Window Target: {target}'),
                    dict(type="info", msg=f'Monitor: {monitor.position} {monitor.size}'),
                    dict(type="info", msg=f'Borderless: {self.is_borderless}'),
                    dict(type="info", msg=f'Offsets: {offset_x} {offset_y}'),
                ])
            self.move(offset_x, offset_y)
            self.is_open_window = True
        except Exception as error:
            if self.debugger:
                log_timer(self.pt, [
                    dict(type="error", msg=f'Update Position Error: {error}'),
                ])
            self.is_open_window = False


if __name__ == "__main__":
    os.environ["QT_FONT_DPI"] = '1'
    prevent_keyboard_exit_error()
    cursor.hide()
    header()
    app = QApplication(sys.argv)
    overlay = Overlay()
    sys.exit(app.exec())
