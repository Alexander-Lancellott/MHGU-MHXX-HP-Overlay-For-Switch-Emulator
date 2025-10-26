import os
import re
import sys
import time
import yaml
import signal
import ctypes
import logging
from art import *
from colorama import Fore
from typing import TypedDict
from functools import lru_cache
from logging.handlers import RotatingFileHandler

green = Fore.GREEN
yellow = Fore.YELLOW
red = Fore.RED
reset = Fore.RESET

max_monsters = 10
max_status = 8


def clear_screen():
    if os.name == "posix":
        os.system("clear")
    else:
        os.system("cls")


def rgba_int(rgb_int, alpha=100):
    return f"rgba{rgb_int // 256 // 256 % 256, rgb_int // 256 % 256, rgb_int % 256, alpha / 100}"


def absolute_path(path: str = ""):
    return os.path.abspath(path).replace("\\modules", "")


def end():
    time.sleep(8)
    sys.exit()


def prevent_keyboard_exit_error():
    def handler(signum, frame):
        sys.exit()

    return signal.signal(signal.SIGINT, handler)


class TextColor:
    @staticmethod
    def green(text):
        return f"{green}{text}{reset}"

    @staticmethod
    def yellow(text):
        return f"{yellow}{text}{reset}"

    @staticmethod
    def red(text):
        return f"{red}{text}{reset}"


def header():
    tprint("MHGU HP Overlay\n", font="tarty1")
    exit_hotkey = TextColor.yellow("Ctrl + C")
    print(f"Exit with {exit_hotkey} or close the application.\n")


def get_crown(size, crowns, enable):
    if not enable or crowns["g"] is None:
        return ""
    if crowns["g"] <= size:
        return " Gold"
    if crowns["s"] <= size:
        return " Silver"
    if crowns["m"] >= size:
        return " Mini"
    return ""


class PassiveTimer:
    def __init__(self):
        self.end_time = None

    def start(self, duration: int):
        self.end_time = time.monotonic() + duration

    @property
    def end(self):
        return time.monotonic() > self.end_time


class Option(TypedDict):
    type: str
    msg: str


class Translator:
    def __init__(self, language="en_US", path="locales"):
        self.language = language
        self.path = path
        self.translations = {}
        self.load_translations()

    def load_translations(self):
        try:
            with open(f"{absolute_path(self.path)}/{self.language}.yaml", "r", encoding="utf-8") as f:
                self.translations = yaml.safe_load(f) or {}
        except FileNotFoundError:
            self.translations = {}

    def set_language(self, language):
        self.language = language
        self.load_translations()

    def __call__(self, key, **kwargs):
        text = self.translations.get(key, key)
        return text.format(**kwargs) if kwargs else text


def log_timer(pt: PassiveTimer, options: list[Option]):
    if pt.end:
        for option in options:
            if option['type'] == "info":
                log_info(option['msg'])
            if option['type'] == "error":
                log_error(option['msg'])
        pt.start(5)


def logger_init(filename: str):
    if os.path.exists(filename):
        os.remove(filename)
    rfh = RotatingFileHandler(filename, maxBytes=10 * 1024 * 1024, backupCount=1)
    logging.basicConfig(
        encoding='utf-8',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[rfh]
    )


@lru_cache(5)
def log_info(msg: str):
    logging.info(msg)


@lru_cache(5)
def log_error(msg: str):
    logging.error(msg)


def enable_ansi_colors():
    if sys.platform != "win32":
        return

    kernel32 = ctypes.windll.kernel32
    handle = kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE = -11

    mode = ctypes.c_uint()
    kernel32.GetConsoleMode(handle, ctypes.byref(mode))

    ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
    new_mode = mode.value | ENABLE_VIRTUAL_TERMINAL_PROCESSING
    kernel32.SetConsoleMode(handle, new_mode)


def disable_quick_edit():
    if sys.platform != "win32":
        return

    kernel32 = ctypes.windll.kernel32
    hStdin = kernel32.GetStdHandle(-10)  # STD_INPUT_HANDLE = -10

    # Get current console mode
    mode = ctypes.c_uint()
    kernel32.GetConsoleMode(hStdin, ctypes.byref(mode))

    # Disable ENABLE_QUICK_EDIT_MODE (0x40)
    # Keep the other flags
    new_mode = mode.value & ~0x40
    kernel32.SetConsoleMode(hStdin, new_mode)


def reset_app():
    clear_screen()
    python = sys.executable
    os.execl(python, python, *sys.argv)


class RyujinxLogMonitor:
    def __init__(self, log_dir):
        self.log_dir = log_dir
        self.last_pos = 0
        self.current_title = None

    def _get_latest_log(self):
        logs = [f for f in os.listdir(self.log_dir) if f.endswith(".log")]
        if not logs:
            return None
        logs.sort(key=lambda f: os.path.getmtime(os.path.join(self.log_dir, f)), reverse=True)
        return os.path.join(self.log_dir, logs[0])

    def check_game_running(self):
        log_file = self._get_latest_log()
        if not log_file:
            return None

        with open(log_file, "r", encoding="utf-8") as f:
            f.seek(self.last_pos)
            lines = f.readlines()
            self.last_pos = f.tell()

        for line in lines:
            # Loader Start: Application Loaded: MONSTER HUNTER GENERATIONS ULTIMATE v1.4.0 [0100770008dd8000] [32-bit]
            match = re.search(r'Loader Start: Application Loaded: ([^\n]+)', line)
            if match:
                self.current_title = match.group(1)

            # HLE.GuestThread.48 KernelSvc : WaitProcessWideKeyAtomic() = TerminationRequested
            # AudioProcessor.Worker AudioRenderer Work: Stopping audio processor
            # HLE.OsThread.11 AudioRenderer StopLocked: Stopped audio renderer
            if re.search(r'= TerminationRequested', line):
                self.current_title = None

        return self.current_title
