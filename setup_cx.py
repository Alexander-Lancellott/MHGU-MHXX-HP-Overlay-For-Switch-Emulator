from cx_Freeze import setup, Executable
from modules.utils import absolute_path

build_exe_options = {
    "build_exe": absolute_path("build\\dist"),
    "include_files": [
        absolute_path(".venv\\Scripts\\AutoHotkey.exe"),
        absolute_path(".venv\\Scripts\\AutoHotkeyV2.exe"),
        absolute_path("config.ini"),
        absolute_path("LICENSE"),
        absolute_path("README.md"),
    ],
    "zip_exclude_packages": ["ahk", "ahk_wmutil"],
    "zip_include_packages": "*",
    "optimize": 2,
}

setup(
    name="MHGU-MHXX-HP-Overlay",
    version="1.1.3",
    author="Alexander-Lancellott",
    description="MHGU-MHXX-HP-Overlay",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            absolute_path("overlay.py"),
            target_name="MHGU-MHXX-HP-Overlay",
            base="console",
            icon=absolute_path("overlay.ico"),
        )
    ],
)
