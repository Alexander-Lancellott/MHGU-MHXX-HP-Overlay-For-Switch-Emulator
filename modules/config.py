import re
from pathlib import Path
from configparser import ConfigParser
from dataclasses import dataclass
from modules.utils import TextColor, prevent_keyboard_exit_error, absolute_path, end

config = ConfigParser()
hotkey_regex = "^([\\^!+#<>]*([a-zA-Z0-9]|F[1-9]|F1[0-2])?)\\s*$"
colors = [
    "aliceblue",
    "antiquewhite",
    "aqua",
    "aquamarine",
    "azure",
    "beige",
    "bisque",
    "black",
    "blanchedalmond",
    "blue",
    "blueviolet",
    "brown",
    "burlywood",
    "cadetblue",
    "chartreuse",
    "chocolate",
    "coral",
    "cornflowerblue",
    "cornsilk",
    "crimson",
    "cyan",
    "darkblue",
    "darkcyan",
    "darkgoldenrod",
    "darkgray",
    "darkgreen",
    "darkgrey",
    "darkkhaki",
    "darkmagenta",
    "darkolivegreen",
    "darkorange",
    "darkorchid",
    "darkred",
    "darksalmon",
    "darkseagreen",
    "darkslateblue",
    "darkslategray",
    "darkslategrey",
    "darkturquoise",
    "darkviolet",
    "deeppink",
    "deepskyblue",
    "dimgray",
    "dimgrey",
    "dodgerblue",
    "firebrick",
    "floralwhite",
    "forestgreen",
    "fuchsia",
    "gainsboro",
    "ghostwhite",
    "gold",
    "goldenrod",
    "gray",
    "green",
    "greenyellow",
    "grey",
    "honeydew",
    "hotpink",
    "indianred",
    "indigo",
    "ivory",
    "khaki",
    "lavender",
    "lavenderblush",
    "lawngreen",
    "lemonchiffon",
    "lightblue",
    "lightcoral",
    "lightcyan",
    "lightgoldenrodyellow",
    "lightgray",
    "lightgreen",
    "lightgrey",
    "lightpink",
    "lightsalmon",
    "lightseagreen",
    "lightskyblue",
    "lightslategray",
    "lightslategrey",
    "lightsteelblue",
    "lightyellow",
    "lime",
    "limegreen",
    "linen",
    "magenta",
    "maroon",
    "mediumaquamarine",
    "mediumblue",
    "mediumorchid",
    "mediumpurple",
    "mediumseagreen",
    "mediumslateblue",
    "mediumspringgreen",
    "mediumturquoise",
    "mediumvioletred",
    "midnightblue",
    "mintcream",
    "mistyrose",
    "moccasin",
    "navajowhite",
    "navy",
    "oldlace",
    "olive",
    "olivedrab",
    "orange",
    "orangered",
    "orchid",
    "palegoldenrod",
    "palegreen",
    "paleturquoise",
    "palevioletred",
    "papayawhip",
    "peachpuff",
    "peru",
    "pink",
    "plum",
    "powderblue",
    "purple",
    "red",
    "rosybrown",
    "royalblue",
    "saddlebrown",
    "salmon",
    "sandybrown",
    "seagreen",
    "seashell",
    "sienna",
    "silver",
    "skyblue",
    "slateblue",
    "slategray",
    "slategrey",
    "snow",
    "springgreen",
    "steelblue",
    "tan",
    "teal",
    "thistle",
    "tomato",
    "turquoise",
    "violet",
    "wheat",
    "white",
    "whitesmoke",
    "yellow",
    "yellowgreen",
]

prevent_keyboard_exit_error()


def save():
    with open(absolute_path("config.ini"), "w") as config_file:
        config.write(config_file)


def set_section(section, conf):
    if section in conf:
        return conf[section]
    else:
        conf[section] = {}
        save()
        return conf[section]


def print_error(option, error):
    print(f"{TextColor.yellow(option)} - {TextColor.red(error)}")
    end()


def set_option(option, section, attr, default):
    try:
        if option in section:
            return getattr(section, attr)(option)
        else:
            section[option] = default
            save()
            return getattr(section, attr)(option)
    except Exception as error:
        print_error(option, error)


@dataclass
class Config:
    config.read("config.ini")
    Overlay = set_section("Overlay", config)
    Layout = set_section("Layout", config)
    Colors = set_section("Colors", config)


@dataclass
class ConfigOverlay:
    hotkey = set_option("hotkey", Config.Overlay, "get", "^!f")
    if not re.search(hotkey_regex, hotkey):
        error = (
            "Invalid hotkey. "
            "Check this: https://www.autohotkey.com/docs/v1/Hotkeys.htm#Symbols "
            "The symbols *, ~, $ and UP are not allowed."
        )
        print_error("hotkey", error)
    reset_hotkey = set_option("reset_hotkey", Config.Overlay, "get", "^r")
    if not re.search(hotkey_regex, reset_hotkey):
        error = (
            "Invalid hotkey. "
            "Check this: https://www.autohotkey.com/docs/v1/Hotkeys.htm#Symbols "
            "The symbols *, ~, $ and UP are not allowed."
        )
        print_error("reset_hotkey", error)
    debugger = set_option("debugger", Config.Overlay, "getboolean", "false")
    font_size = set_option("font_size", Config.Overlay, "getint", "18")
    font_size = font_size if font_size >= 1 else 1
    font_family = set_option(
        "font_family", Config.Overlay, "get", "Consolas, monaco, monospace"
    )
    font_weight = set_option("font_weight", Config.Overlay, "get", "bold")
    max_workers = set_option("max_workers", Config.Overlay, "getint", "2")
    max_workers = max_workers if 1 <= max_workers <= 16 else 2
    hp_update_time = set_option("hp_update_time", Config.Overlay, "getfloat", "0.6")
    hp_update_time = hp_update_time if hp_update_time >= 0.1 else 0.1
    enable_read_ryujinx_logs = set_option(
        "enable_read_ryujinx_logs", Config.Overlay, "getboolean", "false"
    )
    show_initial_hp = set_option(
        "show_initial_hp", Config.Overlay, "getboolean", "true"
    )
    show_hp_percentage = set_option(
        "show_hp_percentage", Config.Overlay, "getboolean", "true"
    )
    show_small_monsters = set_option(
        "show_small_monsters", Config.Overlay, "getboolean", "true"
    )
    show_size_multiplier = set_option(
        "show_size_multiplier", Config.Overlay, "getboolean", "true"
    )
    show_crown = set_option(
        "show_crown", Config.Overlay, "getboolean", "true"
    )
    show_abnormal_status = set_option(
        "show_abnormal_status", Config.Overlay, "getboolean", "true"
    )
    always_show_abnormal_status = set_option(
        "always_show_abnormal_status", Config.Overlay, "getboolean", "false"
    )
    language = set_option("language", Config.Overlay, "get", "en_US")
    locales_directory = Path(absolute_path("locales"))
    available_language = {"en_US"}
    available_language.update(f.stem for f in locales_directory.glob("*.yaml") if f.is_file())
    if language not in available_language:
        error = (
            "Invalid language configuration. Defaulting to 'en_US'. "
            "Use only the available options in the 'locales' folder or create your own custom translation file (.yaml)."
        )
        print_error("language", error)


@dataclass
class ConfigLayout:
    x = set_option("x", Config.Layout, "getint", "100")
    x = x if 0 <= x <= 100 else 100
    y = set_option("y", Config.Layout, "getint", "0")
    y = y if 0 <= y <= 100 else 100
    fix_x = set_option("fix_x", Config.Layout, "getint", "0")
    fix_y = set_option("fix_y", Config.Layout, "getint", "0")
    align = set_option("align", Config.Layout, "getboolean", "true")
    orientation = set_option("orientation", Config.Layout, "get", "center")
    if orientation not in ("center", "left", "right"):
        error = "It can only be center, left or right"
        print_error("orientation", error)
    emu_hide_ui = set_option(
        "emu_hide_ui", Config.Layout, "getboolean", "false"
    )


@dataclass
class ConfigColors:
    text_color = set_option("text_color", Config.Colors, "get", "aquamarine")
    if text_color not in colors:
        error = (
            "Invalid CSS SVG Color. "
            "Check this: https://upload.wikimedia.org/wikipedia/commons/2/2b/SVG_Recognized_color_keyword_names.svg"
        )
        print_error("text_color", error)
    background_color = set_option(
        "background_color", Config.Colors, "get", "darkslategray"
    )
    if background_color not in colors:
        error = (
            "Invalid CSS SVG Color. "
            "Check this: https://upload.wikimedia.org/wikipedia/commons/2/2b/SVG_Recognized_color_keyword_names.svg"
        )
        print_error("background_color", error)
    text_opacity = set_option("text_opacity", Config.Colors, "getint", "100")
    text_opacity = text_opacity if 1 <= text_opacity <= 100 else 100
    background_opacity = set_option("background_opacity", Config.Colors, "getint", "60")
    background_opacity = (
        background_opacity if 1 <= background_opacity <= 100 else 60
    )
    abnormal_status_text_color = set_option(
        "abnormal_status_text_color", Config.Colors, "get", "yellow"
    )
    if abnormal_status_text_color not in colors:
        error = (
            "Invalid CSS SVG Color. "
            "Check this: https://upload.wikimedia.org/wikipedia/commons/2/2b/SVG_Recognized_color_keyword_names.svg"
        )
        print_error("abnormal_status_text_color", error)
    abnormal_status_background_color = set_option(
        "abnormal_status_background_color", Config.Colors, "get", "green"
    )
    if abnormal_status_background_color not in colors:
        error = (
            "Invalid CSS SVG Color. "
            "Check this: https://upload.wikimedia.org/wikipedia/commons/2/2b/SVG_Recognized_color_keyword_names.svg"
        )
        print_error("abnormal_status_background_color", error)
    abnormal_status_text_opacity = set_option(
        "abnormal_status_text_opacity", Config.Colors, "getint", "100"
    )
    abnormal_status_text_opacity = abnormal_status_text_opacity if 1 <= abnormal_status_text_opacity <= 100 else 100
    abnormal_status_background_opacity = set_option(
        "abnormal_status_background_opacity", Config.Colors, "getint", "50"
    )
    abnormal_status_background_opacity = (
        abnormal_status_background_opacity if 1 <= abnormal_status_background_opacity <= 100 else 60
    )
